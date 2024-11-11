from vertexai.resources.preview import FeatureOnlineStore,FeatureView,FeatureViewBigQuerySource, feature_store, Feature, FeatureGroup
import yaml
from google.cloud import aiplatform, bigquery
from google.api_core.exceptions import AlreadyExists
from vertexai.resources.preview.feature_store import utils as fs_utils
import pandas as pd




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

    featureList=newfg.list_features(project = config['project_id'],location = config['region'])
    featureNames=[]
    for feature in featureList:
        featureNames.append(feature.name)
    print(featureNames)
    client = bigquery.Client()

    # Define your BigQuery table (replace with your actual table details)
    table_id = "glowing-baton-440204-i1.featuregroup_test.test_table"

    # Create a query to select only the specified features
    query = f"""
        SELECT {', '.join(featureNames)}
        FROM `{table_id}`
    """

    # Execute the query
    query_job = client.query(query)

    # Convert the result to a DataFrame
    feature_data = query_job.to_dataframe()

    # Display or inspect the retrieved feature data
    print(feature_data.to_string())
        
    
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
