from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model and scaler
model = joblib.load("models/floods.save")
scaler = joblib.load("models/transform.save")


# ===========================
# HOME PAGE
# ===========================
@app.route("/")
def home():
    return render_template("home.html")


# ===========================
# PREDICTION PAGE
# ===========================
@app.route("/predict")
def predict():
    return render_template("index.html")


# ===========================
# RESULT
# ===========================
@app.route("/result", methods=["POST"])
def result():

    try:

        temp = float(request.form["Temp"])
        humidity = float(request.form["Humidity"])
        cloud = float(request.form["CloudCover"])
        annual = float(request.form["ANNUAL"])
        janfeb = float(request.form["JanFeb"])
        marmay = float(request.form["MarMay"])
        junsep = float(request.form["JunSep"])
        octdec = float(request.form["OctDec"])
        avgjune = float(request.form["avgjune"])
        sub = float(request.form["sub"])

        sample = pd.DataFrame([[
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
        ]], columns=[
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
        ])

        sample = scaler.transform(sample)

        prediction = model.predict(sample)[0]

        if prediction == 1:
            return render_template("chance.html")

        else:
            return render_template("no_chance.html")

    except Exception as e:
        return f"Error : {e}"


if __name__ == "__main__":
    app.run(debug=True)