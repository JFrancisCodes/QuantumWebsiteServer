from flask import Flask, render_template, url_for, send_from_directory, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess
import time
import os
import sys


app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


app.config['APPLICATION_ROOT'] = '/qanim'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    template_list = app.jinja_loader.list_templates()
    print(template_list, file=sys.stderr)
    return render_template('index.html')



@app.route('/animations')
def animations():
    print(url_for('animations'), file=sys.stderr) 
    return render_template('animations.html')

@app.route('/single_gaussian')
def single_gaussian():
    return render_template('single_gaussian.html')

@app.route('/heatwavesch')
def heatwavesch():
    return render_template('heatwavesch.html')


@app.route('/double_gaussian')
def double_gaussian():
    return render_template('double_gaussian.html')

@app.route('/gaussapp')
def gaussapp():
    return render_template('gaussapp.html')

@app.route('/play_single_gaussian', methods=['POST'])
def play_single_gaussian():
    sigma = request.form.get('sigma')
    momentum = request.form.get('momentum')

    sigma_str = "{:.2f}".format(float(sigma))
    momentum_str = "{:.2f}".format(float(momentum))


    # Create the filename based on the received sigma and momentum values
    filename = f"single_gaussian_sigma_{sigma_str}_momentum_{momentum_str}.mp4"

    # Define the path to the directory where the video files are stored
    directory_path1 = 'SingleGaussian'
    directory_path2 = 'SingleGaussianAsymp'

    file_path1 = os.path.join(directory_path1, filename)
    file_path2 = os.path.join(directory_path2, filename)

    # Serve the video file using Flask's send_from_directory
    return render_template('single_gaussian.html', mp4_filename1=file_path1, mp4_filename2=file_path2)


@app.route('/play_double_gaussian', methods=['POST'])
def play_double_gaussian():
    sigma_1 = float(request.form.get('sigma1'))
    momentum_1 = float(request.form.get('momentum1'))
    sigma_2 = float(request.form.get('sigma2'))
    momentum_2 = float(request.form.get('momentum2'))
    w = float(request.form.get('weight'))
    sigma1_str = f"{sigma_1:.2f}"
    sigma2_str = f"{sigma_2:.2f}"
    momentum1_str = f"{momentum_1:.2f}"
    momentum2_str = f"{momentum_2:.2f}"
    weight_str = f"{w:.2f}"
    pos1_str = f"{-10:.2f}"
    pos2_str = f"{10:.2f}"

    filename = f"dg_s1_{sigma1_str}_m1_{momentum1_str}_p1_{pos1_str}_s2_{sigma2_str}_m2_{momentum2_str}_p2_{pos2_str}_w_{weight_str}.mp4"

    directory_path1 = 'DoubleGaussian'
    directory_path2 = 'DoubleGaussianAsymp'

    file_path1 = os.path.join(directory_path1, filename)
    file_path2 = os.path.join(directory_path2, filename)

    return render_template('double_gaussian.html', mp4_filename1=file_path1, mp4_filename2=file_path2)


@app.route('/play_hws', methods=['POST'])
def play_hws():
    n = request.form.get('n')
    m = request.form.get('m')

    n_str = "{}".format(int(float(n)))
    m_str = "{}".format(int(float(m)))


    # Create the filename based on the received sigma and momentum values
    filename1 = f"heat_n_{n_str}_m_{m_str}.mp4"
    filename2 = f"wave_n_{n_str}_m_{m_str}.mp4"
    filename3 = f"schrodinger_n_{n_str}_m_{m_str}.mp4"


    # Define the path to the directory where the video files are stored
    directory_path1 = 'Heat'
    directory_path2 = 'Wave'
    directory_path3 = 'Schrodinger'



    file_path1 = os.path.join(directory_path1, filename1)
    file_path2 = os.path.join(directory_path2, filename2)
    file_path3 = os.path.join(directory_path3, filename3)

    # Serve the video file using Flask's send_from_directory
    return render_template('heatwavesch.html', mp4_filename1=file_path1, mp4_filename2=file_path2, mp4_filename3=file_path3)

@app.route('/static/movies/<path:filename>')
def serve_video(filename):
    return send_from_directory('static/movies', filename)
                     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


