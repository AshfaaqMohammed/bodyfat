from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle
import os
from sqlalchemy import inspect

# Load model
with open('bodyfatmodel1.pkl', 'rb') as file:
    rf = pickle.load(file)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:root123@host.docker.internal/bodyfat"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    density = db.Column(db.Float, nullable=False)
    abdomen = db.Column(db.Float, nullable=False)
    chest = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.Float, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    inspector = inspect(db.engine)
    table_exists = inspector.has_table(PredictionRecord.__tablename__)
    
    if not table_exists:
        db.create_all()
        return "Table created, please reload the page."

    else:
        # Table exists, proceed with normal logic
        if request.method == 'POST':
            my_dict = request.form
            density = float(my_dict['density'])
            abdomen = float(my_dict['abdomen'])
            chest = float(my_dict['chest'])
            hip = float(my_dict['hip'])
            weight = float(my_dict['weight'])

            input_features = [[density, abdomen, chest, hip, weight]]
            prediction = float(rf.predict(input_features)[0].round(2))

            record = PredictionRecord(
                density=density,
                abdomen=abdomen,
                chest=chest,
                hip=hip,
                weight=weight,
                prediction=prediction
            )
            db.session.add(record)
            db.session.commit()

            string = f"Percentage of Body Fat Estimated is : {prediction}%"
            return render_template('show.html', string=string)

        return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=False)
