import yaml
from typing import List

from trigger import Trigger, TriggerInput
from deployment import Deployment
from stage import Stage
from workflow import Workflow


class WorkflowManager:
    def __init__(self, workflow_template_path: str, changed_files: List[str]):
        self.workflow_template_path = workflow_template_path
        self.changed_files = changed_files

    def generate_workflow(self) -> Workflow:
        workflow = Workflow(self.workflow_template_path, self.changed_files)
        with open(self.workflow_template_path, 'r') as f:
            template = yaml.safe_load(f)

        for stage_template in template:
            stage = Stage(stage_template["description"], stage_template["sequence"])
            for deployment_name, deployment_data in stage_template["deployments"].items():
                triggers = []
                for trigger_data in deployment_data["triggers"]:
                    trigger_inputs = []
                    for input_name, input_data in trigger_data["inputs"].items():
                        trigger_inputs.append(TriggerInput(input_name, input_data["type"], input_data["value"]))
                    triggers.append(Trigger(trigger_data["path"], trigger_inputs))
                deployment = Deployment(deployment_name, triggers)
                deployment.process(self.changed_files)
                stage.add_deployment(deployment)
            workflow.add_stage(stage)

        return workflow