from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def check_password_strength(password):
    special_chars = list('@%*$#&^')
    isdigit_there = any(char.isdigit() for char in password)
    isupper_there = any(char.isupper() for char in password)
    islower_there = any(char.islower() for char in password)
    isspchar_there = any(char in special_chars for char in password)
    all_true = all([isdigit_there, isspchar_there, islower_there, isupper_there])

    if len(password) < 6:
        return "weak", "Password is too short. It should be at least 6 characters long."
    elif len(password) >= 12 and all_true:
        return "very strong", "Password is very strong."
    elif len(password) >= 8 and all_true:
        return "strong", "Password is strong."
    else:
        feedback = []
        if not isdigit_there:
            feedback.append("Add at least one digit.")
        if not isupper_there:
            feedback.append("Add at least one uppercase letter.")
        if not islower_there:
            feedback.append("Add at least one lowercase letter.")
        if not isspchar_there:
            feedback.append("Add at least one special character from @%*$#&^.")
        if len(password) < 8:
            feedback.append("Password should be at least 8 characters long for better security.")
        return "average", "Password is average. " + " ".join(feedback)

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password', '')
    strength, feedback = check_password_strength(password)
    return jsonify({'strength': strength, 'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True)
