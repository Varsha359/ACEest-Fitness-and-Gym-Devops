from flask import Blueprint, render_template, request, jsonify
from app.services import calculate_calories

main_bp = Blueprint('main', __name__)

PROGRAMS = {
    "Fat Loss (FL)": {
        "calorie_factor": 22,
        "workout": "Back Squat + Cardio + Bench + Deadlift",
        "diet": "Egg Whites + Chicken + Fish Curry"
    },
    "Muscle Gain (MG)": {
        "calorie_factor": 35,
        "workout": "Squat + Bench + Deadlift + Rows",
        "diet": "Eggs + Biryani + Mutton Curry"
    },
    "Beginner (BG)": {
        "calorie_factor": 26,
        "workout": "Air Squats + Push-ups + Ring Rows",
        "diet": "Balanced Tamil Meals"
    }
}

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        weight = float(request.form.get("weight"))
        program = request.form.get("program")
        adherence = request.form.get("adherence")

        factor = PROGRAMS[program]["calorie_factor"]
        calories = calculate_calories(weight, factor)

        result = {
            "name": name,
            "age": age,
            "weight": weight,
            "program": program,
            "adherence": adherence,
            "calories": calories,
            "workout": PROGRAMS[program]["workout"],
            "diet": PROGRAMS[program]["diet"]
        }

    return render_template("index.html", programs=PROGRAMS, result=result)