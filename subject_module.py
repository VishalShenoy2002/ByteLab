import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Subject:
    
    def __init__(self) -> None:
        self.subject_name: str = None
        self.course_name: str = None
        self.subject_code: str = None 
        self.semester: int = None
        
    def generate_subject_code(self):
        subject_code ="".join([x[0] for x in self.subject_name.strip().split(' ')])
        return subject_code
    
    def insert_into_table(self):
        query = f'INSERT INTO subjects(subject_code,subject_name,course_name,semester) VALUES("{self.subject_code}","{self.subject_name}","{self.course_name}",{self.semester});'
        cursor.execute(query)
        conn.commit()
        del query

        
class SubjectRetriever:
    
    def __init__(self) -> None:
        self.subject_code: str = None
        self.subject_name: str = None
        self.semester: int = None
        
    def get_code_by_name(self):
        
        query = f'SELECT subject_code FROM subjects WHERE subject_name="{self.subject_name}";'
        cursor.execute(query)
        
        record = cursor.fetchone()
        record = record[0]
        del query
        return record
    
    def get_name_by_code(self):
        
        query = f'SELECT subjec_name FROM subjects WHERE subject_code="{self.subject_code}";'
        cursor.execute(query)
        
        record = cursor.fetchone()
        del query
        return record
    
    def list_subject_for_sem(self):
        query = f'SELECT subject_code,subject_name FROM subjects WHERE semester={self.semester}'
        cursor.execute(query)
        
        records = cursor.fetchall()
        del query
        return records