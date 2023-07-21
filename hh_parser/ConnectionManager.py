import time

import grequests as grequests
import requests as req
from random_user_agent.user_agent import UserAgent
from loguru import logger


class ConnectionManager:
    def __init__(self, proxies: [dict], wait_time: float = 1.0, user_agent_manager=None,
                 proxy_ban_time: int = 2 * 60 * 60):
        """
        proxies last used - list of timestamps of usage of proxies
        :param proxies: list of proxies to rotate through
        :param wait_time: time to wait between requests
        """
        if user_agent_manager is None:
            self.user_agent_manager = UserAgent()
        else:
            self.user_agent_manager = user_agent_manager
        self.proxies = proxies
        self.proxies_last_used = [time.time()] * len(proxies)
        self.wait_time = wait_time
        self.proxy_ban_time = proxy_ban_time

    def get(self, wait_for_status_codes=None, *args, **kwargs):
        """
        Rotates through proxies and waits between requests
        :param wait_for_status_codes: if status code is not in wait_for_status_code manager will repeat request using other proxy. This one will be banned for proxi_ban_time
        :param args: args to pass to requests.get
        :param kwargs: kwargs to pass to requests.get
        :return: requests.get response
        """
        if wait_for_status_codes is None:
            wait_for_status_codes = [200]
        successful_request = False
        while not successful_request:
            oldest_proxy_index = self.oldest_proxy()
            if time.time() - self.proxies_last_used[oldest_proxy_index] < self.wait_time:
                logger.debug(
                    f"Waiting for {self.wait_time - (time.time() - self.proxies_last_used[oldest_proxy_index])} seconds")
                time.sleep(self.wait_time - (time.time() - self.proxies_last_used[oldest_proxy_index]))

            self.proxies_last_used[oldest_proxy_index] = time.time()
            proxy = self.proxies[oldest_proxy_index]
            r = req.get(*args, **kwargs, proxies=proxy)
            if r.status_code not in wait_for_status_codes:
                logger.warning(f"Got status code {r.status_code} for proxy {proxy}")
                if r.status_code == 403:
                    self.ban_proxy(oldest_proxy_index)
                elif r.status_code == 404:
                    return self.set_404_json(r)
            else:
                return r

    def oldest_proxy(self) -> int:
        """Returns index of oldest proxy"""
        return self.proxies_last_used.index(min(self.proxies_last_used))

    def batch_oldest_proxy(self, batch_size: int) -> list[int]:
        """Returns list of batch_size indexes of oldest proxies."""
        return sorted(range(len(self.proxies_last_used)), key=lambda i: self.proxies_last_used[i])[:batch_size]

    def ban_proxy(self, oldest_proxy):
        self.proxies_last_used[oldest_proxy] = time.time() + self.proxy_ban_time  #
        logger.info(f"Banned proxy {self.proxies[oldest_proxy]} for {self.proxy_ban_time} seconds")

    @staticmethod
    def set_404_json(response):
        try:
            r_json = response.json()
        except:
            r_json = {}
        return r_json + {"status_code": 404, 'status': 'error', "msg": "not found", "url": response.url,
                         "proxy": response.proxy}

    def batch_get(self, urls: [str], wait_for_status_codes=None):
        """
        Get batch of urls using grequests
        :param wait_for_status_codes: Optional[list[int]] list of accepted status codes. Default: [200]
        :param urls: list of urls to get
        """
        if wait_for_status_codes is None:
            wait_for_status_codes = [200]
        proxy_indexes = self.batch_oldest_proxy(len(urls))
        proxies = [self.proxies[i] for i in proxy_indexes]
        if time.time() - self.proxies_last_used[proxy_indexes[0]] < self.wait_time:
            logger.debug(
                f"Waiting for {self.wait_time - (time.time() - self.proxies_last_used[proxy_indexes[0]])} seconds")
            time.sleep(self.wait_time - (time.time() - self.proxies_last_used[proxy_indexes[0]]))
        reqs = [grequests.get(url, proxies=proxies[i]) for i, url in enumerate(urls)]
        responses = grequests.map(reqs)
        for i, r in enumerate(responses):
            if r.status_code in wait_for_status_codes:
                responses[i] = r
            else:
                logger.warning(f"Got status code {r.status_code} for proxy {proxies[i]} and url {urls[i]}")
                if r.status_code == 403:
                    self.ban_proxy(proxy_indexes[i])
                    responses[i] = self.get(url=urls[i])
                elif r.status_code == 404:
                    responses[i] = self.set_404_json(r)
                else:
                    logger.critical(f"Unknown status code {r.status_code} for proxy {proxies[i]} and url {urls[i]}")
                    responses[i] = self.get(url=urls[i])
        return responses
