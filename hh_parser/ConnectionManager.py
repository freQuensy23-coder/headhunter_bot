import time
import requests as req
from random_user_agent.user_agent import UserAgent

class ConnectionManager:
    def __init__(self, proxies: [dict], wait_time: float = 1.0, user_agent_manager=None):
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

    def get(self, *args, **kwargs):
        """
        Rotates through proxies and waits between requests
        :param args: args to pass to requests.get
        :param kwargs: kwargs to pass to requests.get
        :return: requests.get response
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {"User-Agent": self.user_agent_manager.get_random_user_agent()}
        elif "User-Agent" not in kwargs["headers"]:
            kwargs["headers"]["User-Agent"] = self.user_agent_manager.get_random_user_agent()

        oldest_proxy = self.oldest_proxy()
        if time.time() - self.proxies_last_used[oldest_proxy] < self.wait_time:
            print(f"Waiting for {self.wait_time - (time.time() - self.proxies_last_used[oldest_proxy])} seconds")
            time.sleep(self.wait_time - (time.time() - self.proxies_last_used[oldest_proxy]))

        self.proxies_last_used[oldest_proxy] = time.time()
        proxy = self.proxies[oldest_proxy]
        return req.get(*args, **kwargs, proxies=proxy)

    def oldest_proxy(self):
        return self.proxies_last_used.index(min(self.proxies_last_used))
