import unittest
from app import app, db
from app.models import Message

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

    def test_message_serialization(self):
        """
        Test serialize() for message
        """
        message = Message(
            channel_id=1,
            sender_id=1,
            text='test text',
            timestamp=1622016000
        )
        db.session.add(message)
        db.session.commit()
        retrieved_message = Message.query.get(1)
        expected_serialization = {
            'id': 1,
            'channel_id': 1,
            'sender_id': 1,
            'text': 'test text',
            'timestamp': 1622016000
        }
        self.assertEqual(retrieved_message.serialize(), expected_serialization)

    def test_add_message(self):
        # CREATE A TEST MESSAGE
        message = Message(
            channel_id=1,
            sender_id=1,
            text='test text',
            timestamp=1622016000
        )
        db.session.add(message)
        db.session.commit()

        # RETRIEVE THE MESSAGE FROM THE DATABASE
        retrieved_message = Message.query.get(1)

        # CHECK THAT THE SERIALIZATION IS CORRECT
        expected_serialization = {
            'id': 1,
            'channel_id': 1,
            'sender_id': 1,
            'text': 'test text',
            'timestamp': 1622016000
        }
        self.assertEqual(retrieved_message.serialize(), expected_serialization)


if __name__ == '__main__':
    unittest.main()
