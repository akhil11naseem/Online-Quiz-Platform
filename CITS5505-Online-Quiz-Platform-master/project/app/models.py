from app import db

class insert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self):
        self.user_id = user_id



    