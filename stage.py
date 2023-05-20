from deployment import Deployment


class Stage:
    def __init__(self, description: str, sequence: int):
        self.description = description
        self.sequence = sequence
        self.deployments = []

    def add_deployment(self, deployment: Deployment):
        self.deployments.append(deployment)