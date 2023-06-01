import json
import sys
import time
from typing import List
from flask_login import current_user, login_required, login_user, logout_user
from flask_socketio import emit, join_room, leave_room, rooms, send
from app import app, socket_io, db
from flask import jsonify, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import openai
from sqlalchemy import and_
from app.models import Channel, ChannelParticipant, Message, User
from secret.secret import SECRET_KEY, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

@app.route('/')
@app.route('/index')
@login_required

def index():
    return render_template("index.html", name=current_user.username, user_id=current_user.id)


@login_required
def get_history(channel_id):
    return db.session.query(Message)\
        .filter(Message.channel_id == channel_id)\
        .all()

#TODO: remove this init, change it to render time., it is useless. 
@socket_io.on('init')
def init_connection(data):
    join_room("user:" + str(current_user.id))
    if (current_user.curr_channel):
        channel = {}
        channel['channel_id'] = current_user.curr_channel
        change_channel(channel)

# Receive a message from the front end HTML
@socket_io.on('transmit_data')
def message_recieved(data):
    # TODO: This shouldn't be able to be forged.
    # TODO: Make sure that someone is a part of channel before committing their message
    text = data['text']
    channel_id = current_user.curr_channel
    print(text, channel_id)
    if not (text and channel_id):
        return
    msg = Message(
        sender_id=current_user.id,
        channel_id=channel_id,
        text=text,
        timestamp=int(time.time_ns() / 1000000)  # UTC timestamp in ms
    )
    db.session.add(msg)
    db.session.commit()
    
    data = []
    data.append({
             'sender_name': db.session.query(User).get(msg.sender_id).username, 
             'timestamp': msg.timestamp, 
             'text': msg.text
            })
    emit('history', data, room="channel:" + str(channel_id))

    # If it starts with '/gpt', process the message
    chatGptReq = text.startswith('/gpt')
    if chatGptReq:
        # Split the message into parts
        parts = text.split(maxsplit=2)

        # If a bot username is provided, try to find it. If not, or if the bot doesn't exist, default to "ChatGPT"
        gpt_username = str(parts[1]) if len(parts) >= 2 else "ChatGPT"
        GPT_user = db.session.query(User).filter_by(username=gpt_username, is_GPT=True).first()
        
        # If no GPT user was found with the provided username, default to "ChatGPT"
        if GPT_user is None:
            GPT_user = db.session.query(User).filter_by(username="ChatGPT", is_GPT=True).first()
        # Check again if the GPT user exists (in case the default "ChatGPT" bot also doesn't exist for some reason)
        if GPT_user:
            sendGPTmessage(GPT_user.id, channel_id)

@socket_io.on('change_channel')
def change_channel(data):
    if (not data):
        emit('change_channel', room="user:"+str(current_user.id))

    channel_id = int(data['channel_id'])
    channel_name = db.session.query(Channel).get(channel_id).name

    for channel in rooms(current_user.id):
        leave_room(channel)

    x = db.session.query(ChannelParticipant)\
        .filter((ChannelParticipant.user_id == current_user.id) & (ChannelParticipant.channel_id == channel_id))\
        .first()
    if x:
        print(f"SUCCESS: User {current_user.username} changed to channel {channel_id}")
        emit('change_channel', {'success': True, 'channel_id': channel_id, 'channel_name': channel_name}, room="user:"+str(current_user.id))
        current_user.curr_channel = channel_id
        db.session.commit()
        join_room("channel:" + str(channel_id))
        message_history = get_history(channel_id)
        data = []
        for msg in message_history:
            data.append({
                 'sender_name': db.session.query(User).get(msg.sender_id).username, 
                 'timestamp': msg.timestamp, 
                 'text': msg.text})
        emit('history', data, room="user:"+str(current_user.id))
    else:
        print(f"FAIL: User {current_user.username} failed to change to channel {channel_id}")
        emit('change_channel', {'success': False})
    # emit('history', {'data': f'{current_user.username} joined'}, room=)


@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return render_template('signup.html')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/v1/channels/<int:channel_id>/users', methods=['GET'])
# grabs users in and not in channel_id
def get_users(channel_id):
    # Query to find users not in curr_channel
    subquery = db.session.query(ChannelParticipant.user_id).filter(ChannelParticipant.channel_id == channel_id).subquery()
    users_not_in_channel_query = db.session.query(User).filter(User.id.notin_(subquery))
    users_in_channel_query = db.session.query(User).filter(User.id.in_(subquery))
    
    users_not_in_channel = users_not_in_channel_query.all()
    users_in_channel = users_in_channel_query.all()

    data_not_in_channel = []
    for user in users_not_in_channel:
        data_not_in_channel.append({'id': user.id, 'username': user.username})

    data_in_channel = []
    for user in users_in_channel:
        data_in_channel.append({'id': user.id, 'username': user.username})

    data = {'not_in_channel': data_not_in_channel, 'in_channel': data_in_channel}
    return jsonify(data), 200

@app.route('/api/v1/channels/user/<int:user_id>', methods=['GET'])
# grabs users NOT IN channel_id
def get_channels(user_id):
    # Query to find users not in curr_channel
    user_channels = db.session.query(ChannelParticipant)\
                .filter(ChannelParticipant.user_id == user_id).all()
    channels = [[i.channel.id, i.channel.name] for i in user_channels]
    return jsonify(channels)

@app.route('/api/v1/channels/leave/<int:channel_id>/<int:user_id>', methods=['POST'])
# grabs users NOT IN channel_id
def leave_channel(channel_id, user_id):
    # Query to find users not in curr_channel
    cp = db.session.query(ChannelParticipant).filter(
        and_(
            ChannelParticipant.user_id == user_id,
            ChannelParticipant.channel_id == channel_id
        )
    ).first()
    data = {}
    data['success'] = False

    if cp:
        # delete the ChannelParticipant entry
        print("Removing user_id ${user_id} from channel_id ${channel_id}")
        db.session.delete(cp)
        data['success'] = True

        # check if there are no participants left in the channel
        remaining_participants = db.session.query(ChannelParticipant).filter(
            ChannelParticipant.channel_id == channel_id
        ).count()

        if remaining_participants == 0:
            print("No participants left in channel_id ${channel_id}: Deleting channel.")
            # if no participants are left, delete the channel and associated messages
            channel_to_delete = db.session.query(Channel).get(channel_id)
            if channel_to_delete:
                db.session.delete(channel_to_delete)

            messages_to_delete = db.session.query(Message).filter(
                Message.channel_id == channel_id
            ).all()

            for msg in messages_to_delete:
                db.session.delete(msg)

        # check if the user's 'curr_channel' is the channel they are being removed from
        user = db.session.query(User).get(user_id)
        print(user)
        if user and user.curr_channel == channel_id:
            print(f"User's current channel is the channel being removed. Setting 'curr_channel' to None.")
            user.curr_channel = None
            print("user:"+str(user_id))
            emit('change_channel', None, room="user:"+str(user_id), namespace='/')
            user_channels = db.session.query(ChannelParticipant)\
                        .filter(ChannelParticipant.user_id == user_id).all()
            channels = [[i.channel.id, i.channel.name] for i in user_channels]
            emit('user_channels', channels, room="user:"+str(user_id), namespace='/')
            emit("update_user_list", room="channel:"+str(channel_id), namespace='/')

    db.session.commit()
    return jsonify(data), 201


@app.route('/search')
def search():
    if current_user.is_authenticated:
        return render_template('search.html')
    else:
        return render_template('login.html')


@app.route('/api/v1/channels/', methods=['POST'])
@login_required
def create_channel():
    data = request.get_json()
    if 'name' not in list(data.keys()):
        return jsonify({'success': False, 'message': 'Must provide "name" parameter'}), 400
    name = data['name']
    channel: Channel = Channel(name=name)
    print(f"Create Channel {name=}")
    # The creator is added to the channel by default.
    db.session.add(ChannelParticipant(user_id=current_user.id, channel=channel))
    db.session.commit()
    user_channels = db.session.query(ChannelParticipant)\
                .filter(ChannelParticipant.user_id == current_user.id).all()
    channels = [[i.channel.id, i.channel.name] for i in user_channels]
    emit('user_channels', channels, room="user:"+str(current_user.id), namespace='/')
    return jsonify({'id': channel.id, 'name': channel.name}), 201

@app.route('/api/v1/bots/create', methods=['POST'])
@login_required
def create_bot():
    data = request.get_json()
    if 'name' not in list(data.keys()):
        return jsonify({'success': False, 'message': 'Must provide "name" parameter'}), 400
    if 'begin_prompt' not in list(data.keys()):
        return jsonify({'success': False, 'message': 'Must provide "begin_prompt" parameter'}), 400
    name = data['name']
    begin_prompt = "A user in a chat channel has created you, giving the following character prompt: "+data['begin_prompt']+"\n"
    bot = User(username=name, begin_prompt=begin_prompt, end_prompt="Stay in character! You are not an assistant unless the prompt explicitly states it. Users invoke you with '/gpt {your name}'. Do not include your name in replies!", is_GPT=True)
    db.session.add(bot)
    print(f"Create Bot {name=}")
    # The creator is added to the channel by default.
    db.session.commit()
    return jsonify({'id': bot.id, 'name': bot.username}), 201


# TODO: Can we use jsonschema to validate :,(

@app.route('/api/v1/channels/<int:channel_id>/users/', methods=['POST'])
@login_required
def add_users_to_channel(channel_id):
    data = request.get_json()

    if 'users' not in data or not isinstance(data['users'], (list)):
        return jsonify({'error': 'Missing required parameters'}), 400
    for user in data['users']:
        print(f"Add user {user} to channel {channel_id}")
        db.session.add(ChannelParticipant(user_id=user, channel=Channel.query.get(channel_id)))

    db.session.commit()
    #emit to all involved users that they have been added to a new channel
    for user in data['users']:
        user_channels = db.session.query(ChannelParticipant)\
                    .filter(ChannelParticipant.user_id == user).all()
        channels = [[i.channel.id, i.channel.name] for i in user_channels]
        emit('user_channels', channels, room="user:"+str(user), namespace='/')
    emit("update_user_list", room="channel:"+str(channel_id), namespace='/')
    return jsonify({'success':True, 'message':'Added users to Channel'}), 200

@app.route('/api/v1/auth/login', methods=['POST'])
def login_post():
    if not current_user.is_authenticated:
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing required parameters'}), 400

        user: User = db.session.query(User).filter(User.email == email).first()
        if user is not None and check_password_hash(user.password_hash, password):
            login_user(user=user)
            return jsonify({'message': 'Logged in', 'status': 200}), 200
        else:
            return jsonify({'error': 'authentication_failed', 'message': 'Password incorrect or user does not exist.', 'status': 403}), 403


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if not email or not username or not password:
        return jsonify({'error': 'Missing required parameters'}), 400

    errors = []
    if db.session.query(User).filter((User.username == username)).first():
        app.logger.error(f"Could not create user {email=} {username=}: user exists.")
        errors.append({'error': 'username_exists', "message": "Username is taken."})
    if db.session.query(User).filter((User.email == email)).first():
        app.logger.error(f"Could not create user {email=} {username=}: email exists.")
        errors.append({'error': 'email_exists', "message": "Email is already registered."})
    if len(errors) > 0:
        return jsonify({'errors': errors, 'status': 400}), 400

    db.session.add(User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password)
    ))

    print(f"Create user {email=} {username=} {password=}")
    db.session.commit()

    # TODO: Redirect to login page on success
    return jsonify({'message': 'Created user', 'status': 200}), 200

def sendGPTmessage(GPT_user_id, channel_id):
    gpt_user = User.query.get(GPT_user_id)
    
    # check if GPT user exists
    if gpt_user is None:
        print("GPT user does not exist")
        return

    # check if user is a GPT user
    if not gpt_user.is_GPT:
        print("User is not a GPT user")
        return

    # get the 10 most recent messages from the channel
    recent_messages = db.session.query(Message)\
        .filter(Message.channel_id == channel_id)\
        .order_by(Message.timestamp.desc())\
        .limit(10)\
        .all()

    # Reverse the list to get the oldest message first
    recent_messages.reverse()

    system_message = {"role": "system", "content": gpt_user.begin_prompt}
    user_messages = [msg.prepare_for_gpt() for msg in recent_messages]
    end_system_message = {"role": "system", "content": gpt_user.end_prompt}
    # Combines all messages
    messages = [system_message] + user_messages + [end_system_message]
    print(messages)
    # generate a response from OpenAI's GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6,
        max_tokens=1000,
    )['choices']

    print(response)
    # # create a new message
    msg = Message(channel_id=channel_id, sender_id=GPT_user_id, text=response[0]['message']['content'], timestamp=int(time.time_ns() / 1000000))

    # add message to database
    db.session.add(msg)
    db.session.commit()

    data = [{
             'sender_name': db.session.query(User).get(msg.sender_id).username, 
             'timestamp': msg.timestamp, 
             'text': msg.text
            }]
    emit('history', data, room="channel:" + str(channel_id))

# WEAK SEARCH
@app.route('/api/v1/messages/search', methods=['POST'])
@login_required
def search_messages():
    query = request.json.get('search_query')

    if not query:
        return jsonify({'error': 'Missing required parameters'}), 400

    messages: List[Message] = Message.query.filter(and_(
        Message.text.ilike(f"%{query}%"), 
        Message.channel_id == current_user.curr_channel)
    ).all()
    print(messages)
    # Group messages by channel
    channels = []
    for message in messages:
        channel_id = message.channel_id
        channel_name = Channel.query.get(channel_id).name
        username = User.query.get(message.sender_id).username
        channels.append({
            'channel_id': channel_id, 
             'channel_name': channel_name, 
             'message_sender': username,
             'text': message.text,
             'timestamp': message.timestamp
             })

    return jsonify(channels)
