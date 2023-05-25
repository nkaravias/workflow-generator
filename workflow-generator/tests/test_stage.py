from stage import Stage
from deployment import Deployment

def test_stage_add_deployment():
    stage = Stage("Test Stage", 1)
    deployment = Deployment("Test Deployment", [])
    
    stage.add_deployment(deployment)
    
    assert len(stage.deployments) == 1
    assert stage.deployments[0] is deployment
    assert stage.deployments[0].name == "Test Deployment"

   # raise ValueError("KAKAKAKAKAKKAOOOO:{}".format(stage.sequence))

