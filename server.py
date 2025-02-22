from flask import Flask, request, jsonify
from flights_api import search_flights, prepare_flight_search_response

app = Flask(__name__)

@app.route('/search-flights', methods=['GET'])
def search_flights_route():
    try:
        departure_id = request.args.get('departure_id')
        arrival_id = request.args.get('arrival_id')
        outbound_date = request.args.get('outbound_date')
        return_date = request.args.get('return_date')

        flights = search_flights(departure_id, arrival_id, outbound_date, return_date)
        flight_search_response = prepare_flight_search_response(flights['best_flights'])
        return jsonify(flight_search_response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
