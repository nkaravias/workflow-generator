import os
import yaml


class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            raise ValueError(f"File '{self.file_path}' does not exist.")

        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                if not isinstance(data, list):
                    raise ValueError(f"File '{self.file_path}' does not contain a valid list of file paths.")
                self.content = data
        except (yaml.YAMLError, FileNotFoundError):
            raise ValueError(f"File '{self.file_path}' is not valid YAML or could not be read.")

    @property
    def output(self):
        return self.content
