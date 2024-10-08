from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cv.db'
db = SQLAlchemy(app)

# Models
class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    bio = db.Column(db.Text)
    

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    year_completed = db.Column(db.Integer)

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    start_date = db.Column(db.String(10))
    end_date = db.Column(db.String(10))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    description = db.Column(db.Text)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/personal_info', methods=['GET', 'POST'])
def personal_info():
    info = PersonalInfo.query.first()
    if request.method == 'POST':
        if info:
            info.name = request.form['name']
            info.email = request.form['email']
            info.bio = request.form['bio']
            db.session.commit()
        else:
            new_info = PersonalInfo(
                name=request.form['name'],
                email=request.form['email'],
                bio=request.form['bio']
            )
            db.session.add(new_info)
            db.session.commit()
        return redirect(url_for('personal_info'))
    return render_template('personal_info.html', info=info)

@app.route('/education', methods=['GET', 'POST'])
def education():
    if request.method == 'POST':
        edu = Education(
            degree=request.form['degree'],
            institution=request.form['institution'],
            year_completed=request.form['year_completed']
        )
        db.session.add(edu)
        db.session.commit()
        return redirect(url_for('education'))
    educations = Education.query.all()
    return render_template('education.html', educations=educations)

@app.route('/delete_education/<int:id>', methods=['POST'])
def delete_education(id):
    education_entry = Education.query.get(id)
    db.session.delete(education_entry)
    db.session.commit()
    return redirect(url_for('education'))

@app.route('/work_experience', methods=['GET', 'POST'])
def work_experience():
    if request.method == 'POST':
        work = WorkExperience(
            job_title=request.form['job_title'],
            company=request.form['company'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date']
        )
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('work_experience'))
    experiences = WorkExperience.query.all()
    return render_template('work_experience.html', experiences=experiences)

@app.route('/delete_work/<int:id>', methods=['POST'])
def delete_work(id):
    work_entry = WorkExperience.query.get(id)
    db.session.delete(work_entry)
    db.session.commit()
    return redirect(url_for('work_experience'))

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'POST':
        skill = Skill(skill_name=request.form['skill_name'])
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for('skills'))
    skills_list = Skill.query.all()
    return render_template('skills.html', skills=skills_list)

@app.route('/delete_skill/<int:id>', methods=['POST'])
def delete_skill(id):
    skill_entry = Skill.query.get(id)
    db.session.delete(skill_entry)
    db.session.commit()
    return redirect(url_for('skills'))

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        project = Project(
            project_name=request.form['project_name'],
            description=request.form['description']
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))
    projects_list = Project.query.all()
    return render_template('projects.html', projects=projects_list)

@app.route('/delete_project/<int:id>', methods=['POST'])
def delete_project(id):
    project_entry = Project.query.get(id)
    db.session.delete(project_entry)
    db.session.commit()
    return redirect(url_for('projects'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here you can implement logic to save or send the message (e.g., email)
        return redirect(url_for('home'))
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

