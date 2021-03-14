import json

from sparkflowtools.models import db

from sparkflowserver import app


def create_job_payload(transform_record: dict) -> dict:
    """Creates a payload to provide to the step manager Lambda when a step is created

    :param transform_record information about the transform for which the run is being kicked off
    :return a payload dictionary with the data needed by the Lambda
    """
    payload = {
        "pool_id": transform_record["pool_id"],
        "step_config": {
            "name": transform_record["transform_name"],
            "spark_args": json.loads(transform_record["app_config"]),
            "job_args": json.loads(transform_record["arguments"]),
            "job_class": transform_record["main_class"],
            "job_jar": transform_record["jar_location"],
            "transform_id": transform_record["transform_id"]
        }
    }
    return payload


def get_job_runs_for_transform_id(transform_id: str) -> list:
    """Retrieves the job records from Dynamo for a given trasform_id

    :param transform_id the ID of the transform to retrieve job runs for
    :returns a list of job run Dynamo records
    """
    jobs_database = db.get_db(app.config["JOBS_DB_TYPE"])()
    jobs_database.connect(app.config["JOBS_DATABASE"])
    jobs_index_name = app.config["JOBS_INDEXNAME"]
    jobs_index_column = app.config["JOBS_INDEX_COLUMN"]
    expression = "{0} = :val".format(jobs_index_column)
    expression_values = {':val': transform_id}
    records = jobs_database.get_records_with_index(
        jobs_index_name, expression, expression_values)[0]
    return records
