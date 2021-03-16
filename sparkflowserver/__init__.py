from flask import Flask


app = Flask(__name__)

app.config["CLUSTER_CREATION_LAMBDA"] = "SparkflowClusterManager"
app.config["STEP_MANAGER_LAMBDA"] = "SparkflowStepManager"
app.config["CLUSTER_POOL_DB_TYPE"] = "DYNAMO"
app.config["CLUSTER_POOL_DATABASE"] = "sparkflow_cluster_pools"
app.config["TRANSFORM_DB_TYPE"] = "DYNAMO"
app.config["TRANSFORM_DATABASE"] = "sparkflow_transforms"
app.config["JOBS_DB_TYPE"] = "DYNAMO"
app.config["JOBS_DATABASE"] = "sparkflow_job_runs"
app.config["CLUSTER_POOL_INDEX_COLUMN"] = "update_date"
app.config["CLUSTER_POOL_INDEXNAME"] = "LastUpdatedPoolIndex"
app.config["TRANSFORM_INDEX_COLUMN"] = "update_date"
app.config["TRANSFORM_INDEXNAME"] = "LastUpdateIndex"
app.config["JOBS_INDEX_COLUMN"] = "transform_id"
app.config["JOBS_INDEXNAME"] = "ParentTransformIndex"
app.config["SUPPORTED_APPLICATIONS"] = ["Spark", "Zeppelin"]
app.config["DATE_FORMAT"] = "%Y-%m-%d"
app.config["LOOKBACK_DAY_RANGE"] = 7

import sparkflowserver.views
