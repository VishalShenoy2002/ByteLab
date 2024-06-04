from groq import Groq
import mysql.connector as mysql
import markdown
from fpdf import FPDF

conn = mysql.connect(host="localhost",user="root",passwd="asdasd123",database="bytelab")
cursor = conn.cursor()

class ReportGenerator:
    
    def __init__(self) -> None:
        self.semester: int = None
        self.uucms_no: str = None
        
        self.API_KEY = "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"
        
        self.ai = Groq(api_key=self.API_KEY)
        
    def get_by_uucms_no(self):
        query = f'SELECT * FROM submissions WHERE student_roll_no="{self.uucms_no}";'
        cursor.execute(query)
        
        records = cursor.fetchall()
        records = [dict(zip(("submission_id","student_roll_no","question_number","programming_language","semester","submission_date","submission","approval_status"),tuple(record))) for record in records]
        # print(records)
        return records
    def _generate_report_text(self):
        messages = [
            {
                "role": "system",
                "content": "Analyze the provided list of Python dictionaries containing student details, submission dates, and codes. Generate a report in Markdown format with a general overview, detailed analysis (including number of submissions by date and by question ID), notable observations, recommendations, and conclusion."
            },
            {
                "role": "user",
                "content": str(self.get_by_uucms_no())
            }
        ]
        details = self.ai.chat.completions.create(messages=messages,model="mixtral-8x7b-32768",temperature=0.5,max_tokens=15000)
        
        return details.choices[0].message.content
    
    def generate_report(self):
        markdown_text = self._generate_report_text()
        
        html_text = markdown.markdown(markdown_text)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.write_html(html_text)
        pdf.output("output.pdf")
       
    
        
        
        
        
    