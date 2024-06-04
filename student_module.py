import mysql.connector as mysql
import hashlib

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Student:
    
    def __init__(self) -> None:
        self.uucms_no: str = None
        self.name: str = None
        self.course: str = None
        self.semester: int = None
        self.batch: int = None
        
    
    def add_to_db(self,student_password):
        
        query = f'INSERT INTO students(uucms_no,name,course,semester,batch,password) VALUES("{self.uucms_no}","{self.name}","{self.course}",{self.semester},{self.batch},"{student_password}");'
        cursor.execute(query)
        conn.commit()
        del query
        
    def generate_student_password(self):
        password = self.name.split(' ')[0].title() + "@123"
        password = password.encode('utf-8')
        password = hashlib.md5(password).hexdigest()
        return password
        

class StudentAuthentication:
    
    def __init__(self):
        self.student = Student()
        self.password: str = None
        
    def authenticate(self):
        query = f'SELECT 1 FROM students WHERE uucms_no="{self.student.uucms_no}" AND password="{self.password}";'
        cursor.execute(query)
        
        response = cursor.fetchone()[0]
        
        if response == 1:
            return True
        else:
            return False
        
class StudentRetriever:
    
    def __init__(self) -> None:
        self.uucms_no: str = None
        self.semester: int = None
        self.type: str = "student"
        
    def get_by_uucms_no(self):
        query = f'SELECT * FROM students WHERE uucms_no = "{self.uucms_no}";'
        
        cursor.execute(query)
        del query
        record = cursor.fetchone()
        record = tuple(list(record) + [self.type])
        record = dict(zip(("uucms_no","name","course","semester","batch","password","type"),record))
        return record
    
    def get_batch_details(self):
        
        query = f'SELECT DISTINCT(batch), course FROM students;'
        cursor.execute(query)
        
        del query
        record = [dict(zip(("Batch","Course"),(batch,course))) for batch,course in cursor.fetchall()]
        return record

    def get_by_batch(self,batch:int,course:str):
        
        query = f'SELECT uucms_no,name,course,batch FROM students WHERE batch={batch} AND course="{course}";'
        cursor.execute(query)
        
        records = cursor.fetchall()
        # print(records)
        records = [dict(zip(("UUCMS No","Name","Course","Batch"),(uucms_no,name,course,batch))) for uucms_no,name,course,batch in records]
        # records =
        
        return records
        
        