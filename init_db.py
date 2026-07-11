import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "database.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")


    # ==========================================
    # 1. USERS TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (

            UserID INTEGER PRIMARY KEY AUTOINCREMENT,

            Name TEXT NOT NULL,

            Email TEXT NOT NULL UNIQUE,

            Password TEXT NOT NULL,

            Role TEXT NOT NULL DEFAULT 'user'

        )
    """)


    # ==========================================
    # 2. WEATHER DATA TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weather_Data (

            DataID INTEGER PRIMARY KEY AUTOINCREMENT,

            UserID INTEGER NOT NULL,

            Temp REAL NOT NULL,

            Humidity REAL NOT NULL,

            CloudCover REAL NOT NULL,

            AnnualRainfall REAL NOT NULL,

            JanFebRainfall REAL NOT NULL,

            MarMayRainfall REAL NOT NULL,

            JunSepRainfall REAL NOT NULL,

            OctDecRainfall REAL NOT NULL,

            AvgJuneRainfall REAL NOT NULL,

            SubRainfall REAL NOT NULL,

            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (UserID)
            REFERENCES Users(UserID)
            ON DELETE CASCADE

        )
    """)


    # ==========================================
    # 3. ML MODEL TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ML_Model (

            ModelID INTEGER PRIMARY KEY AUTOINCREMENT,

            ModelName TEXT NOT NULL,

            AlgorithmType TEXT NOT NULL,

            Accuracy REAL,

            ModelFile TEXT NOT NULL

        )
    """)


    # ==========================================
    # 4. PREDICTION RESULT TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prediction_Result (

            PredictionID INTEGER PRIMARY KEY AUTOINCREMENT,

            DataID INTEGER NOT NULL,

            ModelID INTEGER NOT NULL,

            FloodResult INTEGER NOT NULL,

            FloodProbability REAL,

            PredictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (DataID)
            REFERENCES Weather_Data(DataID)
            ON DELETE CASCADE,

            FOREIGN KEY (ModelID)
            REFERENCES ML_Model(ModelID)
            ON DELETE CASCADE

        )
    """)


    # ==========================================
    # INSERT RANDOM FOREST MODEL INFORMATION
    # ==========================================

    cursor.execute("""
        SELECT ModelID
        FROM ML_Model
        WHERE ModelName = ?
    """, (
        "Flood Prediction Random Forest",
    ))

    existing_model = cursor.fetchone()


    if existing_model is None:

        cursor.execute("""
            INSERT INTO ML_Model (
                ModelName,
                AlgorithmType,
                Accuracy,
                ModelFile
            )
            VALUES (?, ?, ?, ?)
        """, (

            "Flood Prediction Random Forest",

            "Random Forest Classifier",

            95.65,

            "models/floods.save"

        ))


    # ==========================================
    # OPTIONAL DEFAULT ADMIN USER
    # ==========================================

    cursor.execute("""
        SELECT UserID
        FROM Users
        WHERE Email = ?
    """, (
        "admin@floodprediction.com",
    ))

    admin = cursor.fetchone()


    if admin is None:

        hashed_password = generate_password_hash(
            "admin123"
        )

        cursor.execute("""
            INSERT INTO Users (
                Name,
                Email,
                Password,
                Role
            )
            VALUES (?, ?, ?, ?)
        """, (

            "Administrator",

            "admin@floodprediction.com",

            hashed_password,

            "admin"

        ))


    connection.commit()

    connection.close()


    print(
        "Database created successfully!"
    )

    print(
        "Tables created:"
    )

    print(
        "1. Users"
    )

    print(
        "2. Weather_Data"
    )

    print(
        "3. ML_Model"
    )

    print(
        "4. Prediction_Result"
    )


if __name__ == "__main__":

    create_database()