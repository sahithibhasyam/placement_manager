from dbconnector import connect_database, disconnect_database
from mysql.connector import Error
import settings as sett
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        sett.mycursor.execute(query, (email, hashed_password))
        user = sett.mycursor.fetchone()
        if user:
            return user
        else:
            return None
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def register_user(name, studentID, mobile_no, email, dob, address, password):
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "INSERT INTO user (name, studentID, mobile_no, email, dob, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (name, studentID, mobile_no, email, dob, address, hashed_password))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def login_company(companyID, password):
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "SELECT * FROM company WHERE companyID = %s AND password = %s"
        sett.mycursor.execute(query, (companyID, hashed_password))
        company = sett.mycursor.fetchone()
        if company:
            return company
        else:
            return None
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def register_company(companyID, name, industries, address, contact_person, contact_address, password):
    connect_database()
    try:
        hashed_password = hash_password(password)
        query = "INSERT INTO company (companyID, name, industries, address, contact_person, contact_address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (companyID, name, industries, address, contact_person, contact_address, hashed_password))
        sett.connection.commit()
        return companyID
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()


def get_user_profile(studentID):
    connect_database()
    try:
        query = "SELECT * FROM user WHERE studentID = %s"
        sett.mycursor.execute(query, (studentID,))
        user = sett.mycursor.fetchone()

        query = "SELECT a.appid, j.title, a.appdate, a.status FROM application a JOIN job j ON a.jobID = j.jobID WHERE a.studentID = %s"
        sett.mycursor.execute(query, (studentID,))
        applications = sett.mycursor.fetchall()

        return user, applications
    except Error as e:
        print(f"Error: '{e}'")
        return None, None
    finally:
        disconnect_database()

def update_user_profile(studentID, name, mobile_no, email, dob, address, password):
    connect_database()
    try:
        hashed_password = hash_password(password) if password else None
        query = "UPDATE user SET name = %s, mobile_no = %s, email = %s, dob = %s, address = %s"
        params = [name, mobile_no, email, dob, address]
        if hashed_password:
            query += ", password = %s"
            params.append(hashed_password)
        query += " WHERE studentID = %s"
        params.append(studentID)

        sett.mycursor.execute(query, tuple(params))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_companies():
    connect_database()
    try:
        query = "SELECT * FROM company"
        sett.mycursor.execute(query)
        companies = sett.mycursor.fetchall()
        return companies
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        disconnect_database()

def get_company_details(companyID):
    connect_database()
    try:
        query = "SELECT * FROM company WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        company = sett.mycursor.fetchone()

        query = "SELECT * FROM job WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        jobs = sett.mycursor.fetchall()

        return company, jobs
    except Error as e:
        print(f"Error: '{e}'")
        return None, None
    finally:
        disconnect_database()

def apply_for_job(appID,studentID, jobID):
    connect_database()
    try:
        appdate = datetime.now().strftime('%Y-%m-%d')
        query = "INSERT INTO application (appid, studentID, jobID, appdate, status) VALUES (%s ,%s, %s, %s, 'applied')"
        sett.mycursor.execute(query, (appID,studentID, jobID, appdate,))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_company_jobs(companyID):
    connect_database()
    try:
        query = "SELECT * FROM job WHERE companyID = %s"
        sett.mycursor.execute(query, (companyID,))
        jobs = sett.mycursor.fetchall()
        return jobs
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        disconnect_database()

def create_job(jobID, companyID, title, description, required_skills, salary, location):
    connect_database()
    try:
        query = "INSERT INTO job (jobID, companyID, title, description, required_skills, salary, location) VALUES (%s,%s, %s, %s, %s, %s, %s)"
        sett.mycursor.execute(query, (jobID, companyID, title, description, required_skills, salary, location))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()

def get_company_applications(companyID):
    connect_database()
    try:
        query = """
        SELECT a.appid, a.studentID, j.title, a.appdate, a.status, u.name, u.email, u.mobile_no, u.dob
        FROM application a
        JOIN job j ON a.jobID = j.jobID
        JOIN user u ON a.studentID = u.studentID
        WHERE j.companyID = %s
        ORDER BY a.jobID
        """
        sett.mycursor.execute(query, (companyID,))
        applications = sett.mycursor.fetchall()
        return applications
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        disconnect_database()

def update_application_status_db(appid, status):
    connect_database()
    try:
        query = "UPDATE application SET status = %s WHERE appid = %s"
        sett.mycursor.execute(query, (status, appid))
        sett.connection.commit()
        return True
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        disconnect_database()


