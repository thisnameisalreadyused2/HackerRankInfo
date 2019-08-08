import re

from flask import Flask, render_template, request, session, make_response, url_for, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug import exceptions
import requests

from config import Config
from Utils import random_string, generate_url

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/', methods=['GET', 'POST'])
def index_html():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        response = make_response(url_for('/team/create'))


@app.route('/team/create', methods=['POST'])
def team_create():
    team_name = request.form.get('team_name')
    email = request.form.get('email')
    password = request.form.get('password') or random_string()

    if not re.match(r"^[\wа-яіх]{2,30}$", team_name, re.IGNORECASE):
        return jsonify({'error': 'team name is required'}), 400
    if email:
        pass  # TODO: Send info to email

    url = generate_url(team_name)
    team = models.Team(url=url, name=team_name, password=password)
    db.session.add(team)
    db.session.commit()

    return redirect(f'{url}')


@app.route('/team/<team_url>', methods=['GET'])
def team_page(team_url):
    team = db.session.query(models.Team).filter_by(url=team_url).first()
    if not team:
        return jsonify({'error': 'team not found'}), 404

    return render_template('team.html', name=team.name, url=team.url, password=team.password, info_message="Success")


@app.route('/team/<team_url>/users', methods=['GET'])
def team_users(team_url):
    team = db.session.query(models.Team).filter_by(url=team_url).first()
    if not team:
        return jsonify({'error': 'team not found'}), 404
    users = db.session.query(models.User).filter_by(team_id=team.id).all()
    return jsonify([u.to_dict() for u in users])


@app.route('/team/<team_url>/users/add', methods=['POST'])
def add_user(team_url):
    team = db.session.query(models.Team).filter_by(url=team_url).first()
    if not team:
        return jsonify({'error': 'team not found'}), 404

    username = re.match(r"(^[\w]+|(?!hackerrank\.com\/)\w+)$", request.form.get('user_url'))
    if not username:
        return render_template('team.html', name=team.name, url=team.url, password=team.password, info_message="Cant parse username")
    username = username.group()

    user_info = requests.get(f'https://www.hackerrank.com/rest/hackers/{username}/scores_elo').json()
    if not user_info:
        return render_template('team.html', name=team.name, url=team.url, password=team.password, info_message="Cant find user in HackerRank")

    user_id = user_info[0]['practice']['hacker_id']

    user = models.User(id=user_id, name=username, total_score=0, team_id=team.id)
    db.session.add(user)
    db.session.commit()

    return render_template('team.html', name=team.name, url=team.url, password=team.password, info_message=f"User {username} has been added")


@app.route('/team/<team_url>/statistics', methods=['GET'])
def team_stats(team_url):
    team = db.session.query(models.Team).filter_by(url=team_url).first()
    if not team:
        return jsonify({'error': 'team not found'}), 404
    raw_statistics = db.session.query(models.Statistics).filter_by(team_id=team.id).all()
    statistics = {}
    # for record in raw_statistics:
    date_records = db.session.query(models.Statistics).distinct(models.Statistics.timestamp).group_by(models.Statistics.timestamp).all()
    for date_record in date_records:
        time = date_record.timestamp
        statistics[time] = []
        users_in_record = db.session.query(models.StatSlice).filter_by(timestamp=time).all()
        for raw_user in users_in_record:
            user_info = db.session.query(models.StatRecord).filter_by(stat_slice_id=raw_user.id).all()
            score = sum([el.skill_level for el in user_info])
            statistics[time].append({"user_id": raw_user.user_id,
                                    "score": score})

    #return jsonify([s.to_dict(only=('skill_id', 'skill_level', 'stat_slice_id', 'timestamp', 'user_id')) for s in raw_statistics])
    return jsonify(statistics)


@app.route('/skills', methods=['GET'])
def skills():
    skills = db.session.query(models.Skill).all()
    return jsonify([s.to_dict() for s in skills])


@app.errorhandler(exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('index.html', info_message='Please, enter team name')


if __name__ == '__main__':
    app.register_error_handler(400, handle_bad_request)
    app.run()
