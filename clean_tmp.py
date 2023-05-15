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
        self.matching_files = [] # the path of the files that have matched to a trigger path regex
        self.triggered = False



    def process(self, changed_files: List[str]) -> dict:
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

    def is_active(self, changed_files: List[str]) -> bool:
        parameters_list = []  # Accumulate input parameters from all triggers
        for trigger in self.triggers:
            trigger.process(changed_files)
            parameters_list.extend(trigger.input_params)
            if trigger.input_params:
                self.active = True

        # Update the parameters dictionary with the accumulated input parameters
        for param in parameters_list:
            print(param)
            #self.parameters.update(param)

        return self.active


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

for i in trigger.inputs:
    print(i)

print(deployment.name)
print(deployment.parameters)
deployment.is_active(changed_files)
print(deployment.parameters)