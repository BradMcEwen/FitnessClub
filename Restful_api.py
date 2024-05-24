from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.json.sort_keys = False
ma = Marshmallow(app)

db_name = "FitnessClub"
user = "root"
password = "Lukabuka#02"
host = "localhost"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database = db_name, 
            user = user,
            password = password,
            host = host
        )
        if conn.is_connected():
            return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None
    
class MemberSchema(ma.Schema):
    Name = fields.String(required = True)
    Email = fields.String(required = True)
    PhoneNumber = fields.String(required = True)

    class Meta:
        fields = ("MemberID", "Name", "Email", "PhoneNumber")
    
member_schema = MemberSchema()        
members_schema = MemberSchema(many = True)

@app.route('/members', methods = ['GET'])
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    query = "SELECT * FROM Members"
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members_schema.jsonify(members)

@app.route('/members', methods = ['POST'])
def add_member():
    member_info = member_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    Name = member_info['Name']
    Email = member_info['Email']
    PhoneNumber = member_info['PhoneNumber']
    new_member = (Name, Email, PhoneNumber)
    query = "INSERT INTO Members(Name, Email, PhoneNumber) VALUES (%s, %s, %s)"
    cursor.execute(query, new_member)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New member was added successfully"}), 201 

@app.route("/members/<int:MemberID>", methods = ["PUT"])
def upWorkoutDate_member(MemberID):
    member_info = member_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    Name = member_info["Name"]
    Email = member_info["Email"]
    PhoneNumber = member_info["PhoneNumber"]
    upWorkoutDated_member = (Name, Email, PhoneNumber, MemberID)
    query = "UPWorkoutDate Members SET Name = %s, Email = %s, PhoneNumber = %s WHERE MemberID = %s"
    cursor.execute(query, upWorkoutDated_member)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': "Member was upWorkoutDated successfully"}), 200

@app.route('/members/<int:MemberID>', methods = ["DELETE"])
def delete_member(MemberID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Members WHERE MemberID = %s"
    cursor.execute(query, (MemberID,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Member successfully deleted!"}), 200



class WorkoutSessionSchema(ma.Schema):
    WorkoutDate = fields.Date(required = True)
    MemberID = fields.Int(required = True)
    WorkoutType = fields.String(required= True)

    class Meta:
        fields = ("SessionID", "WorkoutType", "WorkoutDate", "MemberID")
    
WorkoutSession_schema = WorkoutSessionSchema()        
WorkoutSessions_schema = WorkoutSessionSchema(many = True)

@app.route('/WorkoutSessions', methods = ['GET'])
def get_WorkoutSessions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    query = "SELECT * FROM WorkoutSessions"
    cursor.execute(query)
    WorkoutSessions = cursor.fetchall()
    cursor.close()
    conn.close()
    return WorkoutSessions_schema.jsonify(WorkoutSessions)

@app.route('/WorkoutSessions', methods = ['POST'])
def add_WorkoutSession():
    WorkoutSession_info = WorkoutSession_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    
    WorkoutType = WorkoutSession_info["WorkoutType"]
    WorkoutDate = WorkoutSession_info['WorkoutDate']
    MemberID = WorkoutSession_info["MemberID"]
    new_WorkoutSession = (WorkoutType, WorkoutDate, MemberID)
    query = "INSERT INTO WorkoutSessions(WorkoutType, WorkoutDate, MemberID) VALUES (%s, %s, %s)"
    cursor.execute(query, new_WorkoutSession)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New Workout Session was added successfully"}), 201 

@app.route("/WorkoutSessions/<int:SessionID>", methods = ["PUT"])
def update_WorkoutSession(SessionID):
    WorkoutSession_info = WorkoutSession_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    WorkoutType = WorkoutSession_info['WorkoutType']
    WorkoutDate = WorkoutSession_info['WorkoutDate']
    MemberID = WorkoutSession_info["MemberID"]
    updated_WorkoutSession = (WorkoutType, WorkoutDate, MemberID, SessionID)
    query = "UPDATE WorkoutSessions SET WorkoutType = %s, WorkoutDate = %s, MemberID = %s WHERE SessionID = %s"
    cursor.execute(query, updated_WorkoutSession)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': "Workout Session was updated successfully"}), 200

@app.route('/WorkoutSessions/<int:SessionID>', methods = ["DELETE"])
def delete_WorkoutSession(SessionID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM WorkoutSessions WHERE SessionID = %s"
    cursor.execute(query, (SessionID,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Workout Session successfully deleted!"}), 200

if __name__ == "__main__":
    app.run(debug=True, port = 5001) 