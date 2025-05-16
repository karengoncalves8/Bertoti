from dotenv import load_dotenv
from huggingface_hub import HfApi
import os

load_dotenv()

hf = os.getenv("HH_TOKEN")

api = HfApi(token=hf)
api.upload_folder(
    folder_path="C:\\Users\\Autaza\\Documents\\Fatec\\Bertoti\\models\\datasets",
    repo_id="karencgoncalves/login_wireframe_json",
    repo_type="dataset",
)
