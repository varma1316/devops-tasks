
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request
app=Flask(__name__)
@app.route("/createjira",methods=["POST"])
def createjira():
    git_data=request.get_json(force=True)
    if git_data["comment"]["body"]!="/jira.com":
        return "Not a Jira trigger", 200 
    url = "https://yourdomain.atlassian.net/rest/api/3/issue"
    
    auth = HTTPBasicAuth("example@gmail.com", "<api_token>")
    
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    
    payload = json.dumps({
        "fields": {
            "project": { "key": "SCRUM" },     # or use "id" if you prefer
            "summary": git_data["issue"]["title"],
            "issuetype": { "id": "10003" },    # could be "Task", "Story", etc.
             "description": {
      "content": [
        {
          "content": [
            {
              "text": git_data["issue"]["body"],
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    }
        }
    })
    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth
    )
    
    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
app.run('0.0.0.0')
