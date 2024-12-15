CREATE DATABASE FitnessCenterDB;
USE FitnessCenterDB;

-- Create the tables for the database
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    UserEmail VARCHAR(255) NOT NULL,
    UserName VARCHAR(255) NOT NULL,
    UserPhone VARCHAR(20),
    UserAddress VARCHAR(255)
);

CREATE TABLE Membership (
    MembershipID INT PRIMARY KEY,
    MembershipName VARCHAR(255) NOT NULL,
    MembershipEmail VARCHAR(255) NOT NULL,
    MonthlyFee DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Promotion (
    PromotionalID INT PRIMARY KEY,
    PromotionalName VARCHAR(255) NOT NULL,
    Description TEXT,
    PromotionalStartDate DATE NOT NULL,
    PromotionalEndDate DATE NOT NULL,
    DiscountPercentage DECIMAL(5, 2) NOT NULL
);

CREATE TABLE TransactionHeader (
    TransactionID INT PRIMARY KEY,
    UserID INT NOT NULL,
    MembershipID INT,
    PromotionalID INT,
    MembershipStartDate DATE,
    MembershipEndDate DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MembershipID) REFERENCES Membership(MembershipID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (PromotionalID) REFERENCES Promotion(PromotionalID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Trainer (
    TrainerID INT PRIMARY KEY,
    TrainerName VARCHAR(255) NOT NULL,
    TrainerSpecialty VARCHAR(255) NOT NULL,
    YearsOfExperience INT NOT NULL,
    TrainerEmail VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL
);

CREATE TABLE Class (
    ClassesID INT PRIMARY KEY,
    ClassesName VARCHAR(255) NOT NULL,
    ClassesSchedule VARCHAR(255) NOT NULL,
    TrainerID INT NOT NULL,
    FOREIGN KEY (TrainerID) REFERENCES Trainer(TrainerID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Maintenance (
    MaintenanceID INT PRIMARY KEY,
    MaintenanceDate DATE NOT NULL,
    MaintenanceType VARCHAR(255) NOT NULL,
    TechnicianName VARCHAR(255) NOT NULL
);

CREATE TABLE Equipment (
    EquipmentID INT PRIMARY KEY,
    EquipmentName VARCHAR(255) NOT NULL,
    Type VARCHAR(255) NOT NULL,
    Cost DECIMAL(10, 2) NOT NULL,
    PurchaseDate DATE NOT NULL,
    TheCondition VARCHAR(50),
    MaintenanceID INT,
    FOREIGN KEY (MaintenanceID) REFERENCES Maintenance(MaintenanceID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE TransactionDetail (
    TransactionID INT,
    ClassesID INT,
    EquipmentID INT,
    Quantity INT NOT NULL,
    PRIMARY KEY (TransactionID, ClassesID, EquipmentID),
    FOREIGN KEY (TransactionID) REFERENCES TransactionHeader(TransactionID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ClassesID) REFERENCES Class(ClassesID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID) ON DELETE CASCADE ON UPDATE CASCADE
);
