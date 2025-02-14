'''
This script will be used to update the Raspberry Pi using crontab
'''

import subprocess

result = subprocess.run(["git", "pull"], capture_output=True, text=True)
print(result.stdout)
