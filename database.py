import mysql.connector
from tkinter import messagebox


def connect_database():
    global mycursor,conn
    try:
        conn = mysql.connector.connect(host='localhost',password='admin',user='root')
        mycursor = conn.cursor()
    except: 
        messagebox.showerror('Error','Somthing went wrong, please open mysql app befor running again')
        return

   #create database and tables(fields)
    mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
    mycursor.execute('USE employee_data')
    mycursor.execute('CREATE TABLE IF NOT EXISTS data (Id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(50),Phone VARCHAR(50),Role VARCHAR(50),Gender VARCHAR(20),Salary DECIMAL(10,2))')


def generate_id():
    employees = fetch_employees()
    if not employees:
        return 1

    try:
        last_id = max(int(employee[0]) for employee in employees)
        return last_id + 1
    except ValueError:
        raise ValueError("Non-numeric ID found in the database")



def insert(id,name,phone,role,gender,salary):
    mycursor.execute('INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s)',(id,name,phone,role,gender,salary))
    conn.commit()
    
def id_exists(id):
    # Wrap the parameter in a tuple
    mycursor.execute('SELECT COUNT(*) FROM data WHERE id=%s', (id,))
    result = mycursor.fetchone()
    print(result)
    return result[0] > 0

def fetch_employees():
    mycursor.execute('SELECT * from data')
    result=mycursor.fetchall()
    return result

def update(new_name, new_phone, new_role, new_gender, new_salary):
    try:
        # Update query with correctly formatted parameters
        query = '''
            UPDATE data 
            SET phone = %s, role = %s, gender = %s, salary = %s 
            WHERE name = %s
        '''
        params = (new_phone, new_role, new_gender, new_salary, new_name)  # Ensure correct order
        mycursor.execute(query, params)
        conn.commit()  # Commit the transaction
        print("Record updated successfully.")  # Replace with logging or user feedback
    except Exception as e:
        conn.rollback()  # Roll back the transaction on error
        print(f"Error updating record: {e}")  # Replace with logging if needed


def delete(id):
    try:
        # Ensure `id` is passed as a single-element tuple
        mycursor.execute('DELETE FROM data WHERE id=%s', (id,))
        conn.commit()
        print("Record deleted successfully.")
    except Exception as e:
        conn.rollback()  # Roll back the transaction on error
        print(f"Error deleting record: {e}")


def search(option, value):
    # Ensure value is passed as a tuple
    mycursor.execute(f'SELECT * FROM data WHERE {option}=%s', (value,))
    result = mycursor.fetchall()
    return result


def deleteall_records():
    mycursor.execute('TRUNCATE TABLE data')
    conn.commit()

connect_database()