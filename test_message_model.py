"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from datetime import datetime

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.user1 = User.signup(
            username="TestUsername1",
            email="TestEmail1",
            password="TestPassword1",
            bio=None,
            location=None,
            image_url=None,
            header_image_url=None,
        )

        self.user2 = User.signup(
            username="testUsername2",
            email="TestEmail2",
            password="TestPassword2",
            bio=None,
            location=None,
            image_url=None,
            header_image_url=None
        )
        db.session.commit() 

        self.client = app.test_client()


    def tearDown(self):
        """Clean up after each test"""
        db.session.rollback()
        

    def test_message_model(self):
        """Does basic model work?"""
        # Create new messages for user1 and user2
        
        user1Msg = Message(
            text="Test message.",
            timestamp=datetime.utcnow(),
            user_id=self.user1.id
        )
        user2Msg = Message(
            text="Test message,",
            timestamp=datetime.utcnow(),
            user_id=self.user2.id
        )

        db.session.add([user1Msg,user2Msg])
        db.session.commit()

        #Check that the length of message list for users1 == 1
        self.assertEqual(len(self.user1.messages), 1)
        #Check that there is content in user1 message
        self.assertIn(user1Msg, self.user1.messages)
        #Check that the text in user1 message is shown
        self.assertEqual(self.user1.messages[0].text, "Test message.")
        #Check that the length of message list for user2 == 1
        self.assertEqual(len(self.user2.messages), 1)
        #Check that there is content in user2 message
        self.assertIn(user2Msg, self.user2.messages)
        #Check that the text in user2 message is shown 
        self.assertEqual(self.user2.messages[0].text, "Test message.")

 
        