import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Project

SUID = 'UID_01741928apfjafj129348'
JUID = 'UID_94781024nalskfnaf092l'
MUID = 'UID_023njondf9283f0vjh238'
DUID = 'UID_98491dhjnc9823af3r89c'
P1   = 'PID_1847jk1h484019h4jfd91'
P2   = 'PID_fjmknmi3jd23098074ehg'
P3   = 'PID_kfopwifj23809nvc39r09'
P4   = 'PID_fklp1kr1r823190809123'
P5   = 'PID_wlkfokpo112390kl2j3p9'
P6   = 'PID_opjfapojf32909023pj00'
P7   = 'PID_lmdalp2mfkd9120398238'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(SUID, username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_follow(self):
        u1 = User(JUID, username='john', email='john@example.com')
        u2 = User(SUID, username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(JUID, username='john', email='john@example.com')
        u2 = User(SUID, username='susan', email='susan@example.com')
        u3 = User(MUID, username='mary', email='mary@example.com')
        u4 = User(DUID, username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Project(P1, u1.userid, 'Project 1', 'webdev;')
        p2 = Project(P2, u2.userid, 'Project 2', 'webdev;python;')
        p3 = Project(P3, u3.userid, 'Project 3', 'webdev;python;mysql;')
        p4 = Project(P4, u4.userid, 'Project 4', 'webdev;python;mysql;flask;')
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_projects().all()
        f2 = u2.followed_projects().all()
        f3 = u3.followed_projects().all()
        f4 = u4.followed_projects().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
