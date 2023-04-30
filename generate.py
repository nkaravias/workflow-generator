import re
import yaml
from typing import List

class TriggerInput:
    def __init__(self, name: str, input_type: str, value: str):
        self.name = name
        self.input_type = input_type
        self.value = value

class Trigger:
    def __init__(self, path: str, inputs: List[TriggerInput]):
        self.path = path
        self.inputs = inputs

    def is_triggered(self, changed_files: List[str]) -> bool:
        for file in changed_files:
            if re.match(self.path, file):
                return True
        return False

class Deployment:
    def __init__(self, name: str, triggers: List[Trigger], parameters: dict):
        self.name = name
        self.triggers = triggers
        self.parameters = parameters

    def is_active(self, changed_files: List[str]) -> bool:
        pass

class Stage:
    def __init__(self, description: str, sequence: int, deployments: List[Deployment]):
        self.description = description
        self.sequence = sequence
        self.deployments = deployments

class Workflow:
    def __init__(self, workflow_template: str, changed_files: List[str]):
        self.stages = []
        self._generate_stages(workflow_template)
        self.stages = sorted(self.stages, key=lambda s: s.sequence)  # sort the stages
        self.changed_files = changed_files

    def _generate_stages(self, workflow_template: str):
        with open(workflow_template, 'r') as f:
            template = yaml.safe_load(f)

        for stage_template in template:
            deployments = []
            for deployment_name, deployment_data in stage_template["deployments"].items():
                triggers = []
                for trigger_data in deployment_data["triggers"]:
                    trigger_inputs = []
                    for input_name, input_data in trigger_data["inputs"].items():
                        trigger_inputs.append(TriggerInput(input_name, input_data["type"], input_data["value"]))
                    triggers.append(Trigger(trigger_data["path"], trigger_inputs))
                deployments.append(Deployment(deployment_name, triggers, parameters={}))
            stage = Stage(stage_template["description"], stage_template["sequence"], deployments)
            self.stages.append(stage)

    def process(self):
        for stage in sorted(self.stages, key=lambda s: s.sequence):
            print(f"Processing stage: {stage.description}")
            for deployment in stage.deployments:
                if deployment.is_active(self.changed_files):
                    print(f"  - Deploying {deployment.name}")
                else:
                    print(f"  - Skipping {deployment.name}")

    def to_yaml(self) -> str:
        workflow_dict = {}
        for stage in self.stages:
            stage_dict = {
                "description": stage.description,
                "deployments": {}
            }
            for deployment in stage.deployments:
                stage_dict["deployments"][deployment.name] = {
                    "parameters": deployment.parameters
                }
            workflow_dict[stage.sequence] = stage_dict

        return yaml.dump(workflow_dict)


changed_files = ["/resource_config/projects/001/nonp/iam/roles.yaml",
                 "/resource_config/projects/001/nonp/policies.yaml",
                 "/plat/p/nonp/resources/lala.yaml",
                 "/no/p/vpcsc/lala.yaml"]

workflow = Workflow('workflow_template.yaml', changed_files)

workflow.process()

print(workflow.to_yaml())
'''
for stage in workflow.stages:
    print("Stage sequence:{}".format(stage.sequence))
    for deployment in stage.deployments:
        print(deployment.name)
        #print("Deployment:".format(deployment))
        for trigger in deployment.triggers:
            print(trigger.path, trigger.is_triggered())
'''
# Pass changed files to trigger
# Pass changed files to trigger
# Pass changed files to trigger
# Pass changed files to trigger


# you must read deployment_units to validate that project_code is list_or_all and act accordingly
# for now just assume it is by default