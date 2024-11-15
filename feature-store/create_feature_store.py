from vertexai.resources.preview import FeatureOnlineStore,FeatureView,FeatureViewBigQuerySource, feature_store, Feature, FeatureGroup
import yaml
from google.cloud import aiplatform, bigquery
from google.api_core.exceptions import AlreadyExists
from vertexai.resources.preview.feature_store import utils, offline_store, FeatureViewReadResponse as fs_utils
import pandas as pd
from google.cloud.aiplatform_v1 import FeatureOnlineStoreServiceClient
from google.cloud.aiplatform_v1.types import feature_online_store_service as feature_online_store_service_pb2

def create_features(config):
    # # Initialize AI platform with project and location from config
    # aiplatform.init(project=config['project_id'], location=config['region'])
    for group in config['feature_groups']:
        currfg= feature_store.FeatureGroup(name=group,project = config['project_id'],location = config['region'])
        for feature in group['features']:
            currfg.create_feature(name=feature['name'],project=config['project_id'], location=config['region'])

    print("Successful created features in feature groups")
    return "Created feature view and feature store"

def create_feature_groups(config):
    # Initialize AI platform with project and location from config
    aiplatform.init(project=config['project_id'], location=config['region'])

    newfs = feature_store.FeatureOnlineStore(project = config['project_id'],location = config['region'], name = config['feature_store_name'])

    # bigQuerySource = feature_store.FeatureGroupBigQuerySource(
    #     uri=config['bqsource'],
    #     entity_id_columns="patient_id",
    # )
    for group in config['feature_groups']:
        # feature_store.FeatureGroup.create(name=group, source = bigQuerySource, project =  config['project_id'],location = config['region'])
        print('dsdds')
        feature_store.FeatureGroup.create(
            name=group,
            source=feature_store.utils.FeatureGroupBigQuerySource(
                uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table", 
                entity_id_columns=["patient_id"]
            ),
        )
    # create_features(config)

    print("Successful created featuregroups")
    return "Created feature view and feature store"

if __name__ == "__main__":
    # Load configurations from config.yaml
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Ensure config values are loaded correctly
    print(f"Project ID: {config['project_id']}, Region: {config['region']}")

    # Create the feature store
    create_feature_groups(config)
