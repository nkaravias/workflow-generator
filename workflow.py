import Stage
from typing import List


class Workflow:
    def __init__(self, workflow_template: str, changed_files: List[str]):
        self.stages = []
        self.changed_files = changed_files

    def add_stage(self, stage: Stage):
        self.stages.append(stage)