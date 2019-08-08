import random
import string
from datetime import datetime

import requests


def random_string(string_length=6, additional_text=""):
    letters_and_digits = string.ascii_letters + string.digits
    return additional_text + ''.join(random.choice(letters_and_digits) for _ in range(string_length))


def generate_url(name):
    url = name.replace(" ", "-").replace("_", "-")
    id = random_string(string_length=4)
    return f"{id}-{url}"


def save_statistics(json, db):
    from models import StatRecord, StatSlice
    timestamp = datetime.utcnow()
    user_id = json[0]['practice']['hacker_id']
    stat_slice = StatSlice(user_id=user_id, timestamp=timestamp)
    db.session.add(stat_slice)
    db.session.commit()

    java_stat_record = None
    sql_stat_record = None
    for track in json:
        practice = track.get('practice')
        if practice:
            score = practice.get('score')
        if track['slug'] == 'java':
            java_stat_record = StatRecord(skill_id=8, skill_level=score, stat_slice_id=stat_slice.id)
            db.session.add(java_stat_record)
        if track['slug'] == 'sql':
            sql_stat_record = StatRecord(skill_id=11, skill_level=score, stat_slice_id=stat_slice.id)
            db.session.add(sql_stat_record)
    JOIN_TABLES_REQUEST = """INSERT INTO statistics (skill_id, skill_level, stat_slice_id, timestamp, user_id, team_id)
                SELECT sr.skill_id, sr.skill_level, sr.stat_slice_id, ss.timestamp, ss.user_id, t.id FROM stat_record sr
                JOIN stat_slice ss ON sr.stat_slice_id = ss.id
                JOIN user u ON ss.user_id = u.id
                JOIN team t ON u.team_id = t.id"""
    db.session.commit()

    db.session.execute(JOIN_TABLES_REQUEST)
    db.session.commit()
