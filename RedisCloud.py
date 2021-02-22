import os
import json
import redis
from flask import Flask,request,jsonify

app = Flask(__name__)
db=redis.StrictRedis(
        host='10.100.2.218',
        #host='node11006-advweb263.app.ruk-com.cloud',
        port=6379,
        #port=11161,
        password='SSYxhd54349',
        decode_responses=True) 

#Show All Employee
@app.route('/',methods=['GET']) 
def Show_AllEmployee():
    name=db.keys() 
    name.sort()
    req = []
    for i in name :
        req.append(db.hgetall(i))
    return jsonify(req)

# Get Single Employee
@app.route('/<Key>', methods=['GET'])
def Show_Employee(Key):
    name = db.hgetall(Key)  
    return jsonify(name)

#Insert Employee
@app.route('/insert', methods=['POST'])
def add_Employee():
    Fullname = request.json['Fullname']
    Position = request.json['Position']
    PhoneNumber = request.json['PhoneNumber']
    Key = request.json['Key'] 
    user = {"Fullname":Fullname, "Position":Position, "PhoneNumber":PhoneNumber}
    db.hmset(Key,user)
    return 'Insert successful'

#Update Employee
@app.route('/<Key>', methods=['PUT'])
def update_Employee(Key):
    Fullname = request.json['Fullname']
    Position = request.json['Position']
    PhoneNumber = request.json['PhoneNumber']
    user = {"Fullname":Fullname, "Position":Position, "PhoneNumber":PhoneNumber}
    db.hmset(Fullname,user)
    return 'Update Successful'

#Detele Employee
@app.route('/<Key>', methods=['DELETE'])
def delete_Employee(Key):
    db.delete(Key)
    return 'Delete Successful'



@app.route('/setname/<name>')
def setname(name):
    db.set('name',name)
    return 'Name updated.'



if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=80)


