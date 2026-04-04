from flask import Blueprint, render_template, request, jsonify
from app.services import (
    calculate_calories,
    save_client,
    get_client,
    save_progress,
    generate_chart
)

main_bp = Blueprint("main", __name__)

PROGRAMS = {
    "Fat Loss (FL)": 22,
    "Muscle Gain (MG)": 35,
    "Beginner (BG)": 26
}

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    message = None
    chart = None

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")

        if action == "save":
            age = request.form.get("age")
            weight = float(request.form.get("weight"))
            program = request.form.get("program")

            calories = calculate_calories(weight, PROGRAMS[program])
            save_client(name, age, weight, program, calories)

            message = "Client saved successfully"

        elif action == "load":
            data = get_client(name)

            if data:
                _, name, age, weight, program, calories = data
                result = {
                    "name": name,
                    "age": age,
                    "weight": weight,
                    "program": program,
                    "calories": calories
                }
            else:
                message = "Client not found"

        elif action == "progress":
            adherence = request.form.get("adherence")
            save_progress(name, adherence)
            message = "Progress saved"

        elif action == "chart":
            chart = generate_chart(name)

            if not chart:
                message = "No progress data available"

    return render_template(
        "index.html",
        programs=PROGRAMS,
        result=result,
        message=message,
        chart=chart
    )