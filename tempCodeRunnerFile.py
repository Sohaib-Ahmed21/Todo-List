from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'todo'

mysql = MySQL(app)

# Routes

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, todo, complete_status FROM todos WHERE user_id = (SELECT id FROM user WHERE username = %s)", [username])
        todos = cur.fetchall()
        print(todos[0][1])
        cur.close()
        return render_template('index.html', username=username, todos=todos)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM user WHERE username = %s AND password = %s", [username, password])
        user = cur.fetchone()
        cur.close()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid login credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", [username, email, password])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_todo', methods=['POST'])
def add_todo():
    if 'username' in session:
        todo = request.form['todo']
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todos (todo, user_id) VALUES (%s, (SELECT id FROM user WHERE username = %s))", [todo, username])
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

@app.route('/toggle_todo/<int:todo_id>')
def toggle_todo(todo_id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE todos SET complete_status = NOT complete_status WHERE id = %s", [todo_id])
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

@app.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM todos WHERE id = %s", [todo_id])
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))


# Function to get tasks from the database
def get_tasks(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, todo, complete_status FROM todos WHERE username = %s", (username,))
    tasks = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return tasks

# Route for modifying a task
@app.route('/modify_todo/<int:task_id>', methods=['GET', 'POST'])
def modify_todo(task_id):
    if request.method == 'POST':
        new_todo = request.form['new_todo']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE todos SET todo = %s WHERE id = %s", (new_todo, task_id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')

    # Get the task to be modified
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT todo FROM todos WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()

    return render_template('modify.html', task=task, task_id=task_id)

# Add this route to render the modification form
@app.route('/modify_todo/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        new_todo = request.form['new_todo']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE todos SET todo = %s WHERE id = %s", (new_todo, task_id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')

    return render_template('modify.html', task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True)
