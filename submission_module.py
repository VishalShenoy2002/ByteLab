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
        
        query = f'SELECT submission_date,student_roll_no,semester,question_number FROM submissions WHERE semester={semester} ORDER BY submission_date DESC LIMIT 10;'
        cursor.execute(query)
        
        records = cursor.fetchall()
        records = [dict(zip(("Submission Timestamp","Roll Number","Semester","Question Number"),(submission_date,student_roll_no,semester,question_number))) for submission_date,student_roll_no,semester,question_number in records]
        return records
    
    def get_lastet_by_student(self,roll_no:str):
        
        query = f'SELECT submission_date,student_roll_no,semester,question_number FROM submissions WHERE student_roll_no="{roll_no}" ORDER BY submission_date DESC LIMIT 10;'
        print(query)
        cursor.execute(query)
        records = cursor.fetchall()
        records = [dict(zip(("Submission Timestamp","Roll Number","Semester","Question Number"),(submission_date,student_roll_no,semester,question_number))) for submission_date,student_roll_no,semester,question_number in records]
        return records     
    
    def get_by_student(self,roll_no:str):
        query = f'SELECT submission_date,student_roll_no,semester,question_number FROM submissions WHERE student_roll_no="{roll_no}" ORDER BY submission_date DESC;'
        cursor.execute(query)
        
        records = cursor.fetchall() 
        records = [dict(zip(("Submission Timestamp","Roll Number","Semester","Question Number"),(submission_date,student_roll_no,semester,question_number))) for submission_date,student_roll_no,semester,question_number in records]
        print(records)
        return records     

    
    def get_by_semester(self,semster:int):
        query = f'SELECT submission_date,student_roll_no,semester,question_number FROM submissions WHERE semester={semster} ORDER BY submission_date DESC;'
        cursor.execute(query)
        
        records = cursor.fetchall() 
        records = [dict(zip(("Submission Timestamp","Roll Number","Semester","Question Number"),(submission_date,student_roll_no,semester,question_number))) for submission_date,student_roll_no,semester,question_number in records]
        
        
        return records     
    