from flask import Flask, request, jsonify
from flights_api import search_flights, prepare_flight_search_response, manual_prepare_flight_search_response
import uuid

app = Flask(__name__)

SEARCH_RESULTS_STORE = {}

@app.route('/search-flights', methods=['GET'])
def search_flights_route():
    try:
        departure_id = request.args.get('departure_id')
        arrival_id = request.args.get('arrival_id')
        outbound_date = request.args.get('outbound_date')
        return_date = request.args.get('return_date')

        # search for flights (using google flights api)
        flights = search_flights(departure_id, arrival_id, outbound_date, return_date)

        # parse and prepare the response with AI
        # flight_search_response = prepare_flight_search_response(flights['best_flights'])
        flight_search_response = manual_prepare_flight_search_response(flights['best_flights'])

        search_id = str(uuid.uuid4())

        # store them so we can reference them again when user picks
        flight_data = flight_search_response
        SEARCH_RESULTS_STORE[search_id] = flight_data


        return jsonify({
            "search_id": search_id,
            "flights": flight_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/select-choice', methods=['POST'])
def select_choice():
    try:
        data = request.get_json()
        search_id = data.get("search_id")
        preferred_flight_index = data.get("preferred_flight_index")

        if not search_id or search_id not in SEARCH_RESULTS_STORE:
            return jsonify({"error": "Invalid or missing search_id"}), 400

        flights_data = SEARCH_RESULTS_STORE[search_id]

        try:
            selected_flight = flights_data[preferred_flight_index]
        except (IndexError, TypeError):
            return jsonify({"error": "Invalid flight index"}), 400

        # Do something with the selected flight, e.g. confirm booking or pass it on to another system
        # For now, we’ll just return it as a success response
        return jsonify({
            "message": "Flight selected successfully",
            "selected_flight": selected_flight
        })
    except Exception as e:
        app.logger.error(f"Error in select_choice: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
