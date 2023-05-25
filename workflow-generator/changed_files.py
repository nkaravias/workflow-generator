import os
import yaml

class ChangedFiles:
    ''' More of a plaholder for now '''
    def __init__(self, file_path):
        self.file_path = file_path
        self._validate_file()

    def _validate_file(self):
        if not os.path.exists(self.file_path):
            raise ValueError(f"File '{self.file_path}' does not exist.")

        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                if not isinstance(data, list):
                    raise ValueError(f"File '{self.file_path}' does not contain a valid list of file paths.")
                self.file_paths = data
        except (yaml.YAMLError, FileNotFoundError):
            raise ValueError(f"File '{self.file_path}' is not valid YAML or could not be read.")

    @property
    def output(self):
        return self.file_paths
