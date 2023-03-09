from typing import Generator, AsyncGenerator, AsyncIterator
from urllib.parse import urljoin

import requests

from HHApi.Exception import NothingFound, HHWrongAnswer
from config import HH_URL
from .Models.SearchResponse import SearchResponse
from .Models.VacancyInfo import Vacancy


class Api:
    def __init__(self, requester):
        self.requester = requester

    async def search_vacancies(self, query: str,
                               per_page: int = 10,
                               area: int = 1) -> AsyncIterator[SearchResponse]:
        """
        docs - https://github.com/hhru/api/blob/master/docs/vacancies.md#search
        :param query: search query
        :param per_page: number of vacancies per page (Параметр per_page ограничен значением в 100)
        :param area: Search region (ex. 1 = Moscow, docs - https://github.com/hhru/api/blob/master/docs/areas.md)
        :return:
        """
        params = {
            'text': query,
            'area': area,
            'page': 0,
            'per_page': per_page
        }
        r = self.requester.get(HH_URL, params)
        if r.status_code != 200:
            raise HHWrongAnswer(f"Status code is {r.status_code} != 200. {r.content[:150]}")
        response: SearchResponse = SearchResponse.parse_raw(r.content)
        if response.found == 0:
            raise NothingFound

        yield response

        for page in range(1, response.pages):
            params['page'] = page
            r = requests.get(HH_URL, params)
            response = SearchResponse.parse_raw(r.content)
            yield response

    async def get_vacancy(self, vacancy_id: int):
        vacancy_url = urljoin(HH_URL, f'vacancies/{vacancy_id}')
        r = self.requester.get(vacancy_url)
        return Vacancy.parse_raw(r.content.decode())
