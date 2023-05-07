
'''
#Testing raw strings and regex matches
normal_string = "/platform_config/projects/(\\d{3})/.*yaml"
raw_string = r"" + normal_string

changed = "/platform_config/projects/002/lala.yaml"

print(normal_string)
print(raw_string)

match = re.match(raw_string, changed)
print(match)
print(match.group(1))
'''
'''
+ for each matching file of this trigger
+ if regex
+   if project code
+     project_code = list of matches
+     (append / insert)
+     at the end of matching files, if all is in the list, set it to [all]
+ if scalar
+   if different than previous --> error
'''