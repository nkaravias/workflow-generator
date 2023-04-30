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

    def is_triggered(self, changed_files: List[str]) -> dict:
        '''
            If the trigger.path matches with any file in the changed_files list
            1) set triggered = True
            2) process all trigger inputs
        '''
        for file in changed_files:
            if re.match(self.path, file):
                print(f"Trigger path {self.path} matched with file:{file}")
                self.matching_files.append(file)
                self.triggered = True
            else:
                print(f"Trigger path {self.path} did NOT match with file:{file}")
        if self.matching_files:
            input_dict = {}
            for input_param in self.inputs:
                input_dict[input_param.name] = input_param.value
            return input_dict
        else:
            return None


class Deployment:
    def __init__(self, name: str, triggers: List[Trigger]):
        self.name = name
        self.triggers = triggers
        self.parameters = {}

    #def is_active(self, changed_files: List[str]) -> bool:
    #    pass

    def is_active(self, changed_files: List[str]) -> bool:
        for trigger in self.triggers:
            input_dict = trigger.is_triggered(changed_files)
            if input_dict:
                self.parameters.update(input_dict)
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
trigger_inputs.append(scode)

triggers = []
paths = {}
paths["n001"] = "/resource_config/projects/001/nonp/policies.yaml"
paths["nonp-project"] = "/resource_config/projects/(.*)/nonp/policies.yaml"
paths["plat-tier"] = "/platform_config/projects/(.*)/*.yaml"
#triggers.append(Trigger(paths["n001"], trigger_inputs))
#triggers.append(Trigger(paths["nonp-project"], trigger_inputs))
triggers.append(Trigger(paths["plat-tier"], trigger_inputs))

for trigger in triggers:
    print(trigger.path)
    for input in trigger.inputs:
        print(input.name, input.input_type, input.value)
    print(trigger.matching_files)
    #print(trigger.is_triggered(changed_files))
    #if trigger.is_triggered(changed_files) == True:
    #    print(f"SUMMARY: trigger path {trigger.path} matched with files:{trigger.matching_files}")

deployments = []
deployments.append(Deployment("deployment_name", triggers))
deployments[0].is_active(changed_files)
print(deployments[0].parameters)