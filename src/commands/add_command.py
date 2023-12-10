from dataclasses import dataclass
from github import Github, Auth
from result import Result
import os
import subprocess

from ..repositories.repositories import ConfigRepository, TrackingRepository

APP_NAME = "projecta"

@dataclass
class AddCommand():
    tracked_file_path: str
    alias: str

class AddHandler:

    def __init__(self, config_repository: ConfigRepository, tracking_repository: TrackingRepository):
        self.config_repository = config_repository
        self.tracking_repository = tracking_repository

    def execute(self, command: AddCommand) -> Result[None, Exception]:

        tracking_directory_path = os.path.expanduser(f"~/{APP_NAME}/{command.alias}")

        github_token = self.config_repository.get_github_token()

        self.create_tracking_directory(tracking_directory_path) 

        self.git_init_tracking_directory(tracking_directory_path)

        self.create_remote_repository(github_token, command.alias)

        self.set_remote_repository(command.alias, github_token, tracking_directory_path)

        tracking_file_path = f"{tracking_directory_path}/{os.path.basename(command.tracked_file_path)}"

        self.tracking_repository.add_file(command.alias, command.tracked_file_path, tracking_file_path)
    
    def create_tracking_directory(self, tracking_directory: str) -> None:
        os.makedirs(tracking_directory, exist_ok=True)
    
    def git_init_tracking_directory(self, tracking_directory: str) -> None:
        subprocess.run(['git', 'init'], cwd=tracking_directory)

    def create_remote_repository(self, github_token: str, alias: str):
        client = Github(auth=Auth.Token(github_token))
        try: 
            client.get_user().create_repo(name=alias, private=True)
        except Exception:
            pass

    def set_remote_repository(self, alias: str, github_token: str, tracking_directory: str):
        client = Github(auth=Auth.Token(github_token))
        remote_repo_ssh_url = client.get_user().get_repo(alias).ssh_url
        subprocess.run(['git', 'remote', 'add', 'origin', remote_repo_ssh_url], cwd=tracking_directory)
