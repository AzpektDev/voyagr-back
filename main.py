import psycopg2
import os
from psycopg2 import Error
from flask import Flask, request, jsonify
import uuid
import json  # Import the json module
from flights_api import search_flights, manual_prepare_flight_search_response
from dotenv import load_dotenv  # Import load_dotenv
from flask_cors import CORS  # Import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

try:
    connection = psycopg2.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'), 
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )

    cursor = connection.cursor()
    print("Connected to PostgreSQL database!")

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id UUID PRIMARY KEY,
        selected_flight JSONB
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        conversation_id UUID,
        flight_data JSONB,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    );
    """)
    connection.commit()

    @app.route('/open-conversation', methods=['POST'])
    def open_conversation():
        generated_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO conversations (id) VALUES (%s)", (generated_id,))
        connection.commit()
        return jsonify({"conversation_id": generated_id})

    @app.route('/get-conversation', methods=['GET'])
    def get_conversation():
        conversation_id = request.args.get('conversation_id')
        if not conversation_id:
            return jsonify({"error": "Invalid or missing conversation_id"}), 400

        cursor.execute("SELECT selected_flight FROM conversations WHERE id = %s", (conversation_id,))
        conversation = cursor.fetchone()
        if not conversation:
            return jsonify({"error": "Invalid or missing conversation_id"}), 400

        cursor.execute("SELECT flight_data FROM flights WHERE conversation_id = %s", (conversation_id,))
        flights = cursor.fetchall()
        flights = [flight[0] for flight in flights]

        return jsonify({"selected_flight": conversation[0], "flights": flights})

    @app.route('/search-flights', methods=['GET'])
    def search_flights_route():
        try:
            conversation_id = request.args.get('conversation_id')
            if not conversation_id:
                return jsonify({"error": "Invalid or missing conversation_id"}), 400

            departure_id = request.args.get('departure_id')
            arrival_id = request.args.get('arrival_id')
            outbound_date = request.args.get('outbound_date')
            return_date = request.args.get('return_date')

            # search for flights (using google flights api)
            flights = search_flights(departure_id, arrival_id, outbound_date, return_date)

            # parse and prepare the response with AI
            flight_search_response = manual_prepare_flight_search_response(flights['best_flights'])

            # store them in the database
            for flight in flight_search_response:
                # Convert the flight dictionary to a JSON string
                flight_json = json.dumps(flight)
                cursor.execute("INSERT INTO flights (conversation_id, flight_data) VALUES (%s, %s)", (conversation_id, flight_json))
            connection.commit()

            return jsonify({
                "flights": flight_search_response
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/select-choice', methods=['POST'])
    def select_choice():
        try:
            data = request.get_json()
            conversation_id = data.get("conversation_id")
            if not conversation_id:
                return jsonify({"error": "Invalid or missing conversation_id"}), 400

            preferred_flight_index = data.get("preferred_flight_index")
            if not isinstance(preferred_flight_index, int):
                preferred_flight_index = int(preferred_flight_index)

            cursor.execute("SELECT flight_data FROM flights WHERE conversation_id = %s", (conversation_id,))
            flights_data = cursor.fetchall()
            flights_data = [flight[0] for flight in flights_data]

            try:
                selected_flight = flights_data[preferred_flight_index]
            except (IndexError, TypeError):
                return jsonify({"error": "Invalid flight index"}), 400

            # Convert the selected flight dictionary to a JSON string
            selected_flight_json = json.dumps(selected_flight)

            # Update the selected flight in the conversation
            cursor.execute("UPDATE conversations SET selected_flight = %s WHERE id = %s", (selected_flight_json, conversation_id))
            connection.commit()

            # Check if the update was successful
            cursor.execute("SELECT selected_flight FROM conversations WHERE id = %s", (conversation_id,))
            updated_flight = cursor.fetchone()
            if updated_flight is None:
                app.logger.error("Failed to update the selected flight in the database.")
                return jsonify({"error": "Failed to update the selected flight in the database."}), 500

            return jsonify({
                "message": "Flight selected successfully",
                "selected_flight": selected_flight
            })
        except Exception as e:
            app.logger.error(f"Error in select_choice: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5001)

finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
