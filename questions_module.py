import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Question:
    
    def __init__(self,question:str, semester:int, programming_language:str, subject:str) -> None:
        self.question = question
        self.semester = semester
        self.programming_language = programming_language
        self.subject = subject
    
    def add_to_db(self):
        query = f"INSERT INTO questions(question,subject_code,semester,programming_language) VALUES (\"{self.question}\", \"{self.subject}\",{self.semester}, \"{self.programming_language}\");"
        print(query)
        cursor.execute(query)
        conn.commit()
        del query
        
    def remove_from_db(self,question_id):
        query = f'DELETE * FROM questions WHERE question_id = {question_id} AND semester = {self.semester};'
        cursor.execute(query)
        conn.commit()
        del query
        
class QuestionRetriever:
    
    def __init__(self) -> None:
        pass
        
    def get_by_programming_language(self,programming_language:str):
        self.programming_language = programming_language
        query = f'SELECT * FROM questions WHERE programming_language="{self.programming_language}";'
        cursor.execute(query)  
        records = cursor.fetchall()
        
        del query
        return records
        
    def get_by_semester(self,semester:int):
        self.semester = semester
        query = f'SELECT * FROM questions WHERE semester={self.semester};'
        cursor.execute(query)  
        records = cursor.fetchall()
        
        del query
        return records
        
    def get_by_semester(self,semester:int):
        self.semester = semester
        query = f'SELECT * FROM questions WHERE semester={self.semester};'
        cursor.execute(query)  
        records = cursor.fetchall()
        
        del query
        return records
        
    def get_by_subject(self,subject:str):
        self.subject = subject
        query = f'SELECT * FROM questions WHERE subject_code="{self.subject}";'
        cursor.execute(query)  
        records = cursor.fetchall()
        
        del query
        return records
    
    def get_by_subject_and_semester(self,subject:str, semester:int):
        self.subject =subject
        self.semester = semester
        query = f'SELECT * FROM questions WHERE subject_code="{self.subject}" and semester={self.semester};'
        cursor.execute(query)  
        records = cursor.fetchall()

        del query
        return records