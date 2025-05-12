from huggingface_hub import HfApi

api = HfApi(token="")
api.upload_folder(
    folder_path="C:\\Users\\Autaza\\Documents\\Fatec\\\Bertoti\\fine_tuned_gpt2",
    repo_id="karencgoncalves/login_wireframe_json",
    repo_type="dataset",
)
