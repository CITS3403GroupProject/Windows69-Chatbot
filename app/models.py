from sqlalchemy import Column, ForeignKey, UniqueConstraint
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID, INTEGER, TIMESTAMP
from app import db


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(127))
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    profile_image = db.Column(db.BLOB())
    curr_channel = db.Column(db.Integer, ForeignKey(Channel.id), nullable=True)
    messages = db.relationship('Message', backref='sender', lazy=True)

    # for GPT bots:
    is_GPT = db.Column(db.Boolean, default=False)
    begin_prompt = db.Column(db.String(255), nullable=True)
    end_prompt = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"{self.id=} <{self.email=}> {self.username=}"

class ChannelParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id))
    channel_id = db.Column(db.Integer, ForeignKey(Channel.id))
    channel = db.relationship('Channel', backref='participants')

    __table_args__ = (UniqueConstraint('user_id', 'channel_id', name='user_channel_unqique'),)

# class Attachment(db.Model):
#     id = Column(UUID, primary_key=True)
#     message_id = ForeignKey('parent.id')
#     content = Column(BLOB, nullable=False)
#     name = Column(TEXT, nullable=False)
#     type = Column(TEXT, nullable=False)
#     size = Column(INTEGER, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, ForeignKey(Channel.id), index=True)
    sender_id = db.Column(db.Integer, ForeignKey(User.id))
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    # attachments = db.relationship("Attachment")

    def serialize(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'sender_id': self.sender_id,
            'text': self.text,
            'timestamp': self.timestamp
        }
    def prepare_for_gpt(self):
        role = 'assistant' if self.sender.is_GPT else 'user'
        return {
            "role": role,
            "content": f"{self.sender.username}: {self.text}"
        }

    __table_args__ = (
        db.Index('idx_channel_id', channel_id),
    )

    def __repr__(self) -> str:
        return f"{self.sender_id=} {self.channel_id=} [{self.timestamp=}]: {self.text=}"
