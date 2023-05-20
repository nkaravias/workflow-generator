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

    workflow_template_path = "workflow_template_test.yaml"
    workflow_manager = WorkflowManager(workflow_template_path, changed_files)
    workflow = workflow_manager.generate_workflow()

    print(workflow.to_yaml())


# TODO 
# [DONE] Make sure if someone sets a match group that doesn't match, index error is caught
# Validate the workflow_template
# [DONE] Test more than one trigger before doing this
# Accept changed files as an input
# Add a logger instead of print with default output to output.log
# Add cli with verbosity

