import yaml
from typing import List

from stage import Stage
from deployment import Deployment


class Workflow:
    def __init__(self, workflow_template: str, changed_files: List[str]):
        self.stages = []
        self.changed_files = changed_files

    def add_stage(self, stage: Stage):
        self.stages.append(stage)


    def to_yaml(self) -> str:
        workflow_dict = {}
        for stage in self.stages:
            stage_dict = {
                "description": stage.description,
                "deployments": {}
            }
            for deployment in stage.deployments:
                deployment_dict = {
                    "active": deployment.active,
                }
                if deployment.active:
                    deployment_dict["matches"] = self.get_deployment_matches(deployment)
                    deployment_dict["parameters"] = deployment.parameters
                stage_dict["deployments"][deployment.name] = deployment_dict
            workflow_dict[stage.sequence] = stage_dict
        return yaml.dump(workflow_dict)

    def get_deployment_matches(self, deployment: Deployment) -> List[dict]:
        matches = []
        for trigger in deployment.triggers:
            if trigger.triggered:
                trigger_match = {
                    "pattern": trigger.path,
                    "files": trigger.matching_files
                }
                matches.append(trigger_match)
        return matches