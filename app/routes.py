from flask import Blueprint, jsonify, render_template, request, redirect, session, send_file
from app.services import *

main_bp = Blueprint("main", __name__)

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@main_bp.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        role = validate_user(user, pwd)
        if role:
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

@main_bp.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    chart = None

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")

        # ✅ Fix: validate name
        if not name:
            return "Error: Name is required"

        if action == "add":
            save_client(name)

        elif action == "progress":
            adherence = request.form.get("adherence")
            save_progress(name, adherence)

        elif action == "chart":
            chart = generate_chart(name)

        elif action == "pdf":
            file = generate_pdf(name)
            return send_file(file, as_attachment=True)

    clients = get_clients()

    return render_template("dashboard.html", clients=clients, chart=chart)

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")