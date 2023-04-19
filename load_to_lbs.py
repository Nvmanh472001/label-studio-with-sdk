import os
from label_studio_sdk import Client
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())

lbs_url = "http://172.20.0.2:8080"
lbs_auth_key = os.getenv("LABEL_STUDIO_USER_TOKEN")

lbs_client = Client(url=lbs_url, api_key=lbs_auth_key)
lbs_client.delete_all_projects()


with open("./configuration.xml", encoding="utf-8", mode="r") as buf:
    label_configuration = buf.read()

lbs_client.delete_all_projects()
project = lbs_client.start_project(
    title="KIE FROM CV DATA",
    label_config=label_configuration,
)

local_storage_config = {
    "local_store_path": "/data/raw/img",
    "regex_filter": "*.(jp?eg|png)",
    "title": "CV Dataset",
}
local_storage = project.connect_local_import_storage(
    local_store_path="/data/raw/img", regex_filter=".*(jpe?g|png)", title="CV Dataset"
)

# project.sync_storage(storage_type=local_storage["type"], storage_id=local_storage["id"])
project.import_tasks("/src/train.json")
project.import_tasks("/src/test.json")
