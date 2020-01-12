from . import db


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64), index=True)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Id {}>'.format(self.id)
