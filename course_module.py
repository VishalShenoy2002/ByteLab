import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Course:
    
    def __init__(self) -> None:
        self.course_name: str = None
        self.full_form: str = None
        self.no_of_sems: int = None
        
    def add_to_db(self):
        
        query=f'INSERT INTO courses(course_name,full_form,num_of_sems)VALUES("{self.course_name}","{self.full_form}",{self.no_of_sems});'
        cursor.execute(query)
        conn.commit()
        
    def list_courses(self):
        query = "SELECT course_name FROM courses;"
        cursor.execute(query)
        
        records = cursor.fetchall()
        records = [x[0] for x in records]
        return records