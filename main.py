from flask import Flask, request, render_template
import pickle

file = open('bodyfatmodel1.pkl', 'rb')
rf = pickle.load(file)
file.close()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        my_dict = request.form

        density = float(my_dict['density'])
        abdomen = float(my_dict['abdomen'])
        chest = float(my_dict['chest'])
        weight = float(my_dict['weight'])
        hip = float(my_dict['hip'])

        input_features = [[density, abdomen, chest, hip, weight]]
        prediction = rf.predict(input_features)[0].round(2)

        string = 'Percentage of Body Fat Estimated is : ' + str(prediction)+'%'

        return render_template('show.html', string=string)

    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5001)