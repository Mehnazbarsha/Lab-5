from flask import Flask, request, jsonify


# Define the Flask app
app = Flask(__name__)

subscribers = {}
subject = ""

def home():
  return "Hello from Flask!"

@app.route('/', methods=['GET'])
def root():
  print(f"Hello at the root")
  return jsonify({'main endpoint':'Ack'})

@app.route('/list-subscribers', methods=['GET'])
def listSubscribers():
  print(f"Listing all subscribers (count: {len(subscribers)})")
  return jsonify(subscribers)

# Windows> curl.exe -X POST -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"URI\":\"http://good.site.com\"}" http://localhost:5000/add-subscriber

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():
  data = request.json
  if not data:
    return jsonify({'error': 'No JSON data provided'}), 400
  
  name = data.get('name')
  URI = data.get('URI')
  
  if not name or not URI:
    return jsonify({'error': 'Both name and URI are required'}), 400
  
  subscribers[name] = URI
  print(f"You entered: Name={name}, Address={URI}")
  return jsonify({'message': f'You sent name: {name} and address: {URI}'}), 201

@app.route('/delete-subscriber', methods=['DELETE'])
def deleteSubscriber():
  data = request.json
  if not data:
    return jsonify({'error': 'No JSON data provided'}), 400
  
  name = data.get('name')
  if not name:
    return jsonify({'error': 'Name is required'}), 400
  
  if name not in subscribers:
    return jsonify({'error': f'Subscriber {name} not found'}), 404
  
  del subscribers[name]
  print(f"You deleted: Name={name}")
  return jsonify({'message': f'Deleted subscriber: {name}'})

@app.route('/update-and-notify', methods=['POST'])
def updateAndNotifyAllSubscribers():
  data = request.json
  if not data:
    return jsonify({'error': 'No JSON data provided'}), 400
  
  subject = data.get('subject-update')
  if not subject:
    return jsonify({'error': 'subject-update is required'}), 400
  
  print(f"You updated the subject to: {subject}")
  print(f"Notifying {len(subscribers)} subscriber(s)...")
  
  for key in subscribers.keys():
    print(f"  -> Notifying {key} at {subscribers[key]} of the new subject: {subject}")
  
  return jsonify({
    'message': f'You updated subject to: {subject}',
    'subscribers_notified': len(subscribers)
  })

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)