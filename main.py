from flask import Flask, render_template, request, session, jsonify
import datetime
import components
import game_engine
import mp_game_engine

app = Flask(__name__)
app.secret_key = 'SK&sdf34JD#$h234df'
# Secret key for securing the session data.
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    if request.method == 'POST':
        data = request.json
        # Checks if the attack hits or misses, updates the session data accordingly, and returns a JSON response.
        if data is not None:
            session['placement'] = {}
            for name in data:
                session['placement'][name] = [data[name][1], data[name][0], data[name][2]]
            return jsonify({"message": "Placement received", "received_data": data}), 200
        else:
            return jsonify({"message": "No Placement received"}), 400
    return render_template('placement.html', board_size=10, ships=components.create_battleships())


@app.route('/attack', methods=['GET'])
def attack():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)
    # Checks if the attack hits or misses, updates the session data, and returns a JSON response.
    if (x, y) in session['player']['hit']:
        hit = True
    elif (x, y) in session['player']['miss']:
        hit = False
    else:
        hit = game_engine.attack((x, y), session['ai']['board'], session['ai']['ships'])
        if hit:
            session['player']['hit'].append((x, y))
        else:
            session['player']['miss'].append((x, y))
        session['player'] = session['player']
        session.modified = True

    response = {
        'hit': hit,
    }
    if components.is_all_ships_sunk(session['ai']['ships']):
        response['finished'] = "Game Over. You won!"
        return jsonify(response)

    x, y = mp_game_engine.generate_attack(len(session['player']['board']), session['ai']['level'], session['ai']['hit'],
                                          session['ai']['miss'])
    if (x, y) in session['ai']['hit']:
        pass
    elif (x, y) in session['ai']['miss']:
        pass
    else:
        ai_hit = game_engine.attack((x, y), session['player']['board'], session['player']['ships'])
        if ai_hit:
            session['ai']['hit'].append((x, y))
        else:
            session['ai']['miss'].append((x, y))
        session['ai'] = session['ai']
        session.modified = True
    response['AI_Turn'] = [y, x]

    if components.is_all_ships_sunk(session['player']['ships']):
        response['finished'] = "Game Over. AI won!"
        return jsonify(response)

    response['finished'] = False
    return jsonify(response)


def setup_ai_mode(level):
    # Sets up the game for the AI mode with the specified difficulty level.
    session['player'] = {
        'board': components.initialise_board(),
        'ships': components.create_battleships(),
        'hit': [],
        'miss': []
    }
    session['ai'] = {
        'board': components.initialise_board(),
        'ships': components.create_battleships(),
        'hit': [], 'miss': [],
        'level': level,
    }
    # Place ships
    print(session.get('placement', None))
    components.place_battleships(session['player']['board'], session['player']['ships'], algorithm='custom',
                                 placement_json=session.get('placement', None))
    components.place_battleships(session['ai']['board'], session['ai']['ships'], algorithm='random')


@app.route('/', methods=['GET'])
def root():
    setup_ai_mode(2)
    return render_template('main.html', player_board=session['player']['board']) 

if __name__ == '__main__':
    app.run(debug=True, port=8888)
# Runs the Flask application in debug mode on port 8888.
