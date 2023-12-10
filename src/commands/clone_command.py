from dataclasses import dataclass
import shutil
from github import Github, Auth
from result import Result
import os
import subprocess

from ..repositories.repositories import ConfigRepository, TrackingRepository

APP_NAME = "projecta"

@dataclass
class CloneCommand():
    alias: str
    tracked_file_path: str

class CloneHandler:

    def __init__(self, config_repository: ConfigRepository, tracking_repository: TrackingRepository):
        self.config_repository = config_repository
        self.tracking_repository = tracking_repository

    def execute(self, command: CloneCommand) -> Result[None, Exception]:

        base_directory = os.path.expanduser(f"~/{APP_NAME}")

        self.git_clone(base_directory, command.alias)

        tracking_file_path = f"{base_directory}/{command.alias}/{os.path.basename(command.tracked_file_path)}"

        self.update_tracked_file(command.tracked_file_path, tracking_file_path)
        
        self.tracking_repository.add_file(command.alias, command.tracked_file_path, tracking_file_path)

    def git_clone(self, base_directory: str, alias: str):
        github_token = self.config_repository.get_github_token()
        client = Github(auth=Auth.Token(github_token))
        remote_repo_ssh_url = client.get_user().get_repo(alias).ssh_url
        subprocess.run(['git', 'clone', remote_repo_ssh_url], cwd=base_directory)

    def update_tracked_file(self, tracked_file_path: str, tracking_file_path: str):
        shutil.copy2(tracking_file_path, tracked_file_path)

