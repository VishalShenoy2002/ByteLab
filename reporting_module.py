from groq import Groq
import mysql.connector as mysql
import markdown
import model


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
        details = self.get_by_uucms_no()
        overview = model.generate_overview(details)
        code_recommendation = model.generate_code_recommendations(details)
        general_observation = model.generate_common_observation(details)
        strength_and_weakness= model.generate_strength_and_weakness(details)

        
        text = model.format_output(overview,code_recommendation,general_observation,strength_and_weakness)
        
        return text
    
    def generate_report(self):
        markdown_text = self._generate_report_text()
        
        html_text = markdown.markdown(markdown_text)

       
    
        

        
    