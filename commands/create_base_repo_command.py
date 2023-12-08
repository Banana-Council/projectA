from dataclasses import dataclass
from result import Result
import os
import subprocess
import json
from github import Github
from github import Auth

APP_NAME = "projecta"

@dataclass
class CreateBaseRepoCommand():
    github_token: str
    pass

class CreateBaseRepoCommandHandler:

    def execute(self, command: CreateBaseRepoCommand) -> Result[None, Exception]:

        base_directory = self.create_base_directory()

        self.create_github_repository(command.github_token)

        self.set_remote_repository(command.github_token, base_directory)

        self.start_tracking(base_directory)

        self.create_config_directory()

        self.write_github_token_in_config_file(command.github_token)

    def create_base_directory(self):
        base_directory = os.path.expanduser(f"~/{APP_NAME}/")
        os.makedirs(base_directory, exist_ok=True)
        return base_directory
    
    def create_github_repository(self, github_token: str):
        client = Github(auth=Auth.Token(github_token))
        client.get_user().create_repo(name=APP_NAME, private=True)

    def set_remote_repository(self, github_token: str, base_directory: str):
        github_client = Github(auth=Auth.Token(github_token))
        remote_repo_ssh_url = github_client.get_user().get_repo(APP_NAME).ssh_url
        subprocess.run(['git', 'remote', 'add', 'origin', remote_repo_ssh_url], cwd=base_directory)

    def start_tracking(self, base_directory):
        subprocess.run(['git', 'init'], cwd=base_directory)

    def create_config_directory(self):
        config_directory = os.path.expanduser(f"~/.{APP_NAME}config/")
        os.makedirs(config_directory, exist_ok=True)

    def write_github_token_in_config_file(self, github_token: str):
        config_file_path = os.path.expanduser(f"~/.{APP_NAME}config/config.txt")
        config_file = open(config_file_path, 'w')
        config_file.write(json.dumps({"github_token": github_token}))
        config_file.close()
