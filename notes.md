  triggers:
    - path: "/platform_config/projects/(\\d{3})/.*.yaml"
      inputs:
        project_code:
          type: "regex_match_group"
          value: 1
        service_tier:
          type: "scalar"
          value: "nonp"


for each trigger path regex, multiple files can match, giving different inputs

for example /plat/d{3} would return

code=003 for /plat/003 and
code=002 for /plat/002

so a trigger should return

matching_files (files that matched)

input_params as a list of maps
where each map is the inputs for that file that got matched