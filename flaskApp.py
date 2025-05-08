from flask import Flask, jsonify, request


app = Flask(__name__)

# lets create a mock dictionary of some events

events = [
    {
        'id' : 1,
        'name' : 'Radiohead',
        'venue' : 'colston hall',
        'date' : '2025-06-01'
    },
    {
        'id' : 2,
        'name' : 'Slum Village',
        'venue' : 'SWX',
        'date' : '2025-05-20'

    }
]

@app.route("/") # decorator defines url which runs the function below
def hello_world():
    return "Hello, World!"

@app.route("/<name>") # decorator stores a variable, name
def hello(name):
    return f"Hello {name}"

@app.route("/events", methods=['GET', 'POST'])
def get_events():
    if request.method == 'POST':
        new_event = request.get_json()
        new_event['id'] = len(events) + 1
        events.append(new_event)
        return jsonify(new_event), 201
    return jsonify(events)