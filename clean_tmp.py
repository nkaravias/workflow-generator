import re
from typing import List


class TriggerInput:
    def __init__(self, name: str, input_type: str, value: str):
        self.name = name
        self.input_type = input_type
        self.value = value


class Trigger:
    def __init__(self, path: str, inputs: List[TriggerInput]):
        self.path = path         # the regex path of a trigger (each path has 1-* parameter inputs of scalar or regex type)
        self.inputs = inputs     # a list of TriggerInputs objects
        self.input_params = []   # the k:v pair of inputs after being processed (matched to a file)  
        self.matching_files = [] # the path of the files that have matched to a trigger path regex
        self.triggered = False

    def process(self, changed_files: List[str]) -> dict:
        for file in changed_files:
            raw_path = r"" + self.path
            match_re = re.match(raw_path, file)
            if match_re:
                print(f"Trigger path {self.path} matched with file:{file}")
                self.matching_files.append(file)
                self.triggered = True
                self.input_params.append(self.single_trigger_match_input_params(match_re))
            else:
                print(f"Trigger path {self.path} did NOT match with file:{file}")

    def single_trigger_match_input_params(self, match_re):
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

    def is_active(self, changed_files: List[str]) -> bool:
        for trigger in self.triggers:
            input_dict = trigger.get_params()
            if input_dict:
                self.parameters.update(input_dict)
                print("Adding to deployment parameters:{}".format(input_dict))
                return True
        return False

changed_files = [
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
#Testing raw strings and regex matches
normal_string = "/platform_config/projects/(\\d{3})/.*yaml"
raw_string = r"" + normal_string

changed = "/platform_config/projects/002/lala.yaml"

print(normal_string)
print(raw_string)

match = re.match(raw_string, changed)
print(match)
print(match.group(1))
'''
'''
+ for each matching file of this trigger
+ if regex
+   if project code
+     project_code = list of matches
+     (append / insert)
+     at the end of matching files, if all is in the list, set it to [all]
+ if scalar
+   if different than previous --> error
'''