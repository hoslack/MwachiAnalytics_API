from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String(80))

    """Method for saving user into the database user """
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    phone_number = db.Column(db.String(50), index=True, unique=True)
    how_to_contact = db.Column(db.String(50))
    leading_channel = db.Column(db.String(50))
    project_type = db.Column(db.String(50))
    software_requirements = db.Column(db.String(250))
    description = db.Column(db.Text)
    created_by = db.Column(db.String)
    paid = db.Column(db.Boolean)

    """Method for saving order into the database user """

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.project_type)
