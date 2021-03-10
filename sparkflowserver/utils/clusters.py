import logging

from datetime import datetime, timedelta
from sparkflowtools.models import db

from sparkflowserver import app
from sparkflowserver.utils import dates


def _parse_applications_from_cluster_input(request_form: dict) -> list:
    """Parses the application to install on a cluster being launched from a server request

    :param request_form the input form data received via a request to the server
    :returns a list of applications to install on a cluster
    """
    return [{"Name": application} for application in app.config["SUPPORTED_APPLICATIONS"]
            if "apps{0}".format(application) in request_form]


def create_cluster_input(request_form: dict) -> dict:
    """Creates a Lambda payload for launching new EMR clusters

    :param request_form the input form data received via a request to the server
    :returns a list of EMR creation configs to pass to the cluster manager Lambda
    """
    number_of_clusters = int(request_form["clusterCount"])
    applications = _parse_applications_from_cluster_input(request_form)
    termination_protection = False
    if request_form.get("terminationProtection", "False") == "True":
        termination_protection = True
    auto_terminate = False
    if request_form.get("autoTerminate", "False") == "True":
        auto_terminate = True
    payload = {
        "operation": "create",
        "emr_config": [
            {
                "Name": "{0} pool | SparkFlow-cluster-{1}-".format(request_form["clusterName"], cluster),
                "LogUri": request_form["logUri"],
                "ReleaseLabel": request_form["emrReleaseLabel"],
                "Applications": applications,
                "Ec2InstanceAttributes": {
                    "Ec2KeyName": "mykey5.pem",
                    "Ec2SubnetId": "subnet-f72b0bf8",
                    "Ec2AvailabilityZone": request_form["availabilityZone"],
                    "IamInstanceProfile": request_form["ec2InstanceProfile"],
                    "EmrManagedMasterSecurityGroup": "sg-00888c4bd2e63f00f",
                    "EmrManagedSlaveSecurityGroup": "sg-06e7f80706c55ed8d"
                },
                "Tags": [{"Key": "environment", "Value":  "experimental"}],
                "AutoTerminate": auto_terminate,
                "TerminationProtected": termination_protection,
                "Configurations": [],
                "ServiceRole": request_form["emrServiceRole"]
            } for cluster in range(number_of_clusters)
        ]
    }
    return payload


def delete_cluster_pool(request_form: dict) -> dict:
    """Creates a Lambda payload to delete clusters with

    :param request_form the input form data received via a request to the server
    :returns an EMR deletion config to pass to the cluster manager Lambda
    """
    pool_id = request_form.get("cluster_pool_id")
    if not pool_id:
        logging.warning("cluster_pool_id not available in {0}".format(request_form))
        return {}
    return {"operation": "delete", "pool_id": pool_id, "emr_config": {}}



def get_clusters_in_range(
        from_date: datetime = dates.get_today(), lookback_days: int = app.config["LOOKBACK_DAY_RANGE"],
        formatting: str = app.config["DATE_FORMAT"]) -> list:
    date_range = dates.get_string_date_range(lookback_days, from_date + timedelta(days=1), formatting)
    cluster_pool_database = db.get_db(app.config["CLUSTER_POOL_DB_TYPE"])()
    cluster_pool_database.connect(app.config["CLUSTER_POOL_DATABASE"])
    cluster_pool_index_name = app.config["CLUSTER_POOL_INDEXNAME"]
    cluster_pool_index_column = app.config["CLUSTER_POOL_INDEX_COLUMN"]
    cluster_pools = []
    for cluster_update_day in date_range:
        expression = "{0} = :val".format(cluster_pool_index_column)
        expression_values = {':val': cluster_update_day}
        records = cluster_pool_database.get_records_with_index(
            cluster_pool_index_name, expression, expression_values)[0]
        cluster_pools.extend(records)
    return cluster_pools
