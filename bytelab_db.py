import mysql.connector as mysql

print('Starting Connection')
conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

def execute_query(query:str):
    cursor.execute(query)


def insert_into_questions_table(record:dict):
    query = f"INSERT INTO questions(question,semester,programming_language) VALUES (\"{record['question']}\", {record['semester']}, \"{record['programming_language']}\");"
    execute_query(query)
    del query

def create_batch_table():
    print('[*] Creating Batch Table')
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
    print('[*] Creating Questions Table')
    query='''
            CREATE TABLE IF NOT EXISTS questions (question_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_code VARCHAR(20) NOT NULL,
            question TEXT NOT NULL,
            semester INT(2) NOT NULL,
            programming_language VARCHAR(50) NOT NULL,
            FOREIGN KEY (subject_code) REFERENCES subjects (subject_code));
            '''
    execute_query(query)
    del query

def create_courses_table():
    print('[*] Creating Courses Table')
    query='''
            CREATE TABLE IF NOT EXISTS courses (
            course_name VARCHAR(5) PRIMARY KEY  NOT NULL,
            full_form VARCHAR(250) NOT NULL,
            num_of_sems INT NOT NULL);
            '''
    execute_query(query)
    del query

def create_students_table():
    print('[*] Creating Students Table')
    query='''
            CREATE TABLE IF NOT EXISTS students (uucms_no VARCHAR(50) NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL, 
            course VARCHAR(5) NOT NULL,
            semester INT NOT NULL,
            batch INT NOT NULL,
            password varchar(32) NOT NULL,
            FOREIGN KEY (course) REFERENCES courses(course_name));
            '''
    execute_query(query)
    del query

def create_submission_table():
    print('[*] Creating Submission Table')
    query='''
            CREATE TABLE IF NOT EXISTS submissions (
            submission_id INT AUTO_INCREMENT PRIMARY KEY,
            student_roll_no VARCHAR(50) NOT NULL,
            question_number INT NOT NULL,
            programming_language VARCHAR(50) NOT NULL,
            semester INT NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            submission TEXT NOT NULL,
            approval_status varchar(30) NOT NULL DEFAULT "Pending",
            FOREIGN KEY (student_roll_no) REFERENCES students(uucms_no),
            FOREIGN KEY (question_number) REFERENCES questions(question_id));
            '''
    execute_query(query)
    del query
    
def create_subject_table():
    print('[*] Creating Subject Table')
    query='''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_code VARCHAR(20) NOT NULL PRIMARY KEY,
        subject_name VARCHAR(100) NOT NULL,
        course_name VARCHAR(5) NOT NULL,
        semester int(2) not null default 1,
        FOREIGN KEY (course_name) REFERENCES courses (course_name));
    '''
    execute_query(query)
    del query
    
    
def create_faculty_table():
    print('[*] Creating Faculty Table')
    query='''
    CREATE TABLE IF NOT EXISTS faculty (
        faculty_id VARCHAR(25) NOT NULL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        department VARCHAR(5) NOT NULL,
        email VARCHAR(50) NOT NULL,
        password VARCHAR(32) NOT NULL,
        FOREIGN KEY (department) REFERENCES courses (course_name));
    '''
    execute_query(query)
    del query
    
    
if __name__ == "__main__":
    create_batch_table()
    create_courses_table()
    create_subject_table()
    create_students_table()
    create_questions_table()
    create_submission_table()
    create_faculty_table()
    
conn.commit()
conn.close()