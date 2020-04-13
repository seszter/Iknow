from flask import Flask, session, render_template, request, redirect, url_for
from random import randint

### Globals ###

app = Flask(__name__)
app.secret_key = '9*TGIKi7tggkuyUPJKdY%W^$WKLHOyjv,liIUFL>N>'

### Service / Utility Methods ###

def parsenum (s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@app.route("/setup", methods=['GET'])
def setup():
    if 'players' not in session:
        session['players'] = []
    if session['start_game'] == '1':
        return redirect(url_for('index'))
    session['turn'] = 1
    session['grid'] = [["empty","empty","empty","empty","empty","empty"]]
    session['grid_nums'] = [1,1,2,2,3,3]
    session['grid_plus'] = [["empty","empty","empty","empty","empty","empty"]]
    session['grid_minus'] = [["empty","empty","empty","empty","empty","empty"]]
    return render_template('setup.html',players=session['players']);


@app.route("/setup", methods=['POST'])
def update_setup():
    colors = ['lime','purple','orange','yellow','aqua', 'red']
    session['start_game'] = request.form['ready']

    session['players'].append({'pl_name':request.form['player_name'],
                                'pl_color':colors[len(session['players'])],
                                'pl_score':0})
    if session['start_game']=='0':
        return redirect(url_for('setup'))
    else:
        return redirect(url_for('index'))

@app.route("/restart")
def restart():
    session['start_game'] = '0'
    del session['players']
    return redirect(url_for('setup'))

@app.route("/", methods=['GET'])
def index():
    if not 'players' in session:
        return redirect(url_for('setup'))

    session['next_player'] = session['players'][session['turn'] % len(session['players'])]
    return render_template('index.html',
                           grid=session['grid'],
                           grid_plus = session['grid_plus'],
                           grid_minus = session['grid_minus'],
                           players = session['players'],
                           next_player = session['next_player'],
                           turn = session['turn'],
                           grid_nums = session['grid_nums'])

@app.route("/", methods=['POST'])
def update():
    session['turn'] += 1
    try:
        session['grid'][0][parsenum(request.form['play'])] = session['next_player']['pl_color']
    except:
        pass
    try:
        session['grid_plus'][0][parsenum(request.form['play_plus'])] = session['next_player']['pl_color']
    except:
        pass
    try:
        session['grid_minus'][0][parsenum(request.form['play_minus'])] = session['next_player']['pl_color']
    except:
        pass
    session['next_player'] = session['players'][session['turn'] % len(session['players'])]

    return render_template('index.html',
                           grid=session['grid'],
                           grid_plus = session['grid_plus'],
                           grid_minus = session['grid_minus'],
                           players = session['players'],
                           next_player = session['next_player'],
                           turn = session['turn'],
                           grid_nums = session['grid_nums'])
                           #win = 1)


@app.route("/evaluate")
def evaluate():
    return render_template('evaluate.html',
                           grid=session['grid'],
                           grid_plus = session['grid_plus'],
                           grid_minus = session['grid_minus'],
                           players = session['players'],
                           next_player = session['next_player'],
                           turn = session['turn'],
                           grid_nums = session['grid_nums'])
                           #win = session['win'])

@app.route("/evaluate", methods=['POST'])
def update_evaluate():
    goodgs = []
    for pl in session['players']:
        try:
            gg = request.form[pl['pl_name']]
            gg_index = session['grid'][0].index(pl['pl_color'])
            pl['pl_score'] += gg_index // 2 + 1
            goodgs.append(gg_index)
        except:
            pass

    for pl in session['players']:
        if pl['pl_color'] in session['grid_plus'][0]:
            plus_index = session['grid_plus'][0].index(pl['pl_color'])
            if plus_index in goodgs:
                pl['pl_score'] += 1
            else:
                pl['pl_score'] -= 1
        else:
            minus_index = session['grid_minus'][0].index(pl['pl_color'])
            if minus_index in goodgs:
                pl['pl_score'] -= 1
            else:
                pl['pl_score'] += 1
    session['turn'] += 1
    session['grid'] = [["empty","empty","empty","empty","empty","empty"]]
    session['grid_plus'] = [["empty","empty","empty","empty","empty","empty"]]
    session['grid_minus'] = [["empty","empty","empty","empty","empty","empty"]]
    return redirect(url_for('index'))




















