-- Create the database
CREATE DATABASE FitnessClub;

-- Use the database
USE FitnessClub;

-- Create the Members table
CREATE TABLE Members (
    MemberID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(15)
);

-- Create the WorkoutSessions table
CREATE TABLE WorkoutSessions (
    SessionID INT AUTO_INCREMENT PRIMARY KEY,
    MemberID INT,
    WorkoutDate DATE,
    WorkoutType VARCHAR(50),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);


SELECT * FROM Members;
SELECT * FROM WorkoutSessions;
INSERT INTO WorkoutSessions(WorkoutType) VALUES ("cardio", "push", "pull");