import re
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
        self.matching_files = []
        self.triggered = False

    def process(self, changed_files: List[str]) -> dict:
        '''
            If the trigger.path matches with any file in the changed_files list
            1) set triggered = True
            2) process all trigger inputs
        '''
        for file in changed_files:
            # Convert to raw string so we don't have to escape all the backslashes
            # for the path string
            raw_path = r"" + self.path
            if re.match(raw_path, file):
                print(f"Trigger path {self.path} matched with file:{file}")
                self.matching_files.append(file)
                self.triggered = True
            else:
                print(f"Trigger path {self.path} did NOT match with file:{file}")
        
    def get_params(self) -> dict:
        if self.matching_files:
            raw_path = r"" + self.path
            print("matching files for {}:{}".format(self.path, self.matching_files))
            input_dict = {}
            for input_param in self.inputs:
                if input_param.input_type == 'scalar':
                    input_dict[input_param.name] = input_param.value
                elif input_param.input_type == 'regex_match_group':
                    #print(self.matching_files)
                    #print(self.matching_files[0])
                    #print(self.matching_files)
                    #print(self.matching_files[0])
                    match = re.match(raw_path, self.matching_files[0])
                    input_dict[input_param.name] = match.group(int(input_param.value))
                    input_dict[input_param.name] = match.group(1)
            return input_dict
        else:
            return {}

'''        
    def get_params(self):  
        print(self.matching_files)  
        if self.matching_files:
            print("these files matched:{}".format(self.matching_files))
            input_dict = {}
            for input_param in self.inputs:
                input_dict[input_param.name] = input_param.value
            return input_dict
        else:
            return {}
'''

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

'''
    def is_triggered(self, changed_files: List[str]) -> bool:
        matching_files = [file for file in changed_files if re.match(self.path, file)]
        if matching_files:
            print(f"Trigger path {self.path} matched with files:")
            for file in matching_files:
                print(f"- {file}")
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
changed_files = [#"/resource_config/projects/001/nonp/iam/roles.yaml",
#                 "/resource_config/projects/001/nonp/policies.yaml",
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
#    print(trigger.path)
#    for input in trigger.inputs:
#        print(input.name, input.input_type, input.value)
#    print(trigger.matching_files)
    trigger.process(changed_files)
#    print(trigger.matching_files)
    print(trigger.get_params())

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