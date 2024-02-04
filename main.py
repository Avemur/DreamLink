from flask import Flask, request, g, redirect, url_for, render_template, jsonify
from pymongo import MongoClient
from data import scores

valid_users = {'A': '1', 'Anirudh': 'Password', 'Ethan': 'Password', 'Faiz': 'Password', "Aiden": "Password"}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in valid_users and valid_users[username] == password:
            return redirect(url_for('journal', username=username))
    return render_template('login.html')

@app.route('/journal/<username>', methods=['POST', 'GET'])
def journal(username):
    if request.method == 'POST':
        db = get_database()
        dreamDate = request.form.get('dreamDate')
        dreamTitle = request.form.get('dreamTitle')
        dreamContent = request.form.get('dreamContent')
        if (dreamDate and dreamTitle and dreamContent):
            document = {
                'username': username,
                'dreamDate': dreamDate,
                'dreamTitle': dreamTitle,
                'dreamContent': dreamContent
            }
            db.insert_one(document)

    return render_template('journal.html', username=username)

@app.route('/analysis/<username>')
def analysis(username):
    temp = scores(username)
    archetype = ""
    Visionary = (temp[3] + temp[1])/2
    Stoic = (temp[0] + temp[2])/2
    Trailblazer = (temp[1] + temp[5] + temp[6])/3
    Peacemaker = (temp[3] + temp[4] + temp[0])/3
    Empathetic = (temp[6] + temp[3] + temp[4])/3
    Guardian = (temp[1] + temp[2] + temp[5])/3
    archetypes_numbers = [Visionary, Stoic, Trailblazer, Peacemaker, Empathetic, Guardian]
    archetype_names = ["Visionary", "Stoic", "Trailblazer", "Peacemaker", "Empathetic", "Guardian"]
    archetype = archetype_names[archetypes_numbers.index(max(archetypes_numbers))]
    return render_template('analysis.html', archetype=archetype)

def get_database():
    client = MongoClient("mongodb+srv://test_user:test_pass@dreamcluster.vfcbjke.mongodb.net/?retryWrites=true&w=majority")
    db = client.dreamDB.dreams
    
    return db

if __name__ == "__main__":
    app.run(port=3000, debug=True)