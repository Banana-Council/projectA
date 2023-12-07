from dataclasses import dataclass
from result import Result
import os
import subprocess

from github import Github
from github import Auth

APP_NAME = "projecta"

@dataclass
class CreateBaseRepoCommand():
    github_token: str
    pass

class CreateBaseRepoCommandHandler:

    def execute(self, command: CreateBaseRepoCommand) -> Result[None, Exception]:

        client = Github(auth=Auth.Token(command.github_token))
        _ = client.get_user().create_repo(name=APP_NAME, private=True)

        base_directory = os.path.expanduser(f"~/{APP_NAME}/")
        os.makedirs(base_directory, exist_ok=True)
        
        subprocess.run(['git', 'init'], cwd=base_directory)
