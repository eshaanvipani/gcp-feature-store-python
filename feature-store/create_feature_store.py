from vertexai.resources.preview import FeatureOnlineStore,FeatureView,FeatureViewBigQuerySource, feature_store
import yaml
from google.cloud import aiplatform
from google.api_core.exceptions import AlreadyExists
from google.cloud.aiplatform_v1beta1.types import feature_view as feature_view_pb2


def create_feature_store(config):
    # Initialize AI platform with project and location from config
    aiplatform.init(project=config['project_id'], location=config['region'])

    try:
        newfs = FeatureOnlineStore.create_optimized_store(project = config['project_id'],location = config['region'], name = config['feature_store_name'])
        print("Feature store created successfully.")
        newfv=newfs.create_feature_view(name = config['feature_view_name'], project=config['project_id'], location=config['region'],source = FeatureViewBigQuerySource(
        uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table",
        entity_id_columns=["patient_id"],), sync_config=None )

    except AlreadyExists:
        print("Feature store already exists. Skipping creation.")
    # feature_registry_source = feature_view_pb2.FeatureView.FeatureRegistrySource(
    #     feature_groups=[
    #         feature_view_pb2.FeatureView.FeatureRegistrySource.FeatureGroup(
    #             feature_group_id=config['feature_group_name'], feature_ids=test1
    #         )
    #     ]
    # )
    newfs = feature_store.FeatureOnlineStore(project = config['project_id'],location = config['region'], name = config['feature_store_name'])
    print(newfs)
    newfv= feature_store.FeatureView(name = config['feature_view_name'],feature_online_store_id=config['feature_store_name'],project = config['project_id'],location = config['region'])
    print(newfv)
    newfg= feature_store.FeatureGroup(name=config['feature_group_name'],project = config['project_id'],location = config['region'])
    print(newfg)
    
    print("Successful code run")
    
    # Create the feature store using the preview API
    # try:
    #     fg = feature_store.FeatureGroup.create(
    #         name=config['feature_group_name'],
    #         source=feature_store.utils.FeatureGroupBigQuerySource(
    #             uri="bq://glowing-baton-440204-i1.featuregroup_test.test_table", 
    #             entity_id_columns=["patient_id"]
    #         ),
    #     )
    # except AlreadyExists:
    #     print("Feature group already exists. Skipping creation.")

    # print(f"Feature store '{config['feature_group_name']}' created successfully.")
    return "Created feature view and feature store"

if __name__ == "__main__":
    # Load configurations from config.yaml
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Ensure config values are loaded correctly
    print(f"Project ID: {config['project_id']}, Region: {config['region']}")

    # Create the feature store
    create_feature_store(config)
