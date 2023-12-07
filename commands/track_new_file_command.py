from dataclasses import dataclass
from result import Result
import os
import shutil
import subprocess
from datetime import datetime

from github import Github
from github import Auth

APP_NAME = "projecta"

@dataclass
class TrackNewFileCommand():
    tracked_file_path: str
    alias: str
    github_token: str

class TrackNewFileHandler:

    def execute(self, command: TrackNewFileCommand) -> Result[None, Exception]:

        base_directory = self.get_base_directory()

        tracking_directory = self.create_tracking_directory(command.alias)

        tracking_file = self.create_tracking_file(tracking_directory, command.tracked_file_path)

        self.copy_file(tracking_directory, command.tracked_file_path, tracking_file)

        self.commit_updates(base_directory, tracking_file)

        self.set_remote_repository(base_directory, command.alias, command.github_token)

        self.push_updates(base_directory)

    def get_base_directory(self) -> str:
        return os.path.expanduser(APP_NAME)

    def create_tracking_directory(self, alias: str) -> str:
        return os.path.expanduser(f"~/{APP_NAME}/{alias}/")
    
    def create_tracking_file(self, tracking_directory: str, tracked_file_path: str) -> str:
        return os.path.join(tracking_directory, os.path.basename(tracked_file_path))

    def copy_file(self, tracking_directory: str, tracked_file_path: str, tracking_file: str) -> str:
        os.makedirs(tracking_directory, exist_ok=True)
        shutil.copy2(tracked_file_path, tracking_file)

    def commit_updates(self, base_directory: str, tracking_file: str) -> None:
        # subprocess.run(['git', 'init'], cwd=tracking_directory)
        subprocess.run(['git', 'add', tracking_file], cwd=base_directory)

        commit_message = f'update {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        subprocess.run(['git', 'commit', '-m', commit_message], cwd=base_directory)

    def set_remote_repository(self, base_directory: str, alias: str, github_token: str) -> None:
        github_client = Github(auth=Auth.Token(github_token))
        remote_repo_ssh_url = github_client.get_user().get_repo(APP_NAME).ssh_url
        subprocess.run(['git', 'remote', 'add', 'origin', remote_repo_ssh_url], cwd=base_directory)

    def push_updates(self, base_directory: str) -> None:
        subprocess.run(['git', 'push', '-u', 'origin', 'master'], cwd=base_directory)
