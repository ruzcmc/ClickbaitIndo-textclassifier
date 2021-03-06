# import library
from flask import Flask, request, jsonify, make_response

# db
from flask_sqlalchemy import SQLAlchemy

# cors
from flask_cors import CORS

# limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# env
from dotenv import load_dotenv

# others
from uuid import uuid4
from predict import predict
import os, datetime

# load env
load_dotenv()

# Flask app
app = Flask(__name__)

# allow CORS
CORS(app)

# init limiter
limiter = Limiter(
	app,
	key_func=get_remote_address,
	default_limits=["1 per minute"],
)

# db details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USERNAME', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)

# connect to db
db = SQLAlchemy(app)

# class
# user request
class UserRequest(db.Model):
	__tablename__ = "user_request"

	uuid = db.Column(db.String, primary_key=True, nullable=False)
	text = db.Column(db.String, nullable=False)
	prediction = db.Column(db.Integer, nullable=False)
	ip_address = db.Column(db.String, nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

	def __repr__(self):
		return '<UserRequest %r>' % self.uuid

# user give feedback
class PredictionFeedback(db.Model):
	__tablename__ = "prediction_feedback"

	uuid = db.Column(db.String, primary_key=True, nullable=False)
	is_correct = db.Column(db.Integer, nullable=False)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

	def __repr__(self):
		return '<PredictionFeedback %r>' % self.uuid

# router
@app.route("/")
@limiter.exempt
def main():
	return "Hi!"

@app.route("/<uuid>")
@limiter.limit("20 per minute")
def show(uuid):
	# get data
	data = UserRequest.query.filter_by(uuid=uuid).first()

	# data exists?
	if data:
		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"id": data.uuid,
					"text": data.text,
					"prediction": data.prediction,
					"timestamp": data.timestamp
				}
			),

			# send 200 OK
			200
		)
	else:
		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"message": "Data not found!",
				}
			),

			# send 404 Not Found
			404
		)

	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/<uuid>/correct")
@limiter.limit("20 per minute")
def correct(uuid):
	user_ip = request.remote_addr

	# get data
	data = UserRequest.query.filter_by(uuid=uuid, ip_address=user_ip).first()

	# data exists?
	if data:
		# save feedback
		data = PredictionFeedback(
			uuid = uuid,
			is_correct = 1
		)

		# commit
		db.session.add(data)
		db.session.commit()

		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"message": "Feedback successfully saved"
				}
			),

			# send 200 OK
			200
		)

	else:
		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"message": "Data not found!",
				}
			),

			# send 404 Not Found
			404
		)

	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/<uuid>/incorrect")
@limiter.limit("20 per minute")
def incorrect(uuid):
	user_ip = request.remote_addr

	# get data
	data = UserRequest.query.filter_by(uuid=uuid, ip_address=user_ip).first()

	# data exists?
	if data:
		# save feedback
		data = PredictionFeedback(
			uuid = uuid,
			is_correct = 0
		)

		# commit
		db.session.add(data)
		db.session.commit()

		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"message": "Feedback successfully saved"
				}
			),

			# send 200 OK
			200
		)

	else:
		# return to user
		response = make_response(
			# data
			jsonify(
				{
					"message": "Data not found!",
				}
			),

			# send 404 Not Found
			404
		)

	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/predict", methods=["POST"])
@limiter.limit("2 per minute")
def predictText():
	# ambil data
	request_data = request.get_json()

	# generate uuid dan ambil user ip dan text
	uuid = uuid4()
	text = request_data['text']
	user_ip = request.remote_addr

	# predict
	prediction = predict(text)

	# save prediction
	data = UserRequest(
		uuid = uuid,
		text = text,
		prediction = prediction,
		ip_address = user_ip
	)

	# commit
	db.session.add(data)
	db.session.commit()

	# return to user
	response = make_response(
		# data
		jsonify(
			{
				"id": uuid,
				"prediction": prediction
			}
		),

		# send 200 OK
		200
	)

	response.headers["Content-Type"] = "application/json"
	return response

# handle too much request
@app.errorhandler(429)
def handle_ratelimit(e):
	response = make_response(
		# data
		jsonify(
			{
				"message": f"Error {e.description}"
			}
		),

		# send 429 Too Many Requests
		429
	)

	response.headers["Content-Type"] = "application/json"
	return response

# run app
if __name__ == "__main__":
	app.run(host="0.0.0.0")
