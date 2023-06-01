import unittest
from unittest import mock

from sqlalchemy import desc
from app import app, db
from app.models import Message, User
from app.views import message_recieved

# USE IN-MEMORY DATABASE TO SAVE CLEANING UP FILES.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

class MessageModelTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _test_message_received(self, mock_current_user, mock_emit, message, channel_id, username):
        data = {
            'text': message,
            'channel_id': channel_id
        }
        user = User(id=1, username=username)
        mock_current_user.id = user.id
        mock_current_user.username = user.username

        message_recieved(data)

        msg = db.session.query(Message).order_by(desc(Message.timestamp)).first()
        self.assertEqual(msg.sender_id, user.id)
        self.assertEqual(msg.channel_id, int(channel_id))
        self.assertEqual(msg.text, message)

        expected_emit_calls = [
            unittest.mock.call('receive_data', {'text': f'Message recieved! {message} sender testuser'}, room=[1]),
            unittest.mock.call('history', {'data': [msg.serialize()]}, room=1)
        ]
        mock_emit.assert_has_calls(expected_emit_calls)
