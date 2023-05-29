import pytest
import os

from workflow_manager import WorkflowManager

@pytest.fixture
def workflow_manager_instance():
    # Create a sample WorkflowManager for testing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_template_path = os.path.join(current_dir, 'resources', 'workflow_template_test.yaml')
    changed_files = [ "/resource_config/projects/001/nonp/abc.yaml",
                     "/resource_config/projects/002/nonp/xyz.yaml",
                     "/platform_config/projects/003/nonp/123.yaml",
                     "/platform_config/projects/004/nonp/test.yaml",
                     "/platform_config/projects/006/test/secret.yaml",
                     "/platform_config/org/lala.yaml"]
    return WorkflowManager(workflow_template_path, changed_files)

@pytest.fixture
def workflow_to_yaml_output():
    return r'''- deployments:
    org:
      active: true
      matches:
      - files:
        - /resource_config/projects/002/nonp/xyz.yaml
        pattern: /resource_config/projects/002/nonp/xyz.yaml
      parameters: {}
    project_core:
      active: true
      matches:
      - files:
        - /platform_config/projects/003/nonp/123.yaml
        - /platform_config/projects/004/nonp/test.yaml
        - /platform_config/projects/006/test/secret.yaml
        pattern: /platform_config/projects/(\d{3})/.*.yaml
      - files:
        - /resource_config/projects/001/nonp/abc.yaml
        - /resource_config/projects/002/nonp/xyz.yaml
        pattern: /resource_config/projects/(\d{3})/nonp/.*.yaml
      parameters:
        environment: dev
        project_code: all
        service_tier: nonp
  description: This is the first stage
  sequence: 1
- deployments:
    lala_core:
      active: true
      matches:
      - files:
        - /platform_config/projects/004/nonp/test.yaml
        pattern: /platform_config/projects/(004)/nonp/test.yaml
      parameters:
        project_code: '004'
    network:
      active: false
    org_core:
      active: true
      matches:
      - files:
        - /platform_config/org/lala.yaml
        pattern: /platform_config/org/lala.yaml
      parameters: {}
  description: This is the second stage
  sequence: 2
- deployments:
    secrets:
      active: true
      matches:
      - files:
        - /platform_config/projects/006/test/secret.yaml
        pattern: /platform_config/projects/006/.*.secret.yaml
      parameters:
        project_code: '006'
  description: This is the third stage
  sequence: 3
'''

def test_generate_workflow(workflow_manager_instance,  workflow_to_yaml_output):
    # Generate the workflow using the WorkflowManager
    actual_workflow = workflow_manager_instance.generate_workflow()
    #print("Expected YAML Output:")
    expected_workflow = workflow_to_yaml_output
    #print("Actual YAML Output:")
    #print(actual_workflow.to_yaml())
    assert actual_workflow.to_yaml() == expected_workflow
