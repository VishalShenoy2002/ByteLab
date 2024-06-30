from flask import Flask
from flask import render_template, render_template_string
from flask import request, redirect
from flask import session

from questions_module import Question, QuestionRetriever
from course_module import Course
from subject_module import Subject, SubjectRetriever
from student_module import Student, StudentAuthentication, StudentRetriever
from faculty_module import Faculty,FacultyAuthentication, FacultyRetriever
from submission_module import Submission, SubmissionRetriever
from reporting_module import ReportGenerator
from notification_module import TelegramBot


import os
from werkzeug.utils import secure_filename
import csv
import datetime
import hashlib

if os.path.isdir(os.path.join(os.getcwd(),"uploads")) == False:
    os.makedirs(os.path.join(os.getcwd(),"uploads"))

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),"uploads")

app.secret_key = "bc9a80d9d724bd875ee5cd1637f87101"
app.permanent_session_lifetime = datetime.timedelta(days=5)


@app.route("/")
def index():
    try:
        if session['type'] != "":
            
            if "student" in session['type']:
                return redirect("/student-dashboard")
            elif "faculty" in session['type']:
                return redirect("/faculty-dashboard")
            elif "admin" in session['type']:
                return redirect('/admin-dashboard')
                
        else:
            return redirect("/login")
    except KeyError:
        return redirect("/login")


@app.route('/submit',methods=["POST"])
def saveCode():
    
    if request.method == "POST":
        code = request.form['code']
        language = request.form['language']
        question_id = request.form['question_id']
        question = request.form['question']
        
        print(code.replace(r"\n","\\n"))
        submission = Submission()
        submission.student_roll_no = session['uucms_no']
        submission.semester = session['semester']
        submission.question_id = question_id
        submission.programming_language = language
        submission.submission = code
        submission.approval_status = "Submitted"
        
        bot = TelegramBot()
        
        message = f"""
Greetings,
This message is to inform you that {session["student_name"].title()} from {session["course"].upper()} {session["semester"]} semester has jus submitted a lab program.\n\n
Program Details\n
Question ID: {question_id}
Question: {question}
\n\n
Student Details
UUCMS Number: {session["uucms_no"]}
Student Name: {session["student_name"]}
        
        """
        bot.notify(message)
        
        submission.add_to_db()
        
        return redirect("student-dashboard/solve-questions")

@app.route("/login",methods=["GET","POST"])
def login_page():
    session.permanent = True
    if request.method == "GET":
        return render_template("login_page.html",title="ByteLab | Login")
    
    elif request.method == "POST":
        form_data = request.form
        user_type = form_data.get('type')
        password = form_data.get('password_login').encode('utf-8')
        password = hashlib.md5(password).hexdigest()
        
        if form_data.get('login_id') == "admin" and password == hashlib.md5("admin".encode('utf-8')).hexdigest():
            session['type'] = "admin"
            return redirect('/')
        
        if user_type == "student":
            student_auth = StudentAuthentication()
            student_auth.student.uucms_no = form_data.get('login_id')
            student_auth.password = password
            
            std_auth = student_auth.authenticate()
            if std_auth == True:
                retriever = StudentRetriever()
                student = Student()
                retriever.uucms_no = student_auth.student.uucms_no
                record = retriever.get_by_uucms_no()
                session['uucms_no'] = record.get("uucms_no")
                session['student_name'] = record.get('name')
                session['course'] = record.get('course')
                session['semester'] = record.get('semester')
                session['batch'] = record.get('batch')
                session['password'] = record.get('password') 
                session['type'] = user_type
                del retriever

                return redirect('/')
            else:
                return render_template("login_page.html",title="ByteLab | Login")
            
        elif user_type == "faculty":
            faculty_auth = FacultyAuthentication()
            faculty_auth.faculty.faculty_id = form_data.get('login_id')
            faculty_auth.password = password
            
            fac_auth = faculty_auth.authenticate()
            
            if fac_auth == True:
                retriever = FacultyRetriever()
                retriever.faculty_id = faculty_auth.faculty.faculty_id
                record = retriever.get_by_faculty_id()
                session['faculty_id'] = record.get("faculty_id")
                session['faculty_name'] = record.get('name')
                session['department'] = record.get('department')
                session['email'] = record.get('email')
                session['password'] = record.get('password') 
                session['type'] = user_type
                
                return redirect('/')
            else:
                return render_template("login_page.html",title="ByteLab | Login")
                
                

# Dashboard Routes 
@app.route('/faculty-dashboard',methods=["GET","POST"])
def faculty_dashboard_page():
    if request.method == "GET":
        return render_template("faculty-dashboard.html",title="ByteLab | Faculty Dashboard",page_hero_title="Faculty Dashboard")
    
@app.route('/admin-dashboard',methods=["GET","POST"])
def admin_dashboard_page():
    if request.method == "GET":
        return render_template("admin-dashboard.html",title="ByteLab | Admin Dashboard",page_hero_title="Admin Dashboard")

# Faculty Dashboard Routes 
@app.route('/faculty-dashboard/manage-questions',methods=["GET"])
def manage_questions_page():
    if request.method == "GET":
        return render_template("manage_questions.html",title="Faculty Dashboard | Manage Questions",page_hero_title="Manage Questions")
       
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
        question.add_to_db()

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

@app.route('/faculty-dashboard/manage-questions/edit',methods=["GET","POST"])
def edit_questions_page():
    if request.method == "GET":
        return render_template("edit_question.html",title="Manage Questions | Edit",page_hero_title="Edit Questions",questions=[])
    
    elif request.method == "POST":
        
        form_data = request.form
        qretriever = QuestionRetriever()
        sretriever = SubjectRetriever()
        
        sretriever.subject_name = form_data.get('subject')
        
        semester = form_data.get('semester')
        subject = sretriever.get_code_by_name()
        
        questions = qretriever.get_by_subject_and_semester(subject=subject,semester=semester)

        del qretriever, sretriever
        return render_template("edit_question.html",title="Manage Questions | Edit",page_hero_title="Edit Questions",questions=questions)

@app.route('/faculty-dashboard/manage-questions/edit/<question_id>',methods=['GET','POST'])
def question_editor_page(question_id):
    
    if request.method == "GET":
        question_retiever = QuestionRetriever()        
        details = question_retiever.get_by_id(question_id)
        print(details)
        return render_template("question_editor.html",title="Edit Questions | Question Editor",page_hero_title="Question Editor",details=details)
    
    elif request.method == "POST":
        form_data = request.form
        new_question = form_data.get('question')
        question = Question()
        question.edit_question(question_id=question_id,new_question=new_question)
        
        return render_template("question_editor.html",title="Edit Questions | Question Editor",page_hero_title="Question Editor",details="")
        
@app.route('/faculty-dashboard/manage-students',methods=['GET','POST'])
def manage_students_page():
    if request.method == "GET":
        return render_template("manage_students.html",title="Faculty Dashboard | Manage Students",page_hero_title="Manage Students")

@app.route('/faculty-dashboard/manage-students/add',methods=['GET','POST'])
def add_batch_page():
    if request.method == "GET":
        return render_template("add_batch.html",title="Manage Students | Add",page_hero_title="Add Batch")
    
    elif request.method == "POST":
        batch_file = request.files.get('batch_file')
        if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],"csv")) == False:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],"csv"))
            
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],"csv",secure_filename(batch_file.filename))
        batch_file.save(file_path)
    
        with open(file_path) as f:
            reader = csv.DictReader(f)
            for record in reader:
                student = Student()
                
                student.uucms_no = record.get('uucms_no')
                student.name = record.get('name')
                student.course = record.get('course')
                student.semester = record.get('semester')
                student.batch = record.get('batch')
                password = student.generate_student_password()
                
                student.add_student_to_db(password)
                print(f"added {student.uucms_no}")
            f.close()
        os.remove(file_path)
        return render_template("add_batch.html",title="Manage Students | Add",page_hero_title="Add Batch")

@app.route('/faculty-dashboard/manage-students/view',methods=['GET','POST'])
def view_batch_page():
    if request.method == "GET":
        retriever = StudentRetriever()
        batches = retriever.get_batch_details()
        return render_template("view-batch.html",title="Manage Students | View",page_hero_title="View Batch",batches=batches)
       
@app.route('/faculty-dashboard/manage-students/view/<course>-<batch>',methods=['GET','POST'])
def view_students_page(course,batch):
    if request.method == "GET":
        retriever = StudentRetriever()
        # print(type(batch),batch,type(course),course)
        student_list = retriever.get_by_batch(batch=int(batch),course=course.strip())
        # print(student_list)
        
        return render_template("view-students.html",title="View | Students",page_hero_title="View Students",student_list=student_list)

@app.route('/faculty-dashboard/reporting-and-analysis',methods=["GET","POST"])
def report_and_analysis_page():
    if request.method == "GET":
        retriever = StudentRetriever()
        batches = retriever.get_batch_details()
        return render_template("report_and_analysis_page.html",title="Report And Analysis | View Students",page_hero_title="Report and Analysis",batches=batches)


@app.route('/faculty-dashboard/reporting-and-analysis/view/<course>-<batch>',methods=['GET','POST'])
def student_report_list_page(course,batch):
    if request.method == "GET":
        retriever = StudentRetriever()
        # print(type(batch),batch,type(course),course)
        student_list = retriever.get_by_batch(batch=int(batch),course=course.strip())
        # print(student_list)
        
        return render_template("student-report-list.html",title="View | Students",page_hero_title="View Students",student_list=student_list)
    
@app.route('/faculty-dashboard/reporting-and-analysis/view/<course>-<batch>/<uucms_no>-report')
def show_report(uucms_no,course,batch):
    if request.method == "GET":
        generator = ReportGenerator()
        generator.uucms_no = uucms_no
        report=generator._generate_report_text()

        report_html = render_template("report.html",title=f"Report and Analysis | Report",page_hero_title="Report",report=report)
        return report_html
    
    
@app.route("/faculty-dashboard/view-submissions",methods=["GET","POST"])
@app.route("/student-dashboard/view-submissions",methods=["GET","POST"])
def view_submissions_page():
    if request.method == "GET":
        if "student" in session['type']:
            retriever = SubmissionRetriever()
            records = retriever.get_by_student(session['uucms_no'])
            print(records)
            return render_template("submissions_page.html",title="Student Dashboard | View Submission",page_hero_title="View Submissions",submission_list=records)
        
        elif "faculty" in session['type']:
            retriever = SubmissionRetriever()
            records = retriever.get_by_semester(6)
            return render_template("submissions_page.html",title="Faculty Dashboard | View Submission",page_hero_title="View Submissions",submission_list=records)
            
    # else:
    #     return render_template("submissions_page.html",title="Student Dashboard | View Submission",page_hero_title="View Submissions",submission_list=[])

# Admin Dashboard Routes
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
        
        course.add_to_table()
        
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
        
        subject.add_to_db()
        del form_data
        course = Course()
        course_list = course.list_courses()
        del course
        return render_template("add_subject.html",title="Admin Dashboard | Add Subject",page_hero_title="Add Subject",courses=course_list)


@app.route('/admin-dashboard/add-faculty',methods=["GET","POST"])
def add_faculty_page():
    if request.method == "GET":
        return render_template("registration_page.html",title="Admin Dashboard | Add Faculty",page_hero_title="Add Faculty")
    
    elif request.method == "POST":
        form_data = request.form
        faculty = Faculty()
        faculty.department = "BCA"
        faculty.faculty_id = form_data.get('faculty_id')
        faculty.name = form_data.get('faculty_name')
        faculty.email = form_data.get('faculty_email')
        
        password = form_data.get('password')
        confirm_password =  form_data.get('confirm_password')
        
        
        if password == confirm_password:
            hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
            faculty.password = hashed_password
            
        faculty.add_to_db()
        return redirect('/admin-dashboard')

# Student Dashboard Routes
@app.route('/student-dashboard',methods=["GET","POST"])
def student_dashboard_page():
    if request.method == "GET":
        return render_template("student-dashboard.html",title="ByteLab | Student Dashboard",page_hero_title="Student Dashboard")
 
@app.route('/student-dashboard/solve-questions',methods=["GET","POST"])
def solve_questions_page():
    
    if request.method == "GET":
        if 'student' in session['type']:
            retriever = QuestionRetriever()
            question_list = retriever.get_by_semester(semester=1)
            print(session['semester'])
            print(question_list)
            
            return render_template("solve-questions.html",title="Student Dashboard | Solve Questions",page_hero_title="Solve Questions",question_list=question_list)  

@app.route('/student-dashboard/solve-questions/editor/<question_id>',methods=["GET","POST"])
def editor_page(question_id):
    
    if request.method == "GET":
        retriever = QuestionRetriever()
        question_details = retriever.get_by_id(question_id=question_id)
        return render_template("editor.html",title="Question | Editor",question=question_details['question'],language=question_details['programming_language'].strip(),question_id=question_id,page_hero_title="Editor")
    
    elif request.method == "POST":
        return redirect("/student-dashboard/solve-questions")

@app.route("/account",methods=["GET","POST"])
def my_account_page():
    if request.method == "GET":
        if "student" in session['type']:
            record = (session['uucms_no'],session['student_name'],session['course'],session['semester'],session['batch'],session['type'].title())
            details = list(zip(("UUCMS No","Name","Course","Semester","Batch","Type"),record)) 
            del record
            return render_template("account_page.html",title="ByteLab | My Account",page_hero_title="My Account",details=details)
        
        elif "faculty" in session['type']:
            record = (session['faculty_id'],session['faculty_name'],session['department'],session['email'],session['type'].title())
            details = list(zip(("Faculty ID","Name","Department","Email","Type"),record)) 
            del record
            return render_template("account_page.html",title="ByteLab | My Account",page_hero_title="My Account",details=details)
        
        elif "admin" in session['type']:
            print()
            return render_template("account_page.html",title="ByteLab | My Account",page_hero_title="My Account",details=list(zip(['Account Type'],['Admin'])))
            
        
@app.route("/logout",methods=["GET","POST"])
def logout():
    if request.method == "GET":
        session.clear()
        return redirect("/login")
         
                  
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    
    