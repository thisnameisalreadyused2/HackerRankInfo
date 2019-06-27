from datetime import datetime

from app import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    password = db.Column(db.String(24))

    def __repr__(self):
        return '<Team {}:{}>'.format(self.name, self.id)


class User(db.Model):
    id = db.Column(db.Integer, index=True ,primary_key=True)
    name = db.Column(db.String(12), index=True)
    total_score = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<User {}:{}>'.format(self.name, self.id)


class StatSlice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<StatSlice {}:{}>'.format(self.id, self.user_id)


class StatRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill_level = db.Column(db.Integer)
    stat_slice_id = db.Column(db.Integer, db.ForeignKey('stat_slice.id'))

    def __repr__(self):
        return '<StatRecord {}:{}>'.format(self.skill_id, self.skill_level)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer)
    skill_level = db.Column(db.Integer)
    stat_slice_id = db.Column(db.Integer)

    timestamp = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    team_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Global stat {}>'.format(self.id)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    slug = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Skill {}:{}>'.format(self.id, self.slug)
