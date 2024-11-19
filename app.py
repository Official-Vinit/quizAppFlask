from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'  # For session handling


# Load questions from a JSON file
def load_questions():
    with open('questions.json') as file:
        return json.load(file)


QUESTIONS = load_questions()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session['score'] = 0
    session['current_question'] = 0
    return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session:
        return redirect(url_for('home'))

    current_question_index = session['current_question']
    if current_question_index >= len(QUESTIONS):
        return redirect(url_for('result'))

    question = QUESTIONS[current_question_index]

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == question['answer']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', question=question, question_number=current_question_index + 1,
                           total_questions=len(QUESTIONS))


@app.route('/result')
def result():
    if 'score' not in session:
        return redirect(url_for('home'))
    score = session['score']
    total_questions = len(QUESTIONS)
    return render_template('result.html', score=score, total_questions=total_questions)


if __name__ == '__main__':
    app.run(debug=True)
