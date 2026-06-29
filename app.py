from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# AQI Breakpoints (US EPA Standard)
# Format: (pollutant, [(C_low, C_high, I_low, I_high), ...])
AQI_BREAKPOINTS = {
    "pm25": [
        (0.0,   12.0,   0,   50),
        (12.1,  35.4,  51,  100),
        (35.5,  55.4, 101,  150),
        (55.5, 150.4, 151,  200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ],
    "pm10": [
        (0,    54,   0,   50),
        (55,  154,  51,  100),
        (155, 254, 101,  150),
        (255, 354, 151,  200),
        (355, 424, 201,  300),
        (425, 504, 301,  400),
        (505, 604, 401,  500),
    ],
    "no2": [
        (0,    53,   0,   50),
        (54,  100,  51,  100),
        (101, 360, 101,  150),
        (361, 649, 151,  200),
        (650, 1249, 201, 300),
        (1250, 1649, 301, 400),
        (1650, 2049, 401, 500),
    ],
    "so2": [
        (0,    35,   0,   50),
        (36,   75,  51,  100),
        (76,  185, 101,  150),
        (186, 304, 151,  200),
        (305, 604, 201,  300),
        (605, 804, 301,  400),
        (805, 1004, 401, 500),
    ],
    "co": [
        (0.0,   4.4,   0,   50),
        (4.5,   9.4,  51,  100),
        (9.5,  12.4, 101,  150),
        (12.5, 15.4, 151,  200),
        (15.5, 30.4, 201,  300),
        (30.5, 40.4, 301,  400),
        (40.5, 50.4, 401,  500),
    ],
}

AQI_CATEGORIES = [
    (0,   50,  "Good",                  "#00e400", "Air quality is satisfactory and poses little or no risk."),
    (51,  100, "Moderate",              "#ffff00", "Acceptable air quality, but some pollutants may be a concern for sensitive groups."),
    (101, 150, "Unhealthy for Sensitive Groups", "#ff7e00", "Sensitive people may experience health effects. General public is less likely to be affected."),
    (151, 200, "Unhealthy",             "#ff0000", "Everyone may begin to experience health effects."),
    (201, 300, "Very Unhealthy",        "#8f3f97", "Health alert: everyone may experience more serious health effects."),
    (301, 500, "Hazardous",             "#7e0023", "Health warning of emergency conditions. Everyone is affected."),
]


def calc_aqi_for_pollutant(concentration, pollutant):
    """Calculate sub-AQI for a single pollutant using linear interpolation."""
    breakpoints = AQI_BREAKPOINTS.get(pollutant)
    if breakpoints is None:
        return None
    for (c_lo, c_hi, i_lo, i_hi) in breakpoints:
        if c_lo <= concentration <= c_hi:
            aqi = ((i_hi - i_lo) / (c_hi - c_lo)) * (concentration - c_lo) + i_lo
            return round(aqi)
    # Above max breakpoint
    return 500


def get_aqi_category(aqi):
    for (lo, hi, label, color, advice) in AQI_CATEGORIES:
        if lo <= aqi <= hi:
            return {"label": label, "color": color, "advice": advice}
    return {"label": "Hazardous", "color": "#7e0023", "advice": "Extremely dangerous air quality."}


def calculate_overall_aqi(pm25, pm10, no2, so2, co):
    sub_aqis = {}
    values = {
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "so2": so2,
        "co": co,
    }
    for pollutant, val in values.items():
        if val is not None and val >= 0:
            sub_aqis[pollutant] = calc_aqi_for_pollutant(val, pollutant)

    if not sub_aqis:
        return None, None, {}

    overall_aqi = max(sub_aqis.values())
    dominant = max(sub_aqis, key=sub_aqis.get)
    return overall_aqi, dominant, sub_aqis


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        pm25 = float(data.get("pm25") or 0)
        pm10 = float(data.get("pm10") or 0)
        no2  = float(data.get("no2")  or 0)
        so2  = float(data.get("so2")  or 0)
        co   = float(data.get("co")   or 0)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input values"}), 400

    overall_aqi, dominant, sub_aqis = calculate_overall_aqi(pm25, pm10, no2, so2, co)

    if overall_aqi is None:
        return jsonify({"error": "Please enter at least one pollutant value"}), 400

    category = get_aqi_category(overall_aqi)

    pollutant_names = {
        "pm25": "PM2.5",
        "pm10": "PM10",
        "no2":  "NO₂",
        "so2":  "SO₂",
        "co":   "CO",
    }

    sub_aqi_display = {
        pollutant_names[k]: v for k, v in sub_aqis.items()
    }

    return jsonify({
        "aqi": overall_aqi,
        "category": category["label"],
        "color": category["color"],
        "advice": category["advice"],
        "dominant_pollutant": pollutant_names.get(dominant, dominant),
        "sub_aqis": sub_aqi_display,
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
