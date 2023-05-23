from workflow_manager import WorkflowManager

if __name__ == "__main__":
    changed_files = [
        "/resource_config/projects/001/nonp/abc.yaml",
        "/resource_config/projects/002/nonp/xyz.yaml",
        "/platform_config/projects/003/nonp/123.yaml",
        "/platform_config/projects/004/nonp/test.yaml",
        "/platform_config/projects/006/test/secret.yaml",
        "/platform_config/org/lala.yaml"
    ]

    workflow_template_path = "../workflow_template_test.yaml"
    workflow_manager = WorkflowManager(workflow_template_path, changed_files)
    workflow = workflow_manager.generate_workflow()

    print(workflow.to_yaml())


'''
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

print(workflow.to_yaml())

'''

# TODO 
# Make sure if someone sets a match group that doesn't match, index error is caught
# Validate the workflow_template
# Test more than one trigger before doing this
# Accept changed files as an input
# Add a logger instead of print with default output to output.log
# Add cli with verbosity

