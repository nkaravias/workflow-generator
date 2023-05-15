#from trigger_processor import Deployment as deployment, Trigger, TriggerInput
#from typing import List

for stage in workflow.stages:
    print(f"Stage: {stage.description}")
    for deployment in stage.deployments:
        deployment.is_active(changed_files)
        print(f"Deployment: {deployment.name}")
        print(f"Deployment params: {deployment.parameters}")
        for trigger in deployment.triggers:
            #print(f"Trigger: {trigger.path}")
            pass
            for input_param in trigger.inputs:
                #print(f"Input: {input_param.name} ({input_param.input_type}): {input_param.value}")
                pass