from vertexai.resources.preview import FeatureOnlineStore,FeatureView,FeatureViewBigQuerySource, feature_store, Feature, FeatureGroup
import yaml
from google.cloud import aiplatform, bigquery
from google.api_core.exceptions import AlreadyExists
from vertexai.resources.preview.feature_store import utils, offline_store, FeatureViewReadResponse as fs_utils
import pandas as pd
from google.cloud.aiplatform_v1 import FeatureOnlineStoreServiceClient
from google.cloud.aiplatform_v1.types import feature_online_store_service as feature_online_store_service_pb2



def create_feature_store(config):
    # Initialize AI platform with project and location from config
    aiplatform.init(project=config['project_id'], location=config['region'])

    # try:
    #     # newfs = FeatureOnlineStore.create_optimized_store(project = config['project_id'],location = config['region'], name = config['feature_store_name'])
    #     # print("Feature store created successfully.")
    #     # newfv=newfs.create_feature_view(name = config['feature_view_name'], project=config['project_id'], location=config['region'],source = FeatureViewBigQuerySource(
    #     # uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table",
    #     # entity_id_columns=["patient_id"],), sync_config=None )

    # except AlreadyExists:
    #     print("Feature store already exists. Skipping creation.")
    newfs = feature_store.FeatureOnlineStore(project = config['project_id'],location = config['region'], name = config['feature_store_name'])
    print(newfs)
    newfv= feature_store.FeatureView(name = config['feature_view_name'],feature_online_store_id=config['feature_store_name'],project = config['project_id'],location = config['region'])
    print(newfv)
    newfg= feature_store.FeatureGroup(name=config['feature_group_name'],project = config['project_id'],location = config['region'])
    print(newfg)

        # newfv=newfs.create_feature_view(name = config['feature_view_name'], project=config['project_id'], location=config['region'],source = FeatureViewBigQuerySource(
        # uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table",
        # entity_id_columns=["patient_id"],), sync_config=None )
    newfv.sync()

    # Initialize the FeatureOnlineStoreServiceClient
    data_client = FeatureOnlineStoreServiceClient(
        client_options={"api_endpoint": f"{config['region']}-aiplatform.googleapis.com"}
    )

    # Create a FetchFeatureValuesRequest using the config values
    fetch_request = feature_online_store_service_pb2.FetchFeatureValuesRequest(
        feature_view=f"projects/{config['project_id']}/locations/{config['region']}/featureOnlineStores/{config['feature_store_name']}/featureViews/{config['feature_view_name']}",
        data_key=feature_online_store_service_pb2.FeatureViewDataKey(key="1") # Replace ENTITY_ID with the actual identifier
    )

    # Execute the request and print the response
    response = data_client.fetch_feature_values(request=fetch_request)
    print(response)

    # data = newfv.read(key=["1"]).to_dict()
    # print(data)
    # newfv.get_sync(78785651717177344)
    featureList=newfg.list_features(project = config['project_id'],location = config['region'])
    featureNames=[]
    

    # fg: FeatureGroup = FeatureGroup.create(
    #     "TestFG",fs_utils.FeatureGroupBigQuerySource(
    #         uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table", entity_id_columns=["patient_id"]
    #     ),
    # )

    # patient_height_feature: Feature = fg.create_feature("patient_height")

    
     






    


    # print(f"Feature store '{config['feature_group_name']}' created successfully.")

    print("Successful code run")

    return "Created feature view and feature store"

if __name__ == "__main__":
    # Load configurations from config.yaml
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Ensure config values are loaded correctly
    print(f"Project ID: {config['project_id']}, Region: {config['region']}")

    # Create the feature store
    create_feature_store(config)
