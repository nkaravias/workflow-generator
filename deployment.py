from typing import List
from trigger import Trigger


class Deployment:
    def __init__(self, name: str, triggers: List[Trigger]):
        self.name = name
        self.triggers = triggers
        self.parameters = {}
        self.active = False


    def process(self, changed_files: List[str]) -> bool:
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
        
        self.active = True
        return True

    def process_parameters(self, active_triggers: List[dict]) -> dict:
        ''' processes a list of parameter dictionaries that have been triggered 
            and updates the parameters dictionary of the deployment

            e.g [{'project_code': '003', 'service_tier': 'nonp', 'environment': 'dev'}, {'project_code': '001'}]
            becomes {'project_code': '001,003', 'service_tier': 'nonp', 'environment': 'dev'}
        '''
        # TODO in theory we should be reading deployment_units.yaml and catching the type of each input parameter in that deployment
        # TODO that way we can apply if "all" type logic in where applicable (e.g project_code parameters)

        parameters = {}
        project_codes = set()
        has_inputs = False  # Track if the deployment has any input parameters
        for params_dict in active_triggers:
            if params_dict:
                has_inputs = True  # Set the flag to True since there are input parameters
                for key, value in params_dict.items():
                    if key == "project_code":
                        project_codes.add(value)
                    elif key in parameters:
                        if parameters[key] != value:
                            raise ValueError(f"Scalar value mismatch detected for parameter '{key}' in active triggers.")
                    else:
                        parameters[key] = value

        if not has_inputs:
            return {}  # Return an empty dictionary if there are no input parameters
        # Otherwise add to the comma separated 
        parameters["project_code"] = ",".join(project_codes)

        return parameters