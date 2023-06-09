import re
from typing import List

from logger import workflow_logger


class TriggerInput:
    def __init__(self, name: str, input_type: str, value: str):
        self.name = name
        self.input_type = input_type
        self.value = value
        #workflow_logger.debug(f"A new trigger input: {self.name} {self.input_type}, {self.value}")

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
        #workflow_logger.info(f"Creating trigger for path: {self.path}")
        #workflow_logger.debug(f"A new trigger: {self.path}")


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
        workflow_logger.debug(f"Processing trigger {self.path}")
        for file in changed_files:
            # Convert to raw string so we don't have to escape all the backslashes
            # for the path string
            raw_path = r"" + self.path
            match_re = re.match(raw_path, file)
            if match_re:
                workflow_logger.debug(f"[TRIGGER MATCH]: Trigger path {self.path} matched with file: {file}")
                self.matching_files.append(file)
                self.triggered = True
                try:
                    self.input_params.append(self.get_params(match_re))
                except ValueError as e:
                    raise ValueError(f"Error processing trigger path '{self.path}' for file '{file}': {str(e)}")                    
            else:
                workflow_logger.debug(f"[TRIGGER FAIL]: Trigger path {self.path} did NOT match with file: {file}")

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
                try:
                    group_index = int(input_param.value)
                    if group_index < 0 or group_index > match_re.lastindex:
                        raise ValueError(f"Invalid match group index {group_index} in trigger input '{input_param.name}' of trigger path '{self.path}'")
                    input_dict[input_param.name] = match_re.group(group_index)
                except ValueError:
                    raise ValueError(f"Invalid match group index '{input_param.value}' in trigger input '{input_param.name}' of trigger path '{self.path}'")
        workflow_logger.debug(f"Calculated trigger parameter inputs: {input_dict}")
        return input_dict