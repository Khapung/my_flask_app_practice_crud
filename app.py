from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone



# My App
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"  # creating a database called project.db
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False # This will speed up our app
db = SQLAlchemy(app) 


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()

# Routes to webpages
# Home page
@app.route("/", methods=["POST", "GET"])
def index():
    # Add a Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"  
    # See all current tasks
    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)  
    


# Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"


# Edit an item
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template("edit.html", task=task)    
    
# Runner and debugger
if __name__ == "__main__":
    # with app.app_context(): # This line creates an application context using the Flask app object. An application context is necessary for certain operations, like interacting with the database, as it binds the application to the current context
    #     db.create_all() # Inside the application context, this command creates all the database tables defined in your models. It's a way to set up your database schema.
    app.run(debug=True) # This line runs the Flask web application in debug mode. When debug=True, Flask provides helpful error messages and automatically reloads the server when code changes are detected.







