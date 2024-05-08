from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify

from questions_module import Question, QuestionRetriever
 

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
    

@app.route('/manage-questions',methods=["GET"])
def manage_questions_page():
    if request.method == "GET":
        return render_template("manage_questions.html",title="ByteLab | Manage Questions",page_hero_title="Manage Questions")
    
    
@app.route('/manage-questions/add',methods=["GET","POST"])
def add_questions_page():
    if request.method == "GET":
        return render_template("add_questions.html",title="Manage Questions | Add",page_hero_title="Add Question")
    
    elif request.method == "POST":
        form_data = request.form
        record = {}
        record['question'] = form_data.get('question')
        record['semester'] = int(form_data.get('semester'))
        record['programming_language'] = form_data.get('programming_language')
        
        del form_data
        question = Question(record['question'],record['semester'],record['programming_language'],"")
        question.insert_into_questions_table()

        return render_template("add_questions.html",title="Manage Questions | Add",page_hero_title="Add Question")

@app.route('/manage-questions/view',methods=["GET","POST"])
def view_questions_page():
    if request.method == "GET":
        return render_template("view_questions.html",title="Manage Questions | View",page_hero_title="View Questions",questions=[])
    
    elif request.method == "POST":
        form_data = request.form
        semester = form_data.get('semester')
        subject = form_data.get('subject')
        
        retriever = QuestionRetriever()
        records = retriever.get_by_subject_and_semester(subject=subject,semester=semester)
        
        return render_template("view_questions.html",title="Manage Questions | View",page_hero_title="View Questions",questions=records)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    
    