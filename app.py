from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import sqlite3
import os
import joblib
import pandas as pd

from functools import wraps

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# IMPORTANT:
# Change this to a strong random secret before production.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "flood-prediction-development-secret-key"
)


# =========================================================
# CONFIGURATION
# =========================================================

DATABASE = "database.db"

MODEL_PATH = "models/floods.save"


# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

model = joblib.load(MODEL_PATH)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================

def login_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return route_function(
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # If user is already logged in
    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not name:

            flash(
                "Please enter your name.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if not email:

            flash(
                "Please enter your email.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if not password:

            flash(
                "Please enter a password.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        connection = get_db_connection()


        # Check whether email already exists

        existing_user = connection.execute(
            """
            SELECT UserID
            FROM Users
            WHERE Email = ?
            """,
            (email,)
        ).fetchone()


        if existing_user:

            connection.close()

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Insert user

        connection.execute(
            """
            INSERT INTO Users (
                Name,
                Email,
                Password,
                Role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password,
                "user"
            )
        )


        connection.commit()

        connection.close()


        flash(
            "Registration successful. Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Already logged in

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        connection = get_db_connection()


        user = connection.execute(
            """
            SELECT *
            FROM Users
            WHERE Email = ?
            """,
            (email,)
        ).fetchone()


        connection.close()


        if user is None:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        if not check_password_hash(
            user["Password"],
            password
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # Create session

        session.clear()

        session["user_id"] = user["UserID"]

        session["user_name"] = user["Name"]

        session["user_email"] = user["Email"]

        session["user_role"] = user["Role"]


        flash(
            "Login successful.",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("home")
    )


# =========================================================
# USER DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    connection = get_db_connection()


    # Total predictions by current user

    total_predictions = connection.execute(
        """
        SELECT COUNT(*) AS total

        FROM Prediction_Result AS pr

        JOIN Weather_Data AS wd
        ON pr.DataID = wd.DataID

        WHERE wd.UserID = ?
        """,
        (
            session["user_id"],
        )
    ).fetchone()["total"]


    # Total flood predictions

    flood_predictions = connection.execute(
        """
        SELECT COUNT(*) AS total

        FROM Prediction_Result AS pr

        JOIN Weather_Data AS wd
        ON pr.DataID = wd.DataID

        WHERE
            wd.UserID = ?
            AND pr.FloodResult = 1
        """,
        (
            session["user_id"],
        )
    ).fetchone()["total"]


    # Total no-flood predictions

    no_flood_predictions = connection.execute(
        """
        SELECT COUNT(*) AS total

        FROM Prediction_Result AS pr

        JOIN Weather_Data AS wd
        ON pr.DataID = wd.DataID

        WHERE
            wd.UserID = ?
            AND pr.FloodResult = 0
        """,
        (
            session["user_id"],
        )
    ).fetchone()["total"]


    # Recent predictions

    recent_predictions = connection.execute(
        """
        SELECT

            pr.PredictionID,

            pr.FloodResult,

            pr.FloodProbability,

            pr.PredictionDate,

            wd.Temp,

            wd.Humidity,

            wd.AnnualRainfall

        FROM Prediction_Result AS pr

        JOIN Weather_Data AS wd
        ON pr.DataID = wd.DataID

        WHERE wd.UserID = ?

        ORDER BY
            pr.PredictionDate DESC

        LIMIT 5
        """,
        (
            session["user_id"],
        )
    ).fetchall()


    connection.close()


    return render_template(
        "dashboard.html",

        total_predictions=total_predictions,

        flood_predictions=flood_predictions,

        no_flood_predictions=no_flood_predictions,

        recent_predictions=recent_predictions
    )


# =========================================================
# PREDICTION PAGE
# =========================================================

@app.route("/predict")
@login_required
def predict():

    return render_template(
        "index.html"
    )


# =========================================================
# MAKE PREDICTION
# =========================================================

@app.route(
    "/result",
    methods=["POST"]
)
@login_required
def result():

    try:

        # -----------------------------------------
        # READ FORM VALUES
        # -----------------------------------------

        temp = float(
            request.form["Temp"]
        )

        humidity = float(
            request.form["Humidity"]
        )

        cloud = float(
            request.form["CloudCover"]
        )

        annual = float(
            request.form["ANNUAL"]
        )

        janfeb = float(
            request.form["JanFeb"]
        )

        marmay = float(
            request.form["MarMay"]
        )

        junsep = float(
            request.form["JunSep"]
        )

        octdec = float(
            request.form["OctDec"]
        )

        avgjune = float(
            request.form["avgjune"]
        )

        sub = float(
            request.form["sub"]
        )


        # -----------------------------------------
        # CREATE DATAFRAME
        # -----------------------------------------

        sample = pd.DataFrame(
            [[
                temp,
                humidity,
                cloud,
                annual,
                janfeb,
                marmay,
                junsep,
                octdec,
                avgjune,
                sub
            ]],

            columns=[
                "Temp",
                "Humidity",
                "Cloud Cover",
                "ANNUAL",
                "Jan-Feb",
                "Mar-May",
                "Jun-Sep",
                "Oct-Dec",
                "avgjune",
                "sub"
            ]
        )


        # -----------------------------------------
        # PREDICTION
        # -----------------------------------------

        prediction = int(
            model.predict(sample)[0]
        )


        # -----------------------------------------
        # PREDICTION PROBABILITY
        # -----------------------------------------

        probabilities = model.predict_proba(
            sample
        )[0]


        # Probability of class 1 = Flood

        flood_probability = float(
            probabilities[1] * 100
        )


        # -----------------------------------------
        # DATABASE CONNECTION
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()


        # -----------------------------------------
        # SAVE WEATHER DATA
        # -----------------------------------------

        cursor.execute(
            """
            INSERT INTO Weather_Data (

                UserID,

                Temp,

                Humidity,

                CloudCover,

                AnnualRainfall,

                JanFebRainfall,

                MarMayRainfall,

                JunSepRainfall,

                OctDecRainfall,

                AvgJuneRainfall,

                SubRainfall

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                session["user_id"],

                temp,

                humidity,

                cloud,

                annual,

                janfeb,

                marmay,

                junsep,

                octdec,

                avgjune,

                sub

            )
        )


        # Get inserted DataID

        data_id = cursor.lastrowid


        # -----------------------------------------
        # GET ML MODEL ID
        # -----------------------------------------

        model_record = cursor.execute(
            """
            SELECT ModelID

            FROM ML_Model

            WHERE ModelFile = ?
            """,

            (
                "models/floods.save",
            )

        ).fetchone()


        if model_record is None:

            connection.rollback()

            connection.close()

            raise Exception(
                "ML model information was not found in the database."
            )


        model_id = model_record["ModelID"]


        # -----------------------------------------
        # SAVE PREDICTION RESULT
        # -----------------------------------------

        cursor.execute(
            """
            INSERT INTO Prediction_Result (

                DataID,

                ModelID,

                FloodResult,

                FloodProbability

            )

            VALUES (?, ?, ?, ?)
            """,

            (

                data_id,

                model_id,

                prediction,

                flood_probability

            )
        )


        prediction_id = cursor.lastrowid


        connection.commit()

        connection.close()


        # -----------------------------------------
        # DISPLAY RESULT
        # -----------------------------------------

        if prediction == 1:

            return render_template(

                "chance.html",

                prediction_id=prediction_id,

                probability=round(
                    flood_probability,
                    2
                )

            )


        else:

            return render_template(

                "no_chance.html",

                prediction_id=prediction_id,

                probability=round(
                    flood_probability,
                    2
                )

            )


    except ValueError:

        flash(
            "Please enter valid numeric values.",
            "error"
        )

        return redirect(
            url_for("predict")
        )


    except Exception as error:

        print(
            "Prediction Error:",
            error
        )

        flash(
            "An error occurred while making the prediction.",
            "error"
        )

        return redirect(
            url_for("predict")
        )


# =========================================================
# PREDICTION HISTORY
# =========================================================

@app.route("/history")
@login_required
def history():

    connection = get_db_connection()


    predictions = connection.execute(
        """
        SELECT

            pr.PredictionID,

            pr.FloodResult,

            pr.FloodProbability,

            pr.PredictionDate,

            wd.DataID,

            wd.Temp,

            wd.Humidity,

            wd.CloudCover,

            wd.AnnualRainfall,

            wd.JanFebRainfall,

            wd.MarMayRainfall,

            wd.JunSepRainfall,

            wd.OctDecRainfall,

            wd.AvgJuneRainfall,

            wd.SubRainfall,

            mm.ModelName,

            mm.AlgorithmType

        FROM Prediction_Result AS pr

        JOIN Weather_Data AS wd
        ON pr.DataID = wd.DataID

        JOIN ML_Model AS mm
        ON pr.ModelID = mm.ModelID

        WHERE wd.UserID = ?

        ORDER BY
            pr.PredictionDate DESC
        """,

        (
            session["user_id"],
        )

    ).fetchall()


    connection.close()


    return render_template(

        "history.html",

        predictions=predictions

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )