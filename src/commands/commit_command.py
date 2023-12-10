from dataclasses import dataclass
from datetime import datetime
import shutil
from result import Result
import os
import subprocess

from ..repositories.repositories import TrackingRepository


APP_NAME = "projecta"


@dataclass
class CommitCommand:
    alias: str


class CommitHandler:
    def __init__(self, tracking_repository: TrackingRepository):
        self.tracking_repository = tracking_repository

    def execute(self, command: CommitCommand) -> Result[None, Exception]:
        tracked_file_path = self.tracking_repository.get_tracked_file_path(
            command.alias
        )
        tracking_file_path = self.tracking_repository.get_tracking_file_path(
            command.alias
        )

        self.copy_updates(tracked_file_path, tracking_file_path)

        self.commit_updates(tracking_file_path)

        tracking_directory_path = os.path.dirname(tracking_file_path)

        self.push_updates(tracking_directory_path)

    def copy_updates(self, tracked_file_path: str, tracking_file_path: str) -> None:
        shutil.copy2(tracked_file_path, tracking_file_path)

    def commit_updates(self, tracking_file_path: str) -> None:
        tracking_file_name = os.path.basename(tracking_file_path)
        tracking_file_directory = os.path.dirname(tracking_file_path)

        subprocess.run(["git", "add", tracking_file_name], cwd=tracking_file_directory)
        commit_message = f'update {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        subprocess.run(
            ["git", "commit", "-m", commit_message], cwd=tracking_file_directory
        )

    def push_updates(self, tracking_directory_path: str) -> None:
        subprocess.run(
            ["git", "push", "-u", "origin", "master"], cwd=tracking_directory_path
        )
