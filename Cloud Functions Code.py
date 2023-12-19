from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import os
import logging
import json


def instantiate_inline_workflow_template(event, context):
    # Initialise clients
    storage_client = storage.Client()

    # Get variables
    project_id = os.environ.get("GCP_PROJECT")  
    region = os.environ.get("FUNCTION_REGION")  
    main_python_file_uri = os.environ.get(
        "main_python_file_uri") 
    input_file = f"gs://{event['bucket']}/{event['name']}"

    # Create a client with the endpoint set to the desired region.
    workflow_template_client = dataproc.WorkflowTemplateServiceClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )
    parent = f"projects/{project_id}/regions/{region}"

    template = {
        "jobs": [
            {
                "pyspark_job": {
                    "main_python_file_uri": main_python_file_uri,
                    "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
                    "args": ["gs://dataflow-stockdata-input",
                    "parquet",
                    "insert_dt", 
                    "dataflow-stockdata", 
                    "dataflow_stockdata_dataset",
                    "financial_data",
                    "chenmingyong-cloud-dataproc-output-vmk"],
                },
                "step_id": "pyspark_etl",
            },
        ],
        "placement": {
            "managed_cluster": {
                "cluster_name": "gcp-etl-cluster",
                "config": {
                    "gce_cluster_config": {"zone_uri": ""},
                    "master_config": {"num_instances": 1, "machine_type_uri": "n2-standard-4"},
                    "worker_config": {"num_instances": 2, "machine_type_uri": "n2-standard-4"},
                    "software_config": {"image_version": "1.5-debian"},
                },
            }
        },
    }

    logging.info(
        f"Creating temporary dataproc cluster to run pyspark job on {input_file} and extract result to")

    operation = workflow_template_client.instantiate_inline_workflow_template(
        request={"parent": parent, "template": template}
    )
    operation.result()
    logging.info("Workflow ran successfully.")