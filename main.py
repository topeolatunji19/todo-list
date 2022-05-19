from flask import Flask, render_template, request, jsonify, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap

Base = declarative_base()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-random-key'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# bootstrap = Bootstrap(app)


class Tasks(Base):

    __tablename__ = "To-Do List"
    id = Column(Integer, primary_key=True)
    task = Column(String(500), unique=True, nullable=False)


engine = create_engine("sqlite:///todolist.db")

# Base.metadata.create_all(engine)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_task = request.form["ItemToDo"]
        with Session(engine) as session:
            task_to_add = Tasks(
                task=new_task
            )
            session.add(task_to_add)
            session.commit()
        print(new_task)
        return redirect(url_for('home'))
    with Session(engine) as session:
        all_tasks = session.query(Tasks).all()
    return render_template("index.html", all_tasks=all_tasks)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with Session(engine) as session:
        task_to_delete = session.query(Tasks).get(task_id)
        session.delete(task_to_delete)
        session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)