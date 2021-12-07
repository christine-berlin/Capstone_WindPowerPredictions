from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle
from predict_api import make_prediction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        task_content = request.form['content']
        zone = request.form['zone']
        print('ZONE: ', zone)
        X = task_content
        predictions = make_prediction(X, zone=zone)

        #predictions = dict(zip(range(0,24),make_prediction(X)))
        #pred = make_prediction(X, zone)
        #predictions = dict(zip(range(-1,24),pred))
        print('PRED: ', predictions)
        #print('making prediction for {}: {}'.format(task_content, predictions))
        return render_template('index.html', predictions=predictions)
    else:
        return render_template('index.html', predictions=[])


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)