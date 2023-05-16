import yaml
from typing import List

from trigger import Trigger, TriggerInput
from deployment import Deployment
from stage import Stage
from workflow import Workflow


#class TriggerInput:
#    def __init__(self, name: str, input_type: str, value: str):
#        self.name = name
#        self.input_type = input_type
#        self.value = value
#
#    def __str__(self):
#        return f"{self.name}: {self.value} ({self.input_type})"
#
#
#class Trigger:
#    def __init__(self, path: str, inputs: List[TriggerInput]):
#        self.path = path         # the regex path of a trigger (each path has 1-* parameter inputs of scalar or regex type)
#        self.inputs = inputs     # a list of TriggerInputs objects
#        self.input_params = []   # the k:v pair of inputs after being processed (matched to a file) 
#        # [{service_tier="nonp", project_code="003"}
#        # {service_tier="nonp", project_code="002"}] 
#        self.matching_files = [] # the path of the files that have matched to a trigger path regex
#        self.triggered = False
#
#
#
#    def process(self, changed_files: List[str]) -> dict:
#        '''
#            If the trigger.path matches with any file in the changed_files list
#            1) set triggered = True
#            2) process all trigger inputs
#+ for each matching file of this trigger
#+ if regex
#+   if project code
#+     project_code = list of matches
#+     (append / insert)
#+     at the end of matching files, if all is in the list, set it to [all]
#+ if scalar
#+   if different than previous --> error
#        '''
#        for file in changed_files:
#            # Convert to raw string so we don't have to escape all the backslashes
#            # for the path string
#            raw_path = r"" + self.path
#            match_re = re.match(raw_path, file)
#            if match_re:
#                print(f"Trigger path {self.path} matched with file:{file}")
#                self.matching_files.append(file)
#                self.triggered = True
#                self.input_params.append(self.get_params(match_re))
#            else:
#                print(f"Trigger path {self.path} did NOT match with file:{file}")
#
#    def get_params(self, match_re):
#        ''' For a matched file, process the template trigger inputs
#        Return a map with { input_1_name: input1_1_value ... n }
#        if the input type is scalar just return input_value as is
#        if its a regex, return the value of the match group (which is the input_value)
#        '''
#        input_dict = {}
#        for input_param in self.inputs:
#            if input_param.input_type == 'scalar':
#                input_dict[input_param.name] = input_param.value
#            elif input_param.input_type == 'regex_match_group':
#                input_dict[input_param.name] = match_re.group(int(input_param.value))
#        return input_dict
#
#class Deployment:
#    def __init__(self, name: str, triggers: List[Trigger]):
#        self.name = name
#        self.triggers = triggers
#        self.parameters = {}
#        self.active = False
#
#
#    def process(self, changed_files: List[str]) -> bool:
#        active_triggers = []  # List to store the input parameters of active triggers
#
#        # Process all triggers and collect input parameters of active triggers
#        for trigger in self.triggers:
#            trigger.process(changed_files)
#            parameters_list = trigger.input_params
#            if parameters_list:
#                active_triggers.extend(parameters_list)
#
#        # If no active triggers found, return False
#        if not active_triggers:
#            return False
#
#        # Process the input parameters of active triggers
#        parameters = self.process_parameters(active_triggers)
#
#        # Update the deployment parameters with the processed parameters
#        self.parameters.update(parameters)
#        
#        self.active = True
#        return True
#
#    def process_parameters(self, active_triggers: List[dict]) -> dict:
#        ''' processes a list of parameter dictionaries that have been triggered 
#            and updates the parameters dictionary of the deployment
#
#            e.g [{'project_code': '003', 'service_tier': 'nonp', 'environment': 'dev'}, {'project_code': '001'}]
#            becomes {'project_code': '001,003', 'service_tier': 'nonp', 'environment': 'dev'}
#        '''
#        # TODO in theory we should be reading deployment_units.yaml and catching the type of each input parameter in that deployment
#        # TODO that way we can apply if "all" type logic in where applicable (e.g project_code parameters)
#
#        parameters = {}
#        project_codes = set()
#        has_inputs = False  # Track if the deployment has any input parameters
#        for params_dict in active_triggers:
#            if params_dict:
#                has_inputs = True  # Set the flag to True since there are input parameters
#                for key, value in params_dict.items():
#                    if key == "project_code":
#                        project_codes.add(value)
#                    elif key in parameters:
#                        if parameters[key] != value:
#                            raise ValueError(f"Scalar value mismatch detected for parameter '{key}' in active triggers.")
#                    else:
#                        parameters[key] = value
#
#        if not has_inputs:
#            return {}  # Return an empty dictionary if there are no input parameters
#        # Otherwise add to the comma separated 
#        parameters["project_code"] = ",".join(project_codes)
#
#        return parameters
#    
#
#
#
#class Workflow:
#    def __init__(self, workflow_template: str, changed_files: List[str]):
#        self.stages = []
#        self.changed_files = changed_files
#
#    def add_stage(self, stage: Stage):
#        self.stages.append(stage)
#
#    def to_yaml(self) -> str:
#        workflow_dict = {}
#        for stage in self.stages:
#            stage_dict = {
#                "description": stage.description,
#                "deployments": {}
#            }
#            for deployment in stage.deployments:
#                deployment_dict = {
#                    "active": deployment.active,
#                    "parameters": deployment.parameters
#                }
#                stage_dict["deployments"][deployment.name] = deployment_dict
#            workflow_dict[stage.sequence] = stage_dict
#        return yaml.dump(workflow_dict)


def generate_workflow_from_template(workflow_template_path: str, changed_files: List[str]) -> Workflow:
    workflow = Workflow(workflow_template_path, changed_files)
    with open(workflow_template_path, 'r') as f:
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
            deployment.process(changed_files)        
            stage.add_deployment(deployment)
        workflow.add_stage(stage)

    return workflow




# Example usage
changed_files = [
    "/resource_config/projects/001/nonp/abc.yaml",
    "/resource_config/projects/002/nonp/xyz.yaml",
    "/platform_config/projects/003/nonp/123.yaml",
    "/platform_config/projects/004/nonp/test.yaml",
    "/platform_config/projects/006/test/secret.yaml",
    "/platform_config/org/lala.yaml"
]

workflow_template_path = "workflow_template_test.yaml"
workflow = generate_workflow_from_template(workflow_template_path, changed_files)

#for stage in workflow.stages:
#    for deployment in stage.deployments:
#        deployment.process(changed_files)

print(workflow.to_yaml())



'''
# Create Trigger Inputs
trigger_inputs = [
    TriggerInput("project_code", "regex_match_group", "1"),
    TriggerInput("service_tier", "scalar", "nonp"),
    TriggerInput("environment", "scalar", "dev"),
    #TriggerInput("someparam", "regex_match_group", "2")
]

# Create Trigger
trigger = Trigger("/platform_config/projects/(\\d{3})/.*.yaml", trigger_inputs)


# Create Deployment
deployment = Deployment("bob", [trigger])

# Test with changed files
changed_files = [
    "a/platform_config/projects/001/nonp/abc.yaml",
    "s/platform_config/projects/002/nonp/xyz.yaml",
    "/platform_config/projects/003/nonp/123.yaml",
    "/platform_config/projects/004/nonp/test.yaml"
]

print(deployment.name)
print(deployment.parameters)
deployment.process(changed_files)
print(deployment.parameters)
'''


# TODO 
# Make sure if someone sets a match group that doesn't match, index error is caught
# Validate the workflow_template
# Test more than one trigger before doing this
# Accept changed files as an input
# Add a logger instead of print with default output to output.log
# Add cli with verbosity

