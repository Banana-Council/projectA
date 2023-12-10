import json
import os
from typing import Dict


APP_NAME = "projecta"


class ConfigRepository:
    config_directory = os.path.expanduser(f"~/.{APP_NAME}config/")
    config_file_path = os.path.expanduser(f"~/.{APP_NAME}config/config.txt")

    def initiate(self):
        os.makedirs(self.config_directory, exist_ok=True)

    def write_github_token(self, github_token: str):
        with open(self.config_file_path, "w") as config_file:
            config_file.write(json.dumps({"github_token": github_token}))

    def get_github_token(self) -> str:
        with open(self.config_file_path, "r") as config_file:
            data = json.load(config_file)
            github_token = data.get("github_token")
            return github_token


class TrackingRepository:
    tracking_file_path = os.path.expanduser(f"~/.{APP_NAME}config/tracking.txt")

    def initiate(self):
        open(self.tracking_file_path, "w").close()

    def add_file(self, alias: str, tracked_file_path: str, tracking_file_path: str):
        with open(self.tracking_file_path, "r") as config_file:
            try:
                content = json.load(config_file)
            except json.JSONDecodeError:
                content = {}

        content[alias] = {
            "tracked_file_path": tracked_file_path,
            "tracking_file_path": tracking_file_path,
        }
        with open(self.tracking_file_path, "w") as config_file:
            json.dump(content, config_file, indent=2)

    def get_tracked_file_path(self, alias: str) -> Dict[str, str]:
        config_file = open(self.tracking_file_path, "r")
        content = json.load(config_file)

        tracked_file_path = content[alias].get("tracked_file_path")

        config_file.close()

        return tracked_file_path

    def get_tracking_file_path(self, alias: str) -> Dict[str, str]:
        config_file = open(self.tracking_file_path, "r")
        content = json.load(config_file)

        tracking_file_path = content[alias].get("tracking_file_path")

        config_file.close()

        return tracking_file_path
