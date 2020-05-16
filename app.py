import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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


class CardDeck(db.Model):
    __tablename__ = 'cardDeck'
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(20), unique=True)

    def __init__(self, card):
        self.card = card


@app.route('/addCard', methods=['POST'])
def addCard():
    card = request.form['card']
    if card == '':
        return {'result': 'Error: An action is required.'}
    if db.session.query(CardDeck).filter(CardDeck.card == card).count() == 0:
        data = CardDeck(card)
        db.session.add(data)
        db.session.commit()
        return {'result': 'An action card is added successfully.'}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
