# Workflow-generator
Generates sequential workflows off of a base template. Check test/resources for details.

```
wfgen.py 
usage: wfgen.py [-h] {workflow,trigger} ...

positional arguments:
  {workflow,trigger}

optional arguments:
  -h, --help          show this help message and exit
```

## workflow create
```
wfgen.py workflow create --help
usage: wfgen.py workflow create [-h] -o OUTPUT_FILE [-l {info,debug,warning,error,critical}] -c CHANGED_FILES_PATH -w WORKFLOW_TEMPLATE_PATH

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path to the output file
  -l {info,debug,warning,error,critical}, --log-level {info,debug,warning,error,critical}
                        Log level
  -c CHANGED_FILES_PATH, --changed-files-path CHANGED_FILES_PATH
                        Path to the changed files
  -w WORKFLOW_TEMPLATE_PATH, --workflow-template-path WORKFLOW_TEMPLATE_PATH
                        Path to the workflow template file
```

E.g
```
wfgen.py workflow create -o out.yaml -c tests/resources/git_changes.yaml --workflow-template-path tests/reso
urces/workflow_template_test.yaml
```

## workflow mock
```
wfgen.py workflow mock --help
usage: wfgen.py workflow mock [-h] -o OUTPUT_FILE [-l {info,debug,warning,error,critical}] -w WORKFLOW_TEMPLATE_PATH

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path to the output file
  -l {info,debug,warning,error,critical}, --log-level {info,debug,warning,error,critical}
                        Log level
  -w WORKFLOW_TEMPLATE_PATH, --workflow-template-path WORKFLOW_TEMPLATE_PATH
                        Path to the workflow template file
```

E.g
```wfgen.py workflow mock -o mock.yaml --workflow-template-path tests/resources/workflow_template_test.yaml
2023-05-29 11:19:22,533 - INFO - Generating new workflow
2023-05-29 11:19:22,537 - INFO - A new deployment: org
2023-05-29 11:19:22,537 - INFO - A new deployment: project_core
2023-05-29 11:19:22,537 - DEBUG - Finished adding stage This is the first stage
2023-05-29 11:19:22,537 - INFO - A new deployment: lala_core
2023-05-29 11:19:22,537 - INFO - A new deployment: org_core
2023-05-29 11:19:22,537 - INFO - A new deployment: network
2023-05-29 11:19:22,537 - DEBUG - Finished adding stage This is the second stage
2023-05-29 11:19:22,537 - INFO - A new deployment: secrets
2023-05-29 11:19:22,537 - DEBUG - Finished adding stage This is the third stage
2023-05-29 11:19:22,538 - DEBUG - Writing workflow formatted output:
```

## trigger validate-regex

```
wfgen.py trigger validate-regex --trigger-path "/platform_config/projects/(\\d{3})/.*.yaml" --changed-file "
/platform_config/projects/001/lala.yl,/platform_config/projects/006/koko.yaml"
```

```
2023-05-29 11:17:38,556 - DEBUG - Processing trigger /platform_config/projects/(\d{3})/.*.yaml
2023-05-29 11:17:38,556 - DEBUG - [TRIGGER FAIL]: Trigger path /platform_config/projects/(\d{3})/.*.yaml did NOT match with file: /platform_config/projects/001/lala.yl
2023-05-29 11:17:38,556 - DEBUG - [TRIGGER MATCH]: Trigger path /platform_config/projects/(\d{3})/.*.yaml matched with file: /platform_config/projects/006/koko.yaml
2023-05-29 11:17:38,556 - DEBUG - Calculated trigger parameter inputs: {}
```
