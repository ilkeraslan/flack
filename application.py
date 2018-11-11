import os

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# List for channel storage
channels = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_channel", methods=["POST"])
def create_channel():

    # Query for channel name
    ch = request.form.get("channel")

    # Loop channels to see if channel name exists
    channel_exists = False
    for c in channels:
        if c['channel_name'] == ch:
            channel_exists = True
            return jsonify({"success": False})

    # If channel does not exist, append it to channels list
    if not channel_exists:
        channel = {"channel_name": ch, "channel_creator": "unknown"}
        channels.append(channel)

    return jsonify({
        "success": True,
        "channel_name": channel['channel_name'],
        "channel_creator": channel['channel_creator']})
