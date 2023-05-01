
Trigger class
properties:
  path: "/plat/"
  inputs: [input TriggerInput]

is_triggerered()

TriggerInput:
  name: 
  type:
  value

is_triggered()

Deployment:`
  name:
  triggers: [trigger Trigger]
  
is_active()


Stage:
  sequence: int
  deployments: [deployment Deployment]

Workflow(workflow_template, changed_files):
  stages: [stage Stage]

  The TriggerInput class. It has a name, a type and a value. The type can be either "scalar" or "regex_match_group". If the type is "scalar" the value must be a string. If the type is "regex_match_group", the value must be an integer.

  The Trigger class. It has a path property (string) and an inputs property. The inputs property is a list of one to many TriggerInput objects. The Trigger class also has an is_triggered() method.

  The Deployment class. It has a name property and a triggers property. The triggers property is a list of one to many Trigger objects. The Deployment class also has a is_active() method.

  The Stage class. It han a sequence property (integer) and a deployments property. The deployments property is a list of Deployment objects.

    The workflow class access a workflow_template argument (which has the contents of the workflow_template.yaml file) and a changed_files argument that is the contents of the changed_files list. 


a deployment unit has many triggers

A trigger is triggered if its path regex matches a file that changed

A deployment has expected paramters (in deployment_units) - the generator doesn't know this yet

if a trigger is triggered (path matches with any file in changed_files):
  set triggered = True
  add the file that matched to matched_files
  for each of its input parameters:
    if its scalar, 

project_core deployment has one trigger:
lets say trigger is /resource/projects/(\\d{3})/.*.yaml

changed_files=
res/project/001/lala.yaml
res/project/002/koko.yaml


trigger is triggered
matching files = 
res/project/001/lala.yaml
res/project/002/koko.yaml

trigger has one regex input 
lets say trigger is /resource/projects/(\\d{3})/.*.yaml


for each matching file of this trigger
if regex
  if project code
    project_code = list of matches
    (append / insert)
    at the end of matching files, if all is in the list, set it to [all]
if scalar
  if different than previous --> error









