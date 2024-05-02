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
