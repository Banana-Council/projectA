from dataclasses import dataclass
from result import Result
import os

from ..repositories.repositories import ConfigRepository, TrackingRepository

APP_NAME = "projecta"

@dataclass
class InitCommand():
    github_token: str
    pass

class InitHandler:

    def __init__(self, config_repository: ConfigRepository, tracking_repository: TrackingRepository):
        self.config_repository = config_repository
        self.tracking_repository = tracking_repository

    def execute(self, command: InitCommand) -> Result[None, Exception]:

        base_directory_path = os.path.expanduser(f"~/{APP_NAME}/")

        self.create_base_directory(base_directory_path)

        self.config_repository.initiate()

        self.config_repository.write_github_token(command.github_token)

        self.tracking_repository.initiate()

    def create_base_directory(self, base_directory_path: str):
        os.makedirs(base_directory_path, exist_ok=True)
