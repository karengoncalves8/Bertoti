from dotenv import load_dotenv
from huggingface_hub import HfApi
import os

load_dotenv()

hf = os.getenv("HH_TOKEN")

api = HfApi(token=hf)
api.upload_folder(
    folder_path="C:\\Users\\Autaza\\Documents\\Fatec\\Bertoti\\fine_tuned_gpt2",
    repo_id="karencgoncalves/figma_wireframe_generator",
    repo_type="model",
)
