from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify

from questions_module import Question, QuestionRetriever
from course_module import Course
from subject_module import Subject, SubjectRetriever
 

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/editor")
def editor():
    
    return render_template("editor.html",title="ByteLab | Editor",language="python",question="C Question")


@app.route("/")
def index():
    return redirect("/login")

@app.route('/save',methods=["POST"])
def saveCode():
    code = request.form['code']
    language = request.form['language']
    
    return 'Code saved'

@app.route("/login",methods=["GET","POST"])
def login_page():
    return render_template("login_page.html",title="ByteLab | Login")

@app.route("/register",methods=["GET","POST"])
def registration_page():
    if request.method == "GET":
        return render_template("registration_page.html",title="ByteLab | Registration")
    
    elif request.method == "POST":
        return redirect("/login")
    
@app.route('/faculty-dashboard',methods=["GET","POST"])
def faculty_dashboard_page():
    if request.method == "GET":
        return render_template("faculty-dashboard.html",title="ByteLab | Faculty Dashboard",page_hero_title="Faculty Dashboard")
    
@app.route('/admin-dashboard',methods=["GET","POST"])
def admin_dashboard_page():
    if request.method == "GET":
        return render_template("admin-dashboard.html",title="ByteLab | Admin Dashboard",page_hero_title="Admin Dashboard")
        
@app.route('/faculty-dashboard/manage-questions',methods=["GET"])
def manage_questions_page():
    if request.method == "GET":
        return render_template("manage_questions.html",title="ByteLab | Manage Questions",page_hero_title="Manage Questions")
    
    
@app.route('/faculty-dashboard/manage-questions/add',methods=["GET","POST"])
def add_questions_page():
    if request.method == "GET":
        return render_template("add_questions.html",title="Manage Questions | Add",page_hero_title="Add Question")
    
    elif request.method == "POST":
        form_data = request.form
        record = {}
        record['question'] = form_data.get('question')
        record['semester'] = int(form_data.get('semester'))
        record['programming_language'] = form_data.get('programming_language')
        record['subject'] = form_data.get('subject')
        
        retriever = SubjectRetriever()
        retriever.subject_name = record['subject']
        record['subject'] = retriever.get_code_by_name()
        del form_data
        question = Question(record['question'],record['semester'],record['programming_language'],record['subject'])
        question.insert_into_questions_table()

        return render_template("add_questions.html",title="Manage Questions | Add",page_hero_title="Add Question")

@app.route('/faculty-dashboard/manage-questions/view',methods=["GET","POST"])
def view_questions_page():
    if request.method == "GET":
        return render_template("view_questions.html",title="Manage Questions | View",page_hero_title="View Questions",questions=[])
    
    elif request.method == "POST":
        form_data = request.form
        semester = form_data.get('semester')
        subject = form_data.get('subject')
        
        question_retriever = QuestionRetriever()
        subject_retriever = SubjectRetriever()
        
        subject_retriever.subject_name = subject
        subject = subject_retriever.get_code_by_name()
        
        records = question_retriever.get_by_subject_and_semester(subject=subject,semester=semester)
        
        return render_template("view_questions.html",title="Manage Questions | View",page_hero_title="View Questions",questions=records)


@app.route('/admin-dashboard/add-course',methods=["GET","POST"])
def add_course_page():
    if request.method == "GET":
        return render_template("add_course.html",title="Admin Dashboard | Add Course",page_hero_title="Add Course")
    
    elif request.method == "POST":
        form_data = request.form
        course = Course()
        course.course_name = form_data.get("course_name")    
        course.full_form = form_data.get("course_full_form")    
        course.no_of_sems = form_data.get("no_of_sems")    
        
        course.insert_into_table()
        
        del course, form_data
        
        return render_template("add_course.html",title="Admin Dashboard | Add Course",page_hero_title="Add Course")

@app.route('/admin-dashboard/add-subject',methods=["GET","POST"])  
def add_subject_page():
    if request.method == "GET":
        course = Course()
        course_list = course.list_courses()
        del course
        return render_template("add_subject.html",title="Admin Dashboard | Add Subject",page_hero_title="Add Subject",courses=course_list)
    
    elif request.method == "POST":
        form_data = request.form
        
        subject = Subject()
        subject.course_name = form_data.get('course_name')
        subject.subject_name = form_data.get('subject_name')
        subject.semester = form_data.get('semester')
        subject.subject_code = subject.generate_subject_code()
        
        subject.insert_into_table()
        del form_data
        course = Course()
        course_list = course.list_courses()
        del course
        return render_template("add_subject.html",title="Admin Dashboard | Add Subject",page_hero_title="Add Subject",courses=course_list)
        
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    
    