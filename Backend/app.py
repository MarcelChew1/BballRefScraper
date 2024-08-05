from flask import Flask, request, jsonify
from flask_cors import CORS
from Player import Player
app = Flask(__name__)
CORS(app)

players = {}

@app.route('/create_player', methods=['POST'])
def create_player():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    player = Player(first_name, last_name)
    if player.url_name is None:
        return None
    
    players[player.url_name] = player
    print(players)
    
    return jsonify({
        'player_name': player.url_name,
    })

@app.route('/player', methods=['GET'])
def handle_player_request():
    name = request.args.get("name")
    type = request.args.get("type")
    print(name, type)
    if not all([name, type]):
        return jsonify({"error": "Missing data"}), 400
    
    player = players.get(name, None)
    if player == None:
        return jsonify({"error": "Missing player"}), 400
    
    player_overview = player.season

    method_map = {
        "Per game": player_overview.per_game_info,
        "Total": player_overview.total_info,
        "Per minute": player_overview.per_minute_info,
        "Per possession": player_overview.per_poss_info,
        "Advanced": player_overview.advanced_info,
        "Adjusted Shooting": player_overview.adj_shooting_info,
        "Play by play": player_overview.play_by_play_info,
        "Shooting": player_overview.shooting_info,
        "Career highs": player_overview.highs_info,
        "Playoffs": player_overview.playoff_series_info
    }

    if type in method_map:
        df = method_map[type]()
        column_order = df.columns.tolist()  # Get column order from DataFrame
        data = df.to_dict(orient='records')
        print(column_order)
        print(data)

        return jsonify({"data": data, "columnsOrder": column_order})
    else:
        return jsonify({"error": "Invalid action"}), 400


if __name__ == '__main__':
    app.run(debug=True)