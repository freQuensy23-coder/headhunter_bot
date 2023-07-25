import logging
from datetime import datetime

from tqdm import tqdm

from ConnectionManager import ConnectionManager
from db import client
from proxy import proxy_list
from requests import Response
from loguru import logger

log_file = "hh_full_info_parser.log"
con_manager = ConnectionManager(proxies=proxy_list)
logger.add(log_file)
logger.level("DEBUG")
PARSER_VER = 9
db = client.vacancies
preview_collection = db.preview
info_collection = db.info


def batcher(iterator, batch_size: int = 4):
    batch = []
    for item in iterator:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def get_json(r: Response)-> dict:
    try:
        res = r.json()
    except:
        logger.error(f"Error while getting json from {r.url}")
        res = {}
    if r.status_code == 404:
        res.update({"status_code": 404, 'status': 'error', "msg": "not found", "url": r.url})
    return res

def parse():
    # Get saved_vacancies from mongo vacancies.preview
    # Получи все вакансии из preview collection у которых нет параметра full_info
    # (параметр full_info означает, что вакансия уже была обработана)
    for vacancy_preview in tqdm(preview_collection.find({"full_info": {"$exists": False}})):
        url = vacancy_preview["url"]
        logger.info(f"Getting vacancy info from {url}")
        vacancy_info = con_manager.get(url=url).json()
        info_collection.insert_one(vacancy_info)
        preview_collection.update_one(update={"$set": {"full_info": {"$ref": "info", "$id": vacancy_info["_id"]}}},
                                      filter={"url": url})
        logger.debug(f"Vacancy {url} was updated")


def gparse():
    QUERY = {"full_info": {"$exists": False}}
    total_vacancies = preview_collection.count_documents(QUERY)
    for vacancies_batch in batcher(tqdm(preview_collection.find(QUERY), total=total_vacancies)):
        urls = [vacancy["url"] for vacancy in vacancies_batch]
        logger.info(f"Getting vacancies info from {len(urls)} urls")
        vacancies_info = list(map(get_json, con_manager.batch_get(urls=urls)))
        info_collection.insert_many(vacancies_info)
        for i, vacancy_info in enumerate(vacancies_info):
            preview_collection.update_one(
                update={"$set": {"full_info": {"$ref": "info", "$id": vacancy_info["_id"]}}},
                filter={"url": urls[i]})
        logger.debug(f"Vacancies {urls} were updated")


if __name__ == "__main__":
    gparse()
