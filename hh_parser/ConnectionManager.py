import time
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

    def get(self, wait_for_status_codes=None, *args,
            **kwargs):  # TODO smart exception handling - turn of proxy if it fails
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
                self.ban_proxy(oldest_proxy_index)
            else:
                return r

    def oldest_proxy(self) -> int:
        """Returns index of oldest proxy"""
        return self.proxies_last_used.index(min(self.proxies_last_used))

    def ban_proxy(self, oldest_proxy):
        self.proxies_last_used[oldest_proxy] = time.time() + self.proxy_ban_time  #
        logger.info(f"Banned proxy {self.proxies[oldest_proxy]} for {self.proxy_ban_time} seconds")
