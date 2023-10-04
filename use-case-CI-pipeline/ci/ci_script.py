import firecrest as fc
import os
import time
import requests
import argparse
import utilities as util


# You can use this set to decide if the job has finished
final_slurm_states = {
    'BOOT_FAIL',
    'CANCELLED',
    'COMPLETED',
    'DEADLINE',
    'FAILED',
    'NODE_FAIL',
    'OUT_OF_MEMORY',
    'PREEMPTED',
    'TIMEOUT',
}

# Setup variables of the client as secrets,
# no need to change anything here
CLIENT_ID = os.environ.get("FIRECREST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FIRECREST_CLIENT_SECRET")
FIRECREST_URL = os.environ.get("FIRECREST_URL")
AUTH_TOKEN_URL = os.environ.get("AUTH_TOKEN_URL")

# Setup an argument parser for the script,
# no need to change anything here
parser = argparse.ArgumentParser()
parser.add_argument("--system", default=os.environ.get('MACHINE'), help="choose system to run")
parser.add_argument("--branch", default="main", help="branch to be tested")
parser.add_argument("--account", default="csstaff", help="branch to be tested")
parser.add_argument("--repo", help="repository to be tested")
args = parser.parse_args()
system_name = args.system
ref = args.branch
print(f"Will try to run the ci in system {system_name} on branch {ref}")

# Setup up a firecrest client
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}
response = requests.post(
    AUTH_TOKEN_URL,
    data=data,
)

if response.status_code != 200:
    print(f'Unable to authenticate!')
    exit(1)

TOKEN = response.json()["access_token"]

response = requests.get(
    url=f'{FIRECREST_URL}/status/systems',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

if response.status_code != 200:
    print(f'Unable to check !')
    exit(1)

status = "unavailable"
for system in response.json()["out"]:
    if system["system"] == system_name:
        status = system["status"]
        break

# If the status is available submit and poll every 30 secs until
# it reaches a final state
if status == "available":
    script_content = util.create_batch_script(repo=args.repo, constraint='gpu', num_nodes=2, account=args.account, custom_modules=['cray-python'], branch=ref)
    with open("submission_script.sh", "w") as fp:
        fp.write(script_content)



    # Print the filename of stdout and stderr in the console,
    # as well as their content


    # Add some sanity checks:
    # - Poll for the final result of the system and make sure it "COMPLETED"

    # Check the output with the util function that is provided
    # util.check_output(stdout_content)

else:
    print("System {system_name} is not available")
    exit(1)
