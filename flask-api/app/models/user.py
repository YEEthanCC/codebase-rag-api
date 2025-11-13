from app import db

class User(db.Model):
    public_id = db.Column(db.String, primary_key=True)
    fullname = db.Column(db.String, unique=True, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"User(public_id={self.public_id}, fullname={self.fullname}, created_at={self.created_at}, updated_at={self.updated_at})"
