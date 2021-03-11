from flask import url_for, render_template, request, redirect
from sparkflowtools.utils import aws_lambda

from sparkflowserver import app
from sparkflowserver.utils import clusters


@app.route('/delete_cluster', methods=['POST'])
def delete_cluster():
    """Route to invoke cluster manager Lambda to delete a cluster pool"""
    payload = clusters.delete_cluster_pool(request.form)
    if payload:
        lambda_arn = app.config["CLUSTER_CREATION_LAMBDA"]
        aws_lambda.invoke_function(lambda_arn, payload)
    return redirect(url_for('cluster_pools'))


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


@app.route('/transforms')
def transforms():
    """Route to render transforms available"""
    return render_template('transforms.html', data=[])


@app.route('/job_runs')
def job_runs():
    """Route to render transform executions"""
    return render_template('job_runs.html', data=[])


@app.route('/')
@app.route('/index.html')
def index():
    """Route for landing page"""
    return render_template('transforms.html')
