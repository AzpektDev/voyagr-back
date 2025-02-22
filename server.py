from flask import Flask, request, jsonify
from flights_api import search_flights, prepare_flight_search_response
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
        flight_search_response = prepare_flight_search_response(flights['best_flights'])

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
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
