import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime


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

    # Get channel_name and username from the channelForm
    ch = request.form.get("channel")
    ch_creator = request.form.get("username")

    # Check if channel exists
    if channel_exists(ch):
        return jsonify({"success": False})

    # If channel does not exist, append it to channels list
    if not channel_exists(ch):
        channel = {
            "channel_name": ch,
            "channel_creator": ch_creator,
            "channel_members": [],
            "channel_messages": ["msg_1", "msg_2", "msg_3"]
        }
        channels.append(channel)

    return jsonify({
        "success": True,
        "channel_name": channel['channel_name'],
        "channel_creator": channel['channel_creator']})


@app.route("/get_channels", methods=["POST"])
def get_channels():

    # If no channel in channels, return False
    if len(channels) is 0:
        return jsonify({"success": False})

    # Else, return channels
    return jsonify({"success": True, "channels": channels})


@app.route("/join_channel", methods=["POST"])
def join_channel():

    # Get the corresponding info from the form submitted
    username = request.form.get("username")
    channelToBeJoined = request.form.get("channelToBeJoined")

    for c in channels:
        # If channel exists
        if c['channel_name'] == channelToBeJoined:
            # Append info to that channel
            c['channel_members'].append({"member": username, "join_time": datetime.now()})
            channelJoined = c
            return jsonify({"success": True, "channel_joined": channelJoined})

    return jsonify({"success": False})


@app.route("/get_channel_messages", methods=["POST"])
def get_channel_messages(channel):

    # Ensure the channel provided exists
    if not channel_exists(channel):
        # Return false
        return jsonify({"success": False})

    # Get that channel from channels list
    for c in channels:
        if c['channel_name'] == channel:
            # Get messages from that channel
            channel_messages = ch['channel_messages']
            print(channel_messages)
            return jsonify({"success": True, "channel_messages": channel_messages})

    return jsonify({"success": False})


@socketio.on("submit message")
def message(data):
    message = data["message"]
    channel_name = data["channel_name"]
    # Append the message to messages
    channels['channel_name']['channel_messages'].append(message)
    print(message)
    print(channel_name)
    emit("announce message", {"message": message}, broadcast=True)


def channel_exists(channel):
    for c in channels:
        if c['channel_name'] == channel:
            return True
    return False
