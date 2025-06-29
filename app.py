from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

# Load tasks
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks
def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task = {
            'description': request.form['description'],
            'due_date': request.form['due_date'],
            'completed': False
        }
        tasks = load_tasks()
        tasks.append(task)
        save_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    tasks = load_tasks()
    tasks[task_id]['completed'] = True
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    tasks = load_tasks()
    task = tasks[task_id]
    if request.method == 'POST':
        task['description'] = request.form['description']
        task['due_date'] = request.form['due_date']
        save_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('edit.html', task=task, task_id=task_id)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks.pop(task_id)
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
