from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from enum import Enum
import datetime

app = Flask(__name__)

mongo_client = MongoClient("mongodb+srv://admin:admin@cluster0.y1e6w.mongodb.net/mchacks?retryWrites=true&w=majority")
db = mongo_client.db
entries = db.entries
worksheets = db.worksheets
moods = db.moods

class Mood(Enum):
	VERY_BAD = 0
	BAD = 1
	NEUTRAL = 2
	GOOD = 3
	VERY_GOOD = 4

	def _send_to_mongo(mood):
		post = {"date": datetime.datetime.utcnow(),
			"mood": mood.value}
		moods.insert_one(post)


class CDC(Enum):
	# TODO replace me with actual CDC options
	CDC_OPT_0 = 0
	CDC_OPT_1 = 1
	CDC_OPT_2 = 2
	CDC_OPT_3 = 3

class Journal:
	def __init__(self, entry, upload=True):
		self.journal = entry
		#self.mood = mood
		if upload:
			self._send_to_mongo()

	def _send_to_mongo(self):
		post = {"date": datetime.datetime.utcnow(),
			"journal": self.journal}
			#"mood": self.mood.value}
		entries.insert_one(post)

class Worksheet:
	def __init__(self, entry, cdc, entry1, entry2, upload=True):
		#self.mood = mood
		self.cdc = cdc
		self.entry = entry
		# TODO rename entry1, entry2
		self.entry1 = entry1
		self.entry2 = entry2
		if upload:
			self._send_to_mongo()

	def _send_to_mongo(self):
		post = {"date": datetime.datetime.utcnow(),
			"entry": self.entry,
			"entry1": self.entry1,
			"entry2": self.entry2,
			"cdc": self.cdc.value}
			#"mood": self.mood.value}
		worksheets.insert_one(post);

def journals_get_all():
	journals = [x for x in entries.find()]
	return journals

def worksheets_get_all():
	all_worksheets = [x for x in worksheets.find()]
	return all_worksheets

def moods_get_all():
	all_moods = [x for x in moods.find()]
	return all_moods

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

@app.route("/journal", methods=['POST', 'GET'])
def journal_page():
	if request.method == "GET":
		return render_template("journal.html")
	mood = int(request.form['mood'])
	entry = request.form['journal']
	mood = Mood(mood)
	Journal(entry, mood)
	return redirect('/journal')

@app.route("/worksheet", methods=['POST', 'GET'])
def worksheet_page():
	if request.method == "GET":
		return render_template("journal.html")
	mood = int(request.form['mood'])
	entry = request.form['journal']
	# TODO rename entry1, entry2
	entry1 = request.form['entry1']
	entry2 = request.form['entry2']
	cdc = int(request.form['cdc'])
	mood = Mood(mood)
	cdc = CDC(cdc)
	Worksheet(entry, mood, cdc, entry1, entry2)
	return redirect('/worksheet')


if __name__ == "__main__":
	app.run(debug=True)
