from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Guests, Episodes, Appearances

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shows.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Late-show API!"

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episodes.query.all()
    return jsonify([e.to_dict() for e in episodes])



@app.route('/episodes/<int:id>' , methods=['GET'])
def get_episode(id):
    episode = Episodes.query.get(id)
    if episode:
        return jsonify(episode.to_dict_with_appearances())
    return jsonify({"error": "Episode not found"}), 404


@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guests.query.all()
    return jsonify([g.to_dict(rules=("-appearances",)) for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()

    try:
        new_appearance = Appearances(
            rating=data['rating'],
            guest_id=data['guest_id'],
            episode_id=data['episode_id']
        )
        db.session.add(new_appearance)
        db.session.commit()

        return jsonify(new_appearance.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)



