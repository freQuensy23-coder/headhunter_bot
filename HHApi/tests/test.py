import unittest

import HHApi.Models.SearchResponse
from HHApi.HHApi import Api as HeadHunterAPI
import requests


class HeadhunterTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.api = HeadHunterAPI(requester=requests)
        self.test_vacancy_id = None

    async def test_search(self):
        response: HHApi.Models.SearchResponse.SearchResponse = \
            await self.api.search_vacancies(query="Scala developer").__anext__()
        print(response)
        self.test_vacancy_id = response.items[0].id
        self.assertIsInstance(response, HHApi.Models.SearchResponse.SearchResponse)

    async def test_get_vacancy(self):
        if self.test_vacancy_id is None:
            await self.test_search()
        vacancy = await self.api.get_vacancy(vacancy_id=self.test_vacancy_id)
        self.assertIsInstance(vacancy, HHApi.Models.VacancyInfo.Vacancy)
        print(vacancy)
        self.assertEqual(self.test_vacancy_id, vacancy.id)
