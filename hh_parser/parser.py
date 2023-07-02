from datetime import datetime

from tqdm import tqdm

from ConnectionManager import ConnectionManager
from db import client
from proxy import proxy_list
import requests as req
from loguru import logger

BASE_VACANCIES_URL = "https://api.hh.ru/vacancies"
log_file = "hh_parser.log"
logger.add(log_file)
PARSER_VER = "0.1.0"
db = client.vacancies
preview_collection = db.preview

def get_metro_stations_ids() -> list[str]: # TODO Create mapper from id to name (and for roles too)
    logger.info("Getting metro stations ids")
    metro = req.get("https://api.hh.ru/metro").json()[0]["lines"]
    station_ids = [st["id"] for line in metro for st in line["stations"]]
    logger.debug(f"Got {len(station_ids)} metro stations ids")
    return station_ids


def get_professional_roles_ids() -> list[str]:
    logger.info("Getting professional roles")
    categories = req.get("https://api.hh.ru/professional_roles").json()
    categories = categories["categories"]
    roles_ids = [role["id"] for cat in categories for role in cat["roles"]]
    logger.debug(f"Got {len(roles_ids)} professional roles")
    return roles_ids


def main():
    con_manager = ConnectionManager(proxies=proxy_list)
    roles_ids = get_professional_roles_ids()
    station_ids = get_metro_stations_ids()

    for role_id in tqdm(roles_ids):
        for station_id in station_ids:
            logger.info(f"Getting vacancies for role {role_id} and station {station_id}")
            params = {
                "area": 1,  # Moscow
                "metro": station_id,
                "professional_role": role_id,
                "per_page": 100,
                "page": 0
            }
            vacancies = []
            while True:
                response = con_manager.get(BASE_VACANCIES_URL, params=params)
                if response.status_code != 200:
                    logger.error(f"Got status code {response.status_code} for role {role_id} and station {station_id}")
                    break
                if response.json()["found"] > 2000:
                    logger.warning(f"Got more than 2000 vacancies for role {role_id} and station {station_id}")
                response = response.json()
                vacancies += response["items"]
                if response["pages"] == params["page"]:
                    break
                params["page"] += 1
            logger.debug(f"Got {len(vacancies)} vacancies for role {role_id} and station {station_id}")
            # Save to mongo DB
            if len(vacancies) != 0:
                # Add today date to each vacancy
                for vacancy in vacancies:
                    vacancy["date"] = datetime.today()
                    vacancy["parser_ver"] = PARSER_VER
                preview_collection.insert_many(vacancies)


if __name__ == '__main__':
    main()
