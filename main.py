from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from enum import Enum
import datetime

app = Flask(__name__)

mongo_client = MongoClient()
db = mongo_client.db
entries = db.entries
worksheets = db.worksheets

class Mood(Enum):
	VERY_BAD = 0
	BAD = 1
	NEUTRAL = 2
	GOOD = 3
	VERY_GOOD = 4

class CDC(Enum):
	CDC_OPT_0 = 0
	CDC_OPT_1 = 1
	CDC_OPT_2 = 2
	CDC_OPT_3 = 3

class Journal:
	def __init__(self, entry, mood, upload=True):
		self.journal = entry
		self.mood = mood
		if upload:
			self._send_to_mongo()

	def _send_to_mongo(self):
		post = {"date": datetime.datetime.utcnow(),
			"journal": self.journal,
			"mood": self.mood.value}
		entries.insert_one(post)

class Worksheet:
	def __init__(self, entry, mood, cdc, entry1, entry2, upload=True):
		self.mood = mood
		self.cdc = cdc
		self.entry = entry
		self.entry1 = entry1
		self.entry2 = entry2
		if upload:
			self._send_to_mongo()

	def _send_to_mongo(self):
		post = {"date": datetime.datetime.utcnow(),
			"entry": self.entry,
			"entry1": self.entry1,
			"entry2": self.entry2,
			"cdc": self.cdc.value,
			"mood": self.mood.value}
		worksheets.insert_one(post);

def journals_get_all():
	journals = [x for x in entries.find()]
	return journals

def worksheets_get_all():
	all_worksheets = [x for x in worksheets.find()]
	return all_worksheets

@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == "GET":
		return render_template("index.html")
	name = request.form['name']
	email = request.form['email']
	message = request.form['message']
	print("name: {}\nemail: {}\nmessage: {}".format(name, email, message))
	return redirect('/')
	#journal = Journal("abcdef", Mood.VERY_BAD)
	#print(journals_get_all())

if __name__ == "__main__":
	app.run(debug=True)
