from flask import url_for, render_template, request, redirect
from sparkflowtools.utils import aws_lambda

from sparkflowserver import app
from sparkflowserver.utils import clusters, transforms as transform_utils, job_runs as job_run_utils


@app.route('/delete_cluster', methods=['POST'])
def delete_cluster():
    """Route to invoke cluster manager Lambda to delete a cluster pool"""
    payload = clusters.delete_cluster_pool(request.form)
    if payload:
        lambda_arn = app.config["CLUSTER_CREATION_LAMBDA"]
        aws_lambda.invoke_function(lambda_arn, payload)
    return redirect(url_for('cluster_pools'))


@app.route('/delete_transform', methods=['POST'])
def delete_transform():
    """Route to delete a transform from Dynamo"""
    transform_utils.delete_transform_record(request.form)
    return redirect(url_for('transforms'))


@app.route('/create_cluster', methods=['POST'])
def create_cluster():
    """Route to invoke cluster manager Lambda to create new EMR clusters"""
    payload = clusters.create_cluster_input(request.form)
    lambda_arn = app.config["CLUSTER_CREATION_LAMBDA"]
    aws_lambda.invoke_function(lambda_arn, payload)
    return redirect(url_for('cluster_pools'))


@app.route('/create_transform', methods=['POST'])
def create_transform():
    """Route to create a new transform"""
    payload = transform_utils.create_transform_input(request.form)
    transform_utils.insert_transform_record(payload)
    return redirect(url_for('transforms'))


@app.route('/cluster_creation')
def cluster_creation():
    """Route to render cluster creation form"""
    return render_template('cluster_creation.html')


@app.route('/transform_creation')
def transform_creation():
    """Route to render cluster transform form"""
    return render_template('transform_creation.html')


@app.route('/cluster_pools')
def cluster_pools():
    """Route to render cluster pools available"""
    clusters_to_render = clusters.get_clusters_in_range()
    return render_template('clusters.html', data=clusters_to_render)


@app.route('/transform_detail')
def transform_detail():
    transform_id = request.args.get('transform_id')
    data = transform_utils.get_transform_record(transform_id)
    return render_template('transform_detail.html', data=[data])


@app.route('/run_transform', methods=['POST'])
def run_transform():
    """Route to create a new transform"""
    transform_id = request.form["transform_id"]
    transform_record = transform_utils.get_transform_record(transform_id)
    payload = job_run_utils.create_job_payload(transform_record)
    print(payload)
    lambda_arn = app.config["STEP_MANAGER_LAMBDA"]
    aws_lambda.invoke_function(lambda_arn, payload)
    return redirect(url_for('job_runs', transform_id=transform_id))


@app.route('/transforms')
def transforms():
    """Route to render transforms available"""
    transforms_to_render = transform_utils.get_transforms_in_range()
    return render_template('transforms.html', data=transforms_to_render)


@app.route('/job_runs')
def job_runs():
    """Route to render transform executions"""
    transform_id = request.args.get('transform_id')
    data = job_run_utils.get_job_runs_for_transform_id(transform_id)
    return render_template('job_runs.html', data=data)


@app.route('/')
@app.route('/index.html')
def index():
    """Route for landing page"""
    return redirect(url_for('transforms'))
