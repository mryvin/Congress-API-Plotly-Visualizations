from flask import Flask, jsonify  # Flask for the app, jsonify for JSON responses
from flask_cors import CORS  # Handle Cross Origin Resource Sharing
# Import the functions from the members module
from members import (
    get_member_info_graph,
    get_member_name_graph,
    get_member_party_graph,
    get_member_state_graph,
    get_member_leg_count_graph,
)

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    # Enable CORS for the app
    CORS(app)

    # Define the routes for the application

    # Route for the welcome message
    @app.route('/', methods=['GET'])
    def welcome():
        return jsonify({"message": "Welcome to FiveFortyOne Visuals!"})

    # Route for getting member information
    @app.route('/members/info', methods=['GET'])
    def member_info():
        return get_member_info_graph()

    # Route for getting member names
    @app.route('/members/names', methods=['GET'])
    def member_names():
        return get_member_name_graph()

    # Route for getting member party information
    @app.route('/members/party', methods=['GET'])
    def member_party():
        return get_member_party_graph()

    # Route for getting member state information
    @app.route('/members/state', methods=['GET'])
    def member_state():
        return get_member_state_graph()

    # Route for getting member legislation count
    @app.route('/members/leg_count', methods=['GET'])
    def member_leg_count():
        return get_member_leg_count_graph()

    # Return the app after setting up the routes
    return app

# Main entry point of the application
if __name__ == '__main__':
    # Create the app
    app = create_app()
    # Run the app on port 1089 with debug mode on
    app.run(debug=True, port=1089)
