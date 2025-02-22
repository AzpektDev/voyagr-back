from flask import Flask, request, jsonify
from flights_api import search_flights, prepare_flight_search_response

app = Flask(__name__)

@app.route('/log-name', methods=['POST'])
def log_name():
    try:
        data = request.get_json()
        name = data.get('name')
        
        if not name:
            return jsonify({'error': 'No name provided'}), 400
            
        print(f"Received name from ElevenLabs agent: {name}")
        
        return jsonify({'success': True, 'message': f'Logged name: {name}'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

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
