from flask import Flask, render_template, request
import pandas as pd
import joblib


app = Flask(__name__)


# ==============================
# LOAD TRAINED MODEL
# ==============================

model = joblib.load(
    "models/floods.save"
)


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# ==============================
# PREDICTION PAGE
# ==============================

@app.route("/predict")
def predict():

    return render_template(
        "index.html"
    )


# ==============================
# RESULT PAGE
# ==============================

@app.route(
    "/result",
    methods=["POST"]
)
def result():

    try:

        # Read form values

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


        # Create input DataFrame
        # Feature order must match training data

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


        # Make prediction
        # NO SCALER

        prediction = model.predict(
            sample
        )[0]


        # Debugging

        print(
            "Input:"
        )

        print(
            sample
        )

        print(
            "Prediction:",
            prediction
        )


        # Return result page

        if prediction == 1:

            return render_template(
                "chance.html"
            )

        else:

            return render_template(
                "no_chance.html"
            )


    except Exception as e:

        return f"Error: {e}"


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )