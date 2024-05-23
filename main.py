from flask import Flask, render_template, request, redirect, url_for, jsonify, url_for, session, flash
from flask_restful import Resource
import mysql.connector

app = Flask(__name__)
app.secret_key = 'CRUD'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'flaskcrudapi',
}

con = mysql.connector.connect(**db_config)
cur = con.cursor()

# Create employee table in MySQL
cur.execute('''
    CREATE TABLE IF NOT EXISTS employee (
        emp_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        position VARCHAR(50) NOT NULL,
        department VARCHAR(50) NOT NULL,
        salary DECIMAL(10, 2),
        phone VARCHAR(15),
        email VARCHAR(50),
        gender VARCHAR(10)
    )
''')
cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
con.commit()
cur.close()


# REST API routes

@app.route('/', methods=['GET'])
def home():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global success_message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = mysql.connector.connect(**db_config)
        cur = con.cursor()

        cur.execute('SELECT name,password FROM employee WHERE name=%s AND password=%s', (username, password))
        user = cur.fetchone()
        con.close()

        if user:
            session['username'] = username
            success_message = 'Login successful!'
            flash(success_message, 'success')
            return render_template('employess.html', msg=success_message)

        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('index.html')


@app.route('/api/employees', methods=['GET'])
def get_employees():
    cur = con.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    # employees_list = [dict(zip(["id", "name", "position", "department"], row)) for row in data]
    employees_list = [dict(zip(column_names, row)) for row in data]
    cur.close()
    return jsonify(employees_list)


@app.route('/api/employee/', methods=['GET'])
def get_employee():
    emp_id = request.args.get('emp_id')
    cur = con.cursor()
    cur.execute("SELECT * FROM employee where emp_id=%s", [emp_id])
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    employees_list = [dict(zip(column_names, row)) for row in data]
    cur.close()
    return jsonify(employees_list)


@app.route('/api/add_employee/', methods=['POST'])
def add_employee():
    if request.method == "POST":
        data = request.get_json()
        print('add data', data)
        name = data['name']
        Password = data['Password']
        position = data['position']
        department = data['department']
        salary = data['salary']
        phone = data['phone']
        email = data['email']
        gender = data['gender']

        cur = con.cursor()

        cur.execute(
            "INSERT INTO employee (name, Password, position, department, salary, phone, email, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, Password, position, department, salary, phone, email, gender))
        con.commit()
        cur.close()
        # return redirect(url_for('home'))
        return jsonify({"message": "Employee Added successfully"})

    else:
        # return render_template('all_details.html')
        return jsonify({"message": "Method not allowed"})


@app.route('/api/updateEmployee/', methods=['PUT'])
# @app.route('/api/employees/<int:employee_id>', methods=['PUT'])
# def update_employee(employee_id):
def update_employee():
    if request.method == "PUT":
        data = request.get_json()
        print('data', data)
        name = data['name']
        password = data['password']
        position = data['position']
        department = data['department']
        salary = data['salary']

        phone = data['phone']
        email = data['email']
        gender = data['gender']
        employee_id = data['emp_id']
        cur = con.cursor()
        cur.execute(
            "UPDATE employee SET name=%s, password=%s, position=%s, department=%s, salary=%s, phone=%s, email=%s, gender=%s WHERE emp_id=%s",
            (name, password, position, department, salary, phone, email, gender, employee_id,))
        con.commit()
        cur.close()

        return jsonify({"message": "Employee updated successfully"})
    else:
        return jsonify({"message": "Employee Not updated"})


@app.route('/api/deleteEmployee/', methods=['DELETE'])
# @app.route('/api/employee/', methods=['DELETE'])
def delete_employee():
    emp_id = request.args.get('emp_id')
    print('aaaaaaaaaaaemp_id', emp_id)
    if emp_id:
        cur = con.cursor()
        cur.execute("DELETE FROM employee WHERE emp_id = %s", (emp_id,))
        con.commit()
        cur.close()
        return jsonify({"message": "Employee deleted successfully"})
    return jsonify({"message": "Select Employee"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)
