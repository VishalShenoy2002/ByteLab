import mysql.connector as mysql

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class Question:
    
    def __init__(self,question:str, semester:int, programming_language:str, subject:str) -> None:
        self.question = question
        self.semester = semester
        self.programming_language = programming_language
        self.subject = subject
    
    def insert_into_questions_table(self):
        query = f"INSERT INTO questions(question,semester,programming_language) VALUES (\"{self.question}\", {self.semester}, \"{self.programming_language}\");"
        print(query)
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
        query = f'SELECT * FROM questions WHERE semester="{self.subject}";'
        cursor.execute(query)  
        records = cursor.fetchall()
        
        del query
        return records
