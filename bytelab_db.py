import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

def execute_query(query:str):
    cursor.execute(query)


def insert_into_questions_table(record:dict):
    query = f"INSERT INTO questions(question,semester,programming_language) VALUES (\"{record['question']}\", {record['semester']}, \"{record['programming_language']}\");"
    execute_query(query)
    del query

def create_batch_table():
    query='''
            CREATE TABLE IF NOT EXISTS batches (batch_id VARCHAR(20) NOT NULL PRIMARY KEY, 
            course_name VARCHAR(50) NOT NULL,
            year_start INT NOT NULL,
            year_end INT NOT NULL,
            year_code VARCHAR(10) NOT NULL);
            '''
    execute_query(query)
    del query
    
    

def create_questions_table():
    query='''
            CREATE TABLE IF NOT EXISTS questions (question_id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            semester INT(2) NOT NULL,
            programming_language VARCHAR(50) NOT NULL);
            '''
    execute_query(query)
    del query

def create_courses_table():
    query='''
            CREATE TABLE IF NOT EXISTS courses (
            course_name VARCHAR(5) PRIMARY KEY  NOT NULL,
            full_form VARCHAR(250) NOT NULL,
            num_of_sems INT NOT NULL);
            '''
    execute_query(query)
    del query

def create_students_table():
    query='''
            CREATE TABLE IF NOT EXISTS students (uucms_no VARCHAR(50) NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL, 
            course VARCHAR(5) NOT NULL,
            semester INT NOT NULL,
            batch INT NOT NULL,
            FOREIGN KEY (course) REFERENCES courses(course_name));
            '''
    execute_query(query)
    del query

def create_submission_table():
    query='''
            CREATE TABLE IF NOT EXISTS submission (
            submission_id INT AUTO_INCREMENT PRIMARY KEY,
            student_roll_no VARCHAR(50) NOT NULL,
            question_number INT NOT NULL,
            programming_language VARCHAR(50) NOT NULL,
            semester INT NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_roll_no) REFERENCES students(uucms_no),
            FOREIGN KEY (question_number) REFERENCES questions(question_id));
            '''
    execute_query(query)
    del query
    
    
