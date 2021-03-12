from flask import Flask


app = Flask(__name__)

app.config["CLUSTER_CREATION_LAMBDA"] = "arn:aws:lambda:us-east-1:146066720211:function:sparkflow-lambdas-ClusterManagerFunction-MSGJ92NXWDU3"
app.config["CLUSTER_POOL_DB_TYPE"] = "DYNAMO"
app.config["CLUSTER_POOL_DATABASE"] = "sparkflow_cluster_pools"
app.config["TRANSFORM_DB_TYPE"] = "DYNAMO"
app.config["TRANSFORM_DATABASE"] = "sparkflow_transforms"
app.config["CLUSTER_POOL_INDEX_COLUMN"] = "update_date"
app.config["CLUSTER_POOL_INDEXNAME"] = "LastUpdatedPoolIndex"
app.config["TRANSFORM_INDEX_COLUMN"] = "update_date"
app.config["TRANSFORM_INDEXNAME"] = "LastUpdateIndex"
app.config["SUPPORTED_APPLICATIONS"] = ["Spark", "Zeppelin"]
app.config["DATE_FORMAT"] = "%Y-%m-%d"
app.config["LOOKBACK_DAY_RANGE"] = 7

import sparkflowserver.views
