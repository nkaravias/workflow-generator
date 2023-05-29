import pytest
import os

from workflow import Workflow
from stage import Stage
from deployment import Deployment
from trigger import Trigger

@pytest.fixture
def sample_workflow():
    # Create a sample workflow for testing
    workflow = Workflow([])  # Initialize with an empty list of changed files
    stage1 = Stage("Stage 1", 1)
    stage2 = Stage("Stage 2", 2)

    deployment1 = Deployment("Deployment1", [])
    deployment2 = Deployment("Deployment2", [])

    trigger1 = Trigger("path1", [])
    trigger2 = Trigger("path2", [])

    deployment1.triggers.append(trigger1)
    deployment2.triggers.append(trigger2)

    stage1.add_deployment(deployment1)
    stage2.add_deployment(deployment2)

    workflow.add_stage(stage1)
    workflow.add_stage(stage2)

    return workflow


def test_workflow_to_yaml():
    workflow = Workflow([])  # Empty list of changed files

    stage1 = Stage("Stage 1", 1)
    deployment1 = Deployment("Deployment1", [])
    stage1.add_deployment(deployment1)
    workflow.add_stage(stage1)

    expected_yaml_output = '''- deployments:
    Deployment1:
      active: false
  description: Stage 1
  sequence: 1
'''
    actual_yaml_output = workflow.to_yaml()

    #print("Expected YAML Output:")
    #print(expected_yaml_output)
    #print("Actual YAML Output:")
    #print(actual_yaml_output)

    assert actual_yaml_output == expected_yaml_output


