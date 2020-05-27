import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
import random

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://adpfowzkleeitp:96ccb53cb09065e05c77ee8ef0e64bc26c8fd3d9b7eb4f0fb9fdd9427431a1cb@ec2-46-137-100-204.eu-west-1.compute.amazonaws.com:5432/d2gcilbhceanps'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GameStore(db.Model):
    __tablename__ = 'GameStore'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    path = db.Column(db.String())

    def __init__(self, title, description, path):
        self.title = title
        self.description = description
        self.path = path


class GameMode(db.Model):
    __tablename__ = 'GameMode'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    mode = db.Column(db.String(50))
    description = db.Column(db.String(1000))

    def __init__(self, mode, description):
        self.mode = mode
        self.description = description


class ActionCardDeck(db.Model):
    __tablename__ = 'ActionCardDeck'
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(50), unique=True)

    def __init__(self, card):
        self.card = card


class CharacterCardDeck(db.Model):
    __tablename__ = 'CharacterCardDeck'
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(50), unique=True)

    def __init__(self, card):
        self.card = card


# class GameSession(db.Model):
#     __tablename__ = 'GameSession'
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     code = db.Column(db.String(8), unique=True, default=str(uuid4)[:8])

#     def __init__(self, code, players):
#         self.code = code


@app.route('/getAllGames')
def getAllGames():
    queryResult = GameStore.query.all()
    games = [
        {
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "path": game.path
        } for game in queryResult
    ]
    return {'result': games}


@app.route('/getGameModes')
def getGameModes():
    queryResult = GameMode.query.all()
    modes = [
        {
            "id": mode.id,
            "mode": mode.mode,
            "description": mode.description
        } for mode in queryResult
    ]
    return {'result': modes}


@app.route('/getAllActionCards')
def getAllActionCard():
    queryResult = ActionCardDeck.query.all()
    cards = [
        {
            "id": card.id,
            "card": card.card
        } for card in queryResult
    ]
    return {'result': cards}


@app.route('/addActionCard', methods=['POST'])
def addActionCard():
    card = request.form['card']
    if card == '':
        return {'result': 'Error: An action is required.'}
    if db.session.query(ActionCardDeck).filter(ActionCardDeck.card == card).count() == 0:
        data = ActionCardDeck(card)
        db.session.add(data)
        db.session.commit()
        return {'result': 'An action card is added successfully.'}


@app.route('/getActionCard')
def getActionCard():
    cardCount = db.session.query(ActionCardDeck).count()
    randomNum = random.randint(1, cardCount)
    selectedCard = ActionCardDeck.query.get(randomNum)
    return {"result": selectedCard.card}


@app.route('/getAllCharacterCards')
def getAllCharacterCard():
    queryResult = CharacterCardDeck.query.all()
    cards = [
        {
            "id": card.id,
            "card": card.card
        } for card in queryResult
    ]
    return {'result': cards}


@app.route('/getCharacterCard')
def getCharacterCard():
    cardCount = db.session.query(CharacterCardDeck).count()
    randomNum = random.randint(1, cardCount)
    selectedCard = CharacterCardDeck.query.get(randomNum)
    return {"result": selectedCard.card}


@app.route('/')
def index():
    return "<h1>Party Games API server.</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
