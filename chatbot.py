#!/usr/bin/python3
import os
import aiml
from flask import Flask
from flask import render_template

BRAIN_FILE="brain.dump"

kernel = aiml.Kernel()

# To increase the startup speed of the bot it is
# possible to save the parsed aiml files as a
# dump. This code checks if a dump exists and
# otherwise loads the aiml from the xml files
# and saves the brain dump.
if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    kernel.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    kernel.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    kernel.saveBrain(BRAIN_FILE)

# Endless loop which passes the input to the bot and prints
# its response
app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/<query>")
def api(query):
	return kernel.respond(query)


if __name__ == "__main__":
	app.run(debug=True)