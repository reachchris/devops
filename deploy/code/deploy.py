from flask import Flask, jsonify, request, json
import os, requests
from slack import WebClient
from google.cloud import secretmanager
app = Flask(__name__)
cricket_equiments = [
   {'id': 0,
   'item': 'Cricket Bat',
   'company': 'Goldfinch',
   'brand': 'English Willow grade 1',
   'Price': '3000'},
   {'id': 1,
   'item': 'Cricket Bat',
   'company': 'SS',
   'brand': 'English Willow grade 2',
   'Price': '2500'},
   {'id': 2,
   'item': 'Cricket Helmet',
   'company': 'Gray Nicolls',
   'brand': 'Master Series',
   'Price': '780'}
]
def project_id():
   id = None
   try:
      with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')) as f:
         id = json.load(f)['project_id']
   except Exception:
      id = os.getenv('PROJECT_ID')

   if not id:
      raise Exception('Project ID not set')

   return id
def access_secret_version(secret_id, version_id='latest'):
   client = secretmanager.SecretManagerServiceClient()
   name = client.secret_path(project_id(), secret_id)
   response = client.access_secret_version(request={"name": name})
   return response.payload.data.decode('UTF-8')

def slack_messsage(post):
   r = requests.post(
      access_secret_version('slack-url/versions/latest'),
      data=json.dumps(post),
      headers={'Content-Type': 'application/json'}
   )
   if r.status_code != 200:
      raise request.ConnectionError
   return "Channel Notified"
@app.route('/helloworld')
def hello_world():
   return 'Hello World'

@app.route('/deploy/<module>/')
def deploy(module):
   return handle_deploy(module)

def handle_deploy(module):
   return 'Deploying {}'.format(module)

@app.route('/api/v1/resources/inventoryList', methods=['GET'])
def api_all():
   return jsonify(cricket_equiments)

@app.route('/api/v1/resources/equipment', methods=['GET'])
def api_name():
      if 'name' in request.args:
         name = request.args['name']
      else:
            return "Error: No Name provided. Please search with a valid name"
      results = []
      for equipment in cricket_equiments:
         if equipment['item'] == name:
            results.append(equipment)
      return jsonify(results)

@app.route('/api/v1/notify/channel', methods=['GET'])
def notify_channel():
   post = {
      'text': "Deployment Invoked on Master",
      "color": "#36a64f",
   }
   return slack_messsage(post)
@app.route('/api/v1/notify/user', methods=['GET'])
def notify_user():
   slack_token = access_secret_version('returns-bot-user-token/versions/latest')
   im_channel = access_secret_version('slack-user/versions/latest')
   slack_client = WebClient(slack_token)
   msg_blocks = [
      {
         "type": "section",
         "text":
         {
            "type": "mrkdwn",
            "text": "*Deployment Status on Dev*"
         }
      },
      {
         "type": "divider",
         "block_id": "divider1"
      }
   ]
   msg_attachments = [
      {
         "mrkdwn_in": ["text"],
         "color": "#36a64f",
         "fields": [
            {"title": "Branch", "value": "github_branch_name", "short": True},
            {"title": "Repository", "value": "github_repo_name", "short": True},
            {"title": "Project", "value": "github_project", "short": True},
            {"title": "User ID", "value": im_channel, "short": True},
         ]
      },
      {
         "title": "Modules Passing",
         "color": "#36a64f",
         "fields": [
               {"title": "Plan", "value": ' Modules Passed ', "short": True},
               {"title": "Apply", "value": ' Modules Passed ', "short": True},
         ]
      },
      {
         "title": "Modules Failing",
         "color": "danger",
         "fields": [
               {"title": "Plan", "value": ' Modules Failed ', "short": True},
               {"title": "Apply", "value": ' Modules Failed ', "short": True},
         ]
      },
   ]
   slack_client.api_call( 'chat.postMessage',
   json={
            'channel': im_channel,
            'blocks': msg_blocks,
            'attachments': msg_attachments
         }
   )
   return "Message Sent"

if __name__ == '__main__':
   app.run(host ='0.0.0.0', port=os.getenv('PORT'), debug = True)