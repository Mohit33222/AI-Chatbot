from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
from flask_session import Session
from chatbot_model import get_response

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

FAQ_FILE = 'data/faq_data.csv'

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'


# ✅ Route: Home
@app.route('/')
def index():
    return render_template('index.html')


# ✅ Route: Admin Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Admin login route """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# ✅ Route: Logout
@app.route('/logout')
def logout():
    """ Admin logout route """
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ✅ Route: Admin Portal
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """ Admin portal to manage FAQs """
    if not session.get('admin_logged_in'):
        flash('You must log in first.', 'warning')
        return redirect(url_for('login'))

    # Load FAQ data or create CSV if missing
    try:
        data = pd.read_csv(FAQ_FILE)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['question', 'answer'])
        data.to_csv(FAQ_FILE, index=False)

    # Handle new FAQ submissions
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')

        if question and answer:
            new_faq = pd.DataFrame([[question, answer]], columns=['question', 'answer'])
            data = pd.concat([data, new_faq], ignore_index=True)
            data.to_csv(FAQ_FILE, index=False)

        return redirect(url_for('admin'))

    faqs = data.to_dict(orient='records')

    return render_template('admin.html', faqs=faqs)


# ✅ Route: Edit FAQ
@app.route('/edit_faq/<int:index>', methods=['GET', 'POST'])
def edit_faq(index):
    """ Edit an existing FAQ """
    if not session.get('admin_logged_in'):
        flash('You must log in first.', 'warning')
        return redirect(url_for('login'))

    # Load the FAQ data
    try:
        data = pd.read_csv(FAQ_FILE)
    except FileNotFoundError:
        flash("No FAQ data found.", "danger")
        return redirect(url_for('admin'))

    # Check if index is valid
    if index < 0 or index >= len(data):
        flash("Invalid FAQ index.", "danger")
        return redirect(url_for('admin'))

    # Edit FAQ
    if request.method == 'POST':
        data.at[index, 'question'] = request.form.get('question')
        data.at[index, 'answer'] = request.form.get('answer')
        data.to_csv(FAQ_FILE, index=False)
        flash("FAQ updated successfully.", "success")
        return redirect(url_for('admin'))

    faq = data.iloc[index].to_dict()
    return render_template('edit_faq.html', faq=faq, index=index)


# ✅ Route: Delete FAQ
@app.route('/delete_faq/<int:index>', methods=['GET'])
def delete_faq(index):
    """ Delete an existing FAQ """
    if not session.get('admin_logged_in'):
        flash('You must log in first.', 'warning')
        return redirect(url_for('login'))

    # Load the FAQ data
    try:
        data = pd.read_csv(FAQ_FILE)
    except FileNotFoundError:
        flash("No FAQ data found.", "danger")
        return redirect(url_for('admin'))

    # Ensure the index is valid
    if index < 0 or index >= len(data):
        flash("Invalid FAQ index.", "danger")
        return redirect(url_for('admin'))

    # Remove the FAQ and save the file
    data.drop(index, inplace=True)
    data.to_csv(FAQ_FILE, index=False)

    flash("FAQ deleted successfully.", "success")
    return redirect(url_for('admin'))


# ✅ Route: Chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    """ Handles chatbot interaction """
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})


# ✅ Main execution point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
