#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = Event.query.all()

    events_list = []

    for event in events:
        events_list.append({
            "id": event.id,
            "name": event.name,
            "location": event.location
        })

    return jsonify(events_list), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.get(id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    sessions_list = []

    for session in event.sessions:
        sessions_list.append({
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat() if session.start_time else None,
            "event_id": session.event_id
        })

    return jsonify(sessions_list), 200


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()

    speakers_list = []

    for speaker in speakers:
        speakers_list.append({
            "id": speaker.id,
            "name": speaker.name
        })

    return jsonify(speakers_list), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.get(id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    }), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.get(id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404
    
    speakers_list = []

    for speaker in session.speakers:
        speakers_list.append({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    })

    return jsonify(speakers_list), 200
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)