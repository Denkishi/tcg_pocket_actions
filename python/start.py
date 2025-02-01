import requests
import json
import os

token = os.environ["TOKEN"]
params = {
  "api_key": token,
  "offset": "0",
  "limit": "20",
  "include_options": "1"
}
r = requests.get('https://www.parsehub.com/api/v2/projects', params=params)
data=json.loads(r.text)
#print(data["total_projects"])
proj_num=(data["total_projects"]) #numero progetti
i = 0
while i < proj_num:
    title = data["projects"][i]["title"]
    project_token = data["projects"][i]["token"]
    latest_run = None

    if data["projects"][i]["last_ready_run"] is not None:
        latest_run = data["projects"][i]["last_ready_run"]["run_token"]

    if latest_run is None:
        project_token_string = "https://www.parsehub.com/api/v2/projects/" + project_token + "/run"
        requests.post(project_token_string, data=params)
    else:
        run_token_string = "https://www.parsehub.com/api/v2/runs/" + latest_run
        requests.delete(run_token_string, params=params)
        project_token_string = "https://www.parsehub.com/api/v2/projects/" + project_token + "/run"
        requests.post(project_token_string, data=params)
    i += 1

