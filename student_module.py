import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Student:
    
    def __init__(self) -> None:
        self.uucms_no: str = None
        self.name: str = None
        self.course: str = None
        self.semester: int = None
        self.batch: int = None
    
    def add_student_to_db(self):
        
        query = f'INSERT INTO students(uucms_no,name,course,semester,batch) VALUES("{self.uucms_no}","{self.name}","{self.course}",{self.semester},{self.batch});'
        cursor.execute(query)
        conn.commit()
        del query