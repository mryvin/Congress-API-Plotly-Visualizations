from flask import Flask, jsonify
from flask_cors import CORS
from members import get_member_info_graph, get_member_name_graph, get_member_party_graph, get_member_state_graph, get_member_leg_count_graph

app = Flask(__name__)
CORS(app)

### Member Information

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to FiveFortyOne Visuals!"})

@app.route('/members/info', methods=['GET'])
def member_info():
    return get_member_info_graph()

@app.route('/members/names', methods=['GET'])
def member_names():
    return get_member_name_graph()

@app.route('/members/party', methods=['GET'])
def member_party():
    return get_member_party_graph()

@app.route('/members/state', methods=['GET'])
def member_state():
    return get_member_state_graph()

@app.route('/members/leg_count', methods=['GET'])
def member_leg_count():
    return get_member_leg_count_graph()

if __name__ == '__main__':
    app.run(debug=True, port=1089)
