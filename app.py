from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Init ooapp
app = Flask(__name__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webadmin:CAOnco33311@10.100.2.217:5432/CloudDB"
#app.consfig['SQLALCHEMY_DATABASE_URI'] = "postgresql://webadmin:XCVmpe99066@node8581-advweb-13.app.ruk-com.cloud:11099/CloudDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

#Staff Class/Model
class Staffs(db.Model):
    id = db.Column(db.String(13), primary_key=True, unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(25))s
    phone = db.Column(db.String(10))
    
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

# Staff Schema
class StaffSchema(ma.Schema):
    class Meta:
        fields =('id', 'name', 'email', 'phone')

# Init Schema 
staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

# Get All Staffs
@app.route('/staffs', methods=['GET'])
def get_staffs():
    all_staffs = Staffs.query.all()
    result = staffs_schema.dump(all_staffs)
    return jsonify(result)


# Get Single Staff
@app.route('/staff/<id>', methods=['GET'])
def get_staff(id):
    staff = Staffs.query.get(id)
    return staff_schema.jsonify(staff)

# Create a Staff
@app.route('/staff', methods=['POST'])
def add_staff():
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    new_staff = Staffs(id, name, email, phone)

    db.session.add(new_staff)
    db.session.commit()

    return staff_schema.jsonify(new_staff)

# Update a Staff
@app.route('/staff/<id>', methods=['PUT'])
def update_staff(id):
    staff = Staffs.query.get(id)
    
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    staff.name = name
    staff.email = email
    staff.phone = phone

    db.session.commit()

    return staff_schema.jsonify(staff)

# Delete Staff
@app.route('/staff/<id>', methods=['DELETE'])
def delete_staff(id):
    staff = Staffs.query.get(id)
    db.session.delete(staff)
    db.session.commit()
    
    return staff_schema.jsonify(staff)

# Web Root Hello
@app.route('/', methods=['GET'])
def get():
    return jsonify({'ms': 'Hello Cloud DB1'})

# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
