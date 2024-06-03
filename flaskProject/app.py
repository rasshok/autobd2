from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('auto_repair.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM requests').fetchall()
    conn.close()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=('GET', 'POST'))
def add_request():
    if request.method == 'POST':
        request_number = request.form['request_number']
        date_added = request.form['date_added']
        car_type = request.form['car_type']
        car_model = request.form['car_model']
        problem_description = request.form['problem_description']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = 'new'
        assigned_mechanic = ''

        conn = get_db_connection()
        conn.execute('INSERT INTO requests (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status, assigned_mechanic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status, assigned_mechanic))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_request.html')

@app.route('/edit/<int:request_id>', methods=('GET', 'POST'))
def edit_request(request_id):
    conn = get_db_connection()
    request_data = conn.execute('SELECT * FROM requests WHERE id = ?', (request_id,)).fetchone()

    if request.method == 'POST':
        request_number = request.form['request_number']
        date_added = request.form['date_added']
        car_type = request.form['car_type']
        car_model = request.form['car_model']
        problem_description = request.form['problem_description']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = request.form['status']
        assigned_mechanic = request.form['assigned_mechanic']

        conn.execute('UPDATE requests SET request_number = ?, date_added = ?, car_type = ?, car_model = ?, problem_description = ?, client_name = ?, phone_number = ?, status = ?, assigned_mechanic = ? WHERE id = ?',
                     (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status, assigned_mechanic, request_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_request.html', request=request_data)

@app.route('/view/<int:request_id>')
def view_request(request_id):
    conn = get_db_connection()
    request_data = conn.execute('SELECT * FROM requests WHERE id = ?', (request_id,)).fetchone()
    conn.close()
    return render_template('view_request.html', request=request_data)

if __name__ == '__main__':
    app.run()
