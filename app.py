import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
CORS(app)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/partyGameDb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywwrreehkrldkm:26f8fc64055af96448159aa161df42fbd4d762b0b0545e24e8f42713b21274bf@ec2-46-137-156-205.eu-west-1.compute.amazonaws.com:5432/d2eqo77v5v3rri'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ActionCardDeck(db.Model):
    __tablename__ = 'ActionCardDeck'
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(20), unique=True)

    def __init__(self, card):
        self.card = card


class CharacterCardDeck(db.Model):
    __tablename__ = 'CharacterCardDeck'
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(20), unique=True)

    def __init__(self, card):
        self.card = card


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


@app.route('/getAllActionCard')
def getAllActionCard():
    cards = ActionCardDeck.query.all()
    results = [
        {"result": card.card} for card in cards
    ]
    return {'card': results}


@app.route('/getActionCard')
def getActionCard():
    cardCount = db.session.query(ActionCardDeck).count()
    randomNum = random.randint(1, cardCount)
    selectedCard = ActionCardDeck.query.get(randomNum)
    return {"result": selectedCard.card}


@app.route('/')
def index():
    return "<h1>Party Games API server.</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
