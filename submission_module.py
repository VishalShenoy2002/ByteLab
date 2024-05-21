import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Submission:
    def __init__(self) -> None:
        self.student_roll_no: str = None
        self.question_id: int = None
        self.programming_language: str = None
        self.semester: int = None
        self.submission: str = None
        self.approval_status: str = None
        
    def add_to_db(self):
        query = f'INSERT INTO submissions (student_roll_no,question_number,programming_language,semester,submission,approval_status) VALUES ("{self.student_roll_no}",{self.question_id},"{self.programming_language}",{self.semester},%s,"{self.approval_status}");'
        
        print("Inserting")
        cursor.execute(query,[self.submission])
        conn.commit()
        del query
        
class SubmissionRetriever:
    
    def __init__(self) -> None:
        pass
    
    def get_latest_by_semester(self,semester:int):
        pass
    
    def get_lastet_by_student(self,roll_no:str):
        pass
    
    def ger_lastest_by_subject(self,subject_code:str):
        pass
    
    def get_by_semester(self,semester:int):
        pass
    
    def get_by_student(self,roll_no:str):
        pass
    
    def get_by_subject(self,subject_code:str):
        pass