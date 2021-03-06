from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from enum import Enum
import datetime
import matplotlib.pyplot
import matplotlib.dates

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
	ALL_OR_NOTHING_THINKING = 0
	OVERGENERALIZATION = 1
	MENTAL_FILTERS = 2
	DISCOUNTING_THE_POSITIVE = 3
	JUMPING_TO_CONCLUSIONS = 4
	MAGNIFYING = 5
	EMOTIONAL_REASONING = 6
	SHOULD_STATEMENTS = 7
	LABELING = 8
	PERSONALIZATION = 9
	FILTERING = 10
	POLARIZED_THINKING = 11
	CONTROL_FALLICIES = 12
	FALLACY_OF_FAIRNESS = 13
	BLAMING = 14
	HEAVENS_REWARD_FALLACY = 15





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

@app.route("/Mood/<mood_id>", methods=['POST', 'GET'])
def mood(mood_id):
	Mood._send_to_mongo(Mood(int(mood_id)))
	return redirect('/')

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

@app.route("/analyze", methods=['POST', 'GET'])
def analitty():
	if request.method == "GET":
		return render_template("analytics.html")
	return redirect('/analyze')

@app.route("/journal0", methods=['POST', 'GET'])
def journal_page0():
	if request.method == "GET":
		return render_template("journal 0.html")
	return redirect('/journal0')

@app.route("/journal1", methods=['POST', 'GET'])
def journal_page1():
	if request.method == "GET":
		return render_template("journal1.html")
	return redirect('/journal1')

@app.route("/journal2", methods=['POST', 'GET'])
def journal_page2():
	if request.method == "GET":
		return render_template("journal2.html")
	return redirect('/journal2')

@app.route("/journal3", methods=['POST', 'GET'])
def journal_page3():
	if request.method == "GET":
		return render_template("journal3.html")
	return redirect('/journal3')

@app.route("/journal4", methods=['POST', 'GET'])
def journal_page4():
	if request.method == "GET":
		return render_template("journal4.html")
	return redirect('/journal4')

@app.route("/journal/<page_id>", methods=['POST', 'GET'])
def journal_mood_x(page_id):
	if request.method == "POST":
		entry = request.form['message']
		mood = Mood(int(page_id))
		Journal(entry, mood)
		return redirect('/')
	return redirect('/')

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

@app.route("/analytics", methods=['POST', 'GET'])
def analytics_page():
	if request.method == "GET":
		all_moods = moods_get_all()
		times = [x['date'] for x in all_moods]
		mood_vals = [x['mood'] for x in all_moods]
		dates = matplotlib.dates.date2num(times)
		matplotlib.pyplot.figure(figsize=(8, 6))
		matplotlib.pyplot.plot_date(dates, mood_vals, 'b-')
		matplotlib.pyplot.yticks([0, 1, 2, 3, 4])
		matplotlib.pyplot.ylabel("Mood")
		matplotlib.pyplot.xlabel("Time")
		matplotlib.pyplot.savefig("./static/mood-graph.png")

		all_journals = sorted(journals_get_all(), key=lambda j: j['date'], reverse=True)
		for e in all_journals:
			e['date'] = e['date'].strftime("%c")
		# display worksheets?
		#all_worksheets = sorted(worksheets_get_all(), key=lambda w: w['date'])
		return render_template("analytics.html", journals=all_journals)
	return redirect("/analytics.html")


if __name__ == "__main__":
	app.run(debug=True)
