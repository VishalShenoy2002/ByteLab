import mysql.connector as mysql
import hashlib

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Faculty:
    
    def __init__(self) -> None:
        
        self.faculty_id: str = None
        self.name:str = None
        self.email: str = None
        self.department: str = None
        self.password: str = None
        
    def add_to_db(self):
        
        query = f'INSERT INTO faculty(faculty_id,name,department,email,password) VALUES("{self.faculty_id}","{self.name}","{self.department}","{self.email}","{self.password}");'
        cursor.execute(query)
        conn.commit()
        
        
class FacultyAuthentication:
    
    def __init__(self):
        self.faculty = Faculty()
        self.password: str = None
        
    def authenticate(self):
        query = f'SELECT 1 FROM faculty WHERE faculty_id="{self.faculty.faculty_id}" AND password="{self.password}";'
        cursor.execute(query)
        
        response = cursor.fetchone()[0]
        
        if response == 1:
            return True
        else:
            return False
        
class FacultyRetriever:
    
    def __init__(self) -> None:
        self.faculty_id: str = None
        self.department: str = None
        self.type: str = "faculty"
        
    def get_by_faculty_id(self):
        query = f'SELECT * FROM faculty WHERE faculty_id = "{self.faculty_id}";'
        cursor.execute(query)
        del query
        record = cursor.fetchone()
        print(record)
        record = tuple(list(record) + [self.type])
        record = dict(zip(("faculty_id","name","department","email","password","type"),record))
        return record
        
        