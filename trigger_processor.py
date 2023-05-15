import re
import yaml
from typing import List


class TriggerInput:
    def __init__(self, name: str, input_type: str, value: str):
        self.name = name
        self.input_type = input_type
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value} ({self.input_type})"


class Trigger:
    def __init__(self, path: str, inputs: List[TriggerInput]):
        self.path = path         # the regex path of a trigger (each path has 1-* parameter inputs of scalar or regex type)
        self.inputs = inputs     # a list of TriggerInputs objects
        self.input_params = []   # the k:v pair of inputs after being processed (matched to a file) 
        # [{service_tier="nonp", project_code="003"}
        # {service_tier="nonp", project_code="002"}] 
        self.matching_files = [] # the path of the files that have matched to a trigger path regex
        self.triggered = False



    def process(self, changed_files: List[str]) -> dict:
        '''
            If the trigger.path matches with any file in the changed_files list
            1) set triggered = True
            2) process all trigger inputs
+ for each matching file of this trigger
+ if regex
+   if project code
+     project_code = list of matches
+     (append / insert)
+     at the end of matching files, if all is in the list, set it to [all]
+ if scalar
+   if different than previous --> error
        '''
        for file in changed_files:
            # Convert to raw string so we don't have to escape all the backslashes
            # for the path string
            raw_path = r"" + self.path
            match_re = re.match(raw_path, file)
            if match_re:
                #print(f"Trigger path {self.path} matched with file:{file}")
                self.matching_files.append(file)
                self.triggered = True
                self.input_params.append(self.get_params(match_re))
            else:
                print(f"Trigger path {self.path} did NOT match with file:{file}")

    def get_params(self, match_re):
        ''' For a matched file, process the template trigger inputs
        Return a map with { input_1_name: input1_1_value ... n }
        if the input type is scalar just return input_value as is
        if its a regex, return the value of the match group (which is the input_value)
        '''
        input_dict = {}
        for input_param in self.inputs:
            if input_param.input_type == 'scalar':
                input_dict[input_param.name] = input_param.value
            elif input_param.input_type == 'regex_match_group':
                input_dict[input_param.name] = match_re.group(int(input_param.value))
        return input_dict

class Deployment:
    def __init__(self, name: str, triggers: List[Trigger]):
        self.name = name
        self.triggers = triggers
        self.parameters = {}
        self.active = False


    def is_active(self, changed_files: List[str]) -> bool:
        active_triggers = []  # List to store the input parameters of active triggers

        # Process all triggers and collect input parameters of active triggers
        for trigger in self.triggers:
            trigger.process(changed_files)
            parameters_list = trigger.input_params
            if parameters_list:
                active_triggers.extend(parameters_list)

        # If no active triggers found, return False
        if not active_triggers:
            return False

        # Process the input parameters of active triggers
        parameters = self.process_parameters(active_triggers)

        # Update the deployment parameters with the processed parameters
        self.parameters.update(parameters)

        return True

    def process_parameters(self, active_triggers: List[dict]) -> dict:
        parameters = {}
        project_codes = set()

        for params in active_triggers:
            for key, value in params.items():
                if key == "project_code":
                    project_codes.add(value)
                elif key in parameters:
                    # Check if a different value is detected for a parameter in active triggers
                    if parameters[key] != value:
                        raise ValueError(f"Different values detected for parameter '{key}' in active triggers.")
                else:
                    # Add the parameter to the deployment parameters
                    parameters[key] = value

        # Update the 'project_code' parameter with comma-separated values
        parameters["project_code"] = ",".join(project_codes)

        return parameters





'''    
    def is_active(self, changed_files: List[str]) -> bool:
        parameters_list = []  # Accumulate input parameters from all triggers
        for trigger in self.triggers:
            trigger.process(changed_files)
            parameters_list.extend(trigger.input_params)
            if trigger.input_params:
                self.active = True
                print(trigger.input_params)

        # Update the parameters dictionary with the accumulated input parameters
        for param in parameters_list:
            #print(param)
            self.parameters.update(param)
'''
'''
    def is_active(self, changed_files: List[str]) -> bool:
        for trigger in self.triggers:
            trigger.process(changed_files)
            parameters_list = trigger.input_params
            print(parameters_list)
            if parameters_list:
                self.parameters.update(parameters_list)
                print("Adding to deployment parameters:{}".format(parameters_list))
                return True
        return False
'''

'''
    def is_triggered(self, changed_files: List[str]) -> bool:
        path_regex = re.compile(self.path)
        for file in changed_files:
            if path_regex.match(file):
                return True
        return False
'''
'''
changed_files = ["/resource_config/projects/001/nonp/iam/roles.yaml",
                 "/resource_config/projects/001/nonp/policies.yaml",
                 "/resource_config/projects/002/nonp/core.yaml",
                 "/platform_config/projects/nonp/resources/lala.yaml",
                 "/platform_config/org/vpc_service_controls/access.yaml",
                 "/platform_config/org/vpc_service_controls/nonp/internal.yaml"
                 ]
'''


'''
changed_files = [#"/resource_config/projects/001/nonp/iam/roles.yaml",
                 "/resource_config/projects/001/nonp/policies.yaml",
                 "/platform_config/projects/006/koko.yaml",
                 "/platform_config/projects/002/lala.yaml"
                 ]

trigger_inputs = []
stier = TriggerInput(name='service_tier', input_type='scalar', value='nonp')
scode = TriggerInput(name='project_code', input_type='scalar', value='001')
rtier = TriggerInput(name='service_tier',
                     input_type='regex_match_group', value=1)
rcode = TriggerInput(name='project_code',
                     input_type='regex_match_group', value=1)
trigger_inputs.append(stier)
trigger_inputs.append(rcode)

triggers = []
paths = {}
paths["n001"] = "/resource_config/projects/001/nonp/policies.yaml"
paths["nonp-project"] = "/resource_config/projects/(.*)/nonp/policies.yaml"
#paths["plat-tier"] = "/platform_config/projects/(.*)/*.yaml"
paths["plat-tier"] = "/platform_config/projects/(\\d{3})/.*.yaml"
#triggers.append(Trigger(paths["n001"], trigger_inputs))
#triggers.append(Trigger(paths["nonp-project"], trigger_inputs))
triggers.append(Trigger(paths["plat-tier"], trigger_inputs))

for trigger in triggers:
    trigger.process(changed_files)
    print("Matched files: {}".format(trigger.matching_files))
    print("Trigger inputs: {}".format(trigger.input_params))
    #print(trigger.get_params())

#deployments = []
#deployments.append(Deployment("deployment_name", triggers))
#deployments[0].is_active(changed_files)
#print("{} params = {}".format(deployments[0].name, deployments[0].parameters))
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
deployment.is_active(changed_files)
print(deployment.parameters)


# TODO 
# Make sure if someone sets a match group that doesn't match, index error is caught

# Glue everything together and generate deployments now that we're getting params
# Test more than one trigger before doing this


#with open(workflow_template, 'r') as f:
#    template = yaml.safe_load(f)
#
#deployments = []
#for deployment_name, deployment_data in stage_template["deployments"].items():
#    triggers = []
#    for trigger_data in deployment_data["triggers"]:
#        trigger_inputs = []
#        for input_name, input_data in trigger_data["inputs"].items():
#            trigger_inputs.append(TriggerInput(input_name, input_data["type"], input_data["value"]))
#        triggers.append(Trigger(trigger_data["path"], trigger_inputs))
#    deployments.append(Deployment(deployment_name, triggers, parameters={}))
#stage = Stage(stage_template["description"], stage_template["sequence"], deployments)
#self.stages.append(stage)