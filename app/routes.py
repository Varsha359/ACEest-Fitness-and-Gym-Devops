from flask import Blueprint, render_template, request, jsonify
from .services import programs, get_program_details

main = Blueprint('main', __name__)

# -----------------------------
# Health Route (ADD THIS)
# -----------------------------
@main.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


# -----------------------------
# Existing Home Route
# -----------------------------
@main.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected = request.form['program']
        data = get_program_details(selected)

        return render_template(
            'result.html',
            program=selected,
            workout=data['workout'],
            diet=data['diet'],
            color=data['color']
        )

    return render_template('index.html', programs=programs.keys())