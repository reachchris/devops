from flask import Flask, jsonify, request
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

@app.route('/helloworld')
def hello_world():
   return 'Hello World'

@app.route('/notify/<channel_type>')
def notify(channel_type):
   return handle_notify(channel_type)

def handle_notify(channel_type):
    return 'Notifying {}'.format(channel_type)

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

if __name__ == '__main__':
   app.run(host ='0.0.0.0', port = 5001, debug = True)