from pandas.io import json
import requests
import pandas as pd
from data_app.config import app, logger
from data_app import mongo


def call_duckduckgo(q):
    duckduck_url = "https://api.duckduckgo.com/"
    params = {"q": q, "format": "json", "pretty": "1"}
    try:
        r = requests.get(url=duckduck_url, params=params)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logger.exception(e)


@app.task
def insert_db(collection_name, data, filter):
    collection = mongo.get_collection(collection_name)
    result = collection.replace_one(filter, data, upsert=True)
    logger.info(
        f"matched = {result.matched_count}, modified = {result.modified_count}, upserted_id = {result.upserted_id}"
    )
    return result.matched_count, result.modified_count, str(result.upserted_id)


@app.task
def add_url_description(year, uni_data):
    uni_data = pd.read_json(uni_data)
    uni_data = uni_data.rename(columns=str.strip)
    uni_data["Url"] = ""
    uni_data["Description"] = ""

    for i, _ in enumerate(uni_data):
        uni = uni_data.loc[i]["Institution"]
        api_data = call_duckduckgo(uni)
        try:
            api_data = json.loads(api_data)
        except TypeError as e:
            api_data = {}
            logger.exception(e)
        finally:
            insert_db.delay(
                "university",
                {
                    "University": uni,
                    "Url": api_data.get("AbstractURL", None),
                    "Description": api_data.get("Abstract", None),
                },
                {"University": uni},
            )
            uni_data.at[i, ["Url"]] = api_data.get("AbstractURL", None)
            uni_data.at[i, ["Description"]] = api_data.get("Abstract", None)
            logger.info(uni_data.loc[i])

    uni_data = uni_data.to_json()
    insert_db.delay(
        "yearly", {"year": year, "data": uni_data}, {"year": year}
    )

    return uni_data
