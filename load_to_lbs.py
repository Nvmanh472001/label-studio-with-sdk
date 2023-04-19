import os
from label_studio_sdk import Client
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())

lbs_url = "http://localhost:8080"
lbs_auth_key = os.getenv("LABEL_STUDIO_USER_TOKEN")

lbs_client = Client(url=lbs_url, api_key=lbs_auth_key)
lbs_client.delete_all_projects()


with open("./configuration.xml", encoding="utf-8", mode="r") as buf:
    label_configuration = buf.read()


project = lbs_client.start_project(
    title="KIE FROM CV DATA",
    label_config=label_configuration,
)

local_storage_config = {
    "local_store_path": f"{os.path.abspath(os.path.dirname(__file__))}/data/raw",
    "regex_filter": "*.(jp?eg|png)",
    "title": "CV Dataset",
}
local_storage = project.connect_local_import_storage(**local_storage_config)

project.sync_storage(local_storage["id"])
