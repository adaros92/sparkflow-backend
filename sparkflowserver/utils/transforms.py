import uuid

from datetime import datetime, timedelta
from sparkflowtools.models import db

from sparkflowserver import app
from sparkflowserver.utils import dates


def create_transform_input(request_form: dict) -> dict:
    """Creates a transform payload to log in Dynamo

    :param request_form the input form data received via a request to the server
    :returns a payload to insert as a record in Dynamo for the transform being created
    """
    payload = {
        "transform_id": uuid.uuid4().hex,
        "transform_name": request_form["transformName"],
        "pool_id": request_form["poolId"],
        "jar_location": request_form["jarLocation"],
        "main_class": request_form["mainClass"],
        "app_config": request_form["appConfig"],
        "arguments": request_form["arguments"],
        "update_date": dates.get_today_str(),
        "update_datetime": dates.get_today_str(formatting="%Y-%m-%dT%H%M"),
        "creation_date": dates.get_today_str(),
        "creation_datetime": dates.get_today_str(formatting="%Y-%m-%dT%H%M")
    }
    return payload


def insert_transform_record(transform_payload: dict) -> list:
    """Inserts a transform payload as a record in Dynamo

    :param transform_payload the Dynamo record to insert for a given transform
    :returns the list of failed records as provided by Dynamo client
    """
    transform_database = db.get_db(app.config["TRANSFORM_DB_TYPE"])()
    transform_database.connect(app.config["TRANSFORM_DATABASE"])
    return transform_database.insert_records(records=[transform_payload])


def delete_transform_record(request_form: dict) -> list:
    """Deletes a transform record from Dynamo

    :param request_form the form received from a delete request from the UI
    :returns the list of failed deletion records as provided by Dynamo client
    """
    transform_database = db.get_db(app.config["TRANSFORM_DB_TYPE"])()
    transform_database.connect(app.config["TRANSFORM_DATABASE"])
    delete_payload = [
        {"Key": {"transform_id": request_form["transform_id"]}}
    ]
    return transform_database.delete_records(delete_payload)


def get_transform_record(transform_id: str) -> dict:
    """Retrieves the Dynamo record of an individual transform_id"""
    transform_database = db.get_db(app.config["TRANSFORM_DB_TYPE"])()
    transform_database.connect(app.config["TRANSFORM_DATABASE"])
    return transform_database.get_record(keys={"transform_id": transform_id})[0]


def get_transforms_in_range(
        from_date: datetime = dates.get_today(), lookback_days: int = app.config["LOOKBACK_DAY_RANGE"],
        formatting: str = app.config["DATE_FORMAT"]) -> list:
    date_range = dates.get_string_date_range(lookback_days, from_date + timedelta(days=1), formatting)
    transform_database = db.get_db(app.config["TRANSFORM_DB_TYPE"])()
    transform_database.connect(app.config["TRANSFORM_DATABASE"])
    transform_index_name = app.config["TRANSFORM_INDEXNAME"]
    transform_index_column = app.config["TRANSFORM_INDEX_COLUMN"]
    transforms = []
    for transform_update_day in date_range:
        expression = "{0} = :val".format(transform_index_column)
        expression_values = {':val': transform_update_day}
        records = transform_database.get_records_with_index(
            transform_index_name, expression, expression_values)[0]
        transforms.extend(records)
    return transforms
