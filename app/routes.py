from flask import Blueprint, render_template, request, redirect, url_for, send_file,jsonify
from app.services import calculate_calories
import csv
import io

main_bp = Blueprint('main', __name__)

# In-memory storage (like tkinter list)
clients = []

PROGRAMS = {
    "Fat Loss (FL)": {"factor": 22, "workout": "Back Squat + Cardio", "diet": "Egg Whites + Chicken"},
    "Muscle Gain (MG)": {"factor": 35, "workout": "Squat + Bench + Deadlift", "diet": "Eggs + Biryani"},
    "Beginner (BG)": {"factor": 26, "workout": "Basic Bodyweight", "diet": "Balanced Diet"}
}

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        weight = float(request.form.get("weight"))
        program = request.form.get("program")
        adherence = request.form.get("adherence")
        notes = request.form.get("notes")

        calories = calculate_calories(weight, PROGRAMS[program]["factor"])

        client = {
            "name": name,
            "age": age,
            "weight": weight,
            "program": program,
            "adherence": adherence,
            "notes": notes,
            "calories": calories
        }

        clients.append(client)

        return redirect(url_for("main.index"))

    return render_template("index.html", clients=clients, programs=PROGRAMS)


@main_bp.route("/export")
def export_csv():
    if not clients:
        return "No data"

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Name", "Age", "Weight", "Program", "Adherence", "Notes"])

    for c in clients:
        writer.writerow([
            c["name"], c["age"], c["weight"],
            c["program"], c["adherence"], c["notes"]
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="clients.csv"
    )