from flask import Flask, render_template, request

import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('settings.json') as f:
        settings = json.load(f)
    return render_template('index.html', **settings)


@app.route('/candidate/<int:id>')
def bio(id):
    with open('candidates.json') as f:
        candidates = json.load(f)
    for candidate in candidates:
        if candidate['id'] == id:
            return render_template('candidate.html', **candidate)


@app.route('/list')
def candidates_list():
    with open('candidates.json') as f:
        candidates = json.load(f)

    return render_template('candidates_list.html', candidates=candidates)


@app.route('/search/')
def search_candidate():
    name = request.args.get('name')
    with open('candidates.json') as f:
        candidates = json.load(f)
    with open('settings.json') as f:
        settings = json.load(f)
    people = []
    for candidate in candidates:
        if not settings["case-sensitive"]:
            if name in candidate['name'].lower():
                people.append(candidate['name'])
                return render_template('search_name.html', people=people, total=len(people))
        else:
            if name in candidate['name']:
                people.append(candidate['name'])
                return render_template('search_name.html', people=people, total=len(people))

    return render_template('search_name.html', people=people, total=len(people))


@app.route('/skill/<skill>')
def search_skill(skill):
    with open('candidates.json') as f:
        candidates = json.load(f)
    with open('settings.json') as f:
        settings = json.load(f)
    people = []
    total = 0
    for candidate in candidates:
        if skill in candidate['skills'].lower():
            people.append(candidate['name'])
            total += 1
            if settings['limit'] == total:
                return render_template('skill.html', people=people, total=len(people))

    return render_template('skill.html', people=people, total=len(people))


app.run()
