import base64
from flask import *
from flask import render_template
from flask import request
import os.path
import cv2
import face_recognition as fr
import os
import mediapipe as mp
from datetime import datetime
from flask_socketio import SocketIO, send, emit
import numpy as np
import psycopg2
from time import sleep


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__)

socketio = SocketIO(app)
name = None
login_date_time = None

DATABASE_URL = os.environ.get('postgres://jmpzfhmuopteea:803abea6d8b0f13812302d21d388e0d62bb645ff7bd96d787d340b47a759ff46@ec2-54-82-205-3.compute-1.amazonaws.com:5432/d995muhn3hifl1')

cmd_create_action_table = """CREATE TABLE details(id SERIAL primary key,name VARCHAR(25),username varchar(25),height VARCHAR(25),weight VARCHAR(25),password VARCHAR(25))"""

con = None
try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = con.cursor()
    cur.execute(cmd_create_action_table)

    # close the communication with the HerokuPostgres
    cur.close()
except Exception as error:
    print('Could not connect to the Database.')
    print('Cause: {}'.format(error))

finally:
    # close the communication with the database server by calling the close()
    if con is not None:
        con.close()
        print('Database connection closed.')



# # Connect to your PostgresSQL database on a remote server
# def connections():
#     conn = psycopg2.connect(host="127.0.0.1", port="5432", dbname="user_details", user="postgres", password="p@ssw0rd")
#
#     # Open a cursor to perform database operations
#     cur = conn.cursor()
#     return cur, conn


@app.route('/check', methods=['POST', 'GET'])
def check():
    global login_date_time, name
    username = request.form.get('username')
    password = request.form.get('password')
    # cur, conn = connections()

    with con:
        cur.execute(f"SELECT * FROM details WHERE username=%(username)s AND password=%(password)s",
                    {'username': username, 'password': password})

        if not cur.fetchall():
            return render_template("home.html")
        else:
            name = request.form.get("username")
            dt = datetime.now()
            login_date_time = dt
            print(login_date_time)
            print(name)
            cur.execute('INSERT INTO  user_logindetails(username,login) VALUES(%s,%s) ', (name, dt,))
            con.commit()
            # conn.close()
            return render_template("success.html")


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        height = request.form.get('height')
        weight = request.form.get('weight')
        password = request.form.get('password')
        # cur, conn = connections()
        check_in_db = "SELECT * from details where username like %s"
        cur.execute(check_in_db, [username])
        result = cur.fetchall()
        print(result)
        if len(result) >= 1:
            msg = "user name already exists, Register with other username"
            return render_template('register.html', msg=msg)
        else:
            cur.execute('INSERT INTO details(name,username,height,weight,password) VALUES (%s,%s,%s,%s,%s)',
                        (name, username, height, weight, password))
            con.commit()
            # conn.close()
            msg = 'Registered successfully'
            return render_template('login.html', msg=msg)


@socketio.on('message')
def hello(data):
    print(data)
    return render_template("light_workout.html")


@socketio.on("face")
def face(data):
    global login_date_time, name

    path = "static/users_images/"

    known_names = []
    known_name_encodings = []
    # cur, conn = connections()
    images = os.listdir(path)
    for _ in images:
        image = fr.load_image_file(path + _)
        # print(image)
        image_path = path + _
        # print(image_path)
        encoding = fr.face_encodings(image)[0]

        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(os.path.basename(image_path))[0].lower())
        cap = cv2.VideoCapture(0)
        if cap.isOpened:
            while True:
                ret, frame = cap.read()
                image_data = cv2.resize(frame, (250, 250))
                image_data = cv2.imencode('image_data.jpg', image_data)[1].tobytes()
                base_64_encoded = base64.b64encode(image_data).decode('utf-8')
                image_data = "data:image/jpeg;base64,{}".format(base_64_encoded)
                send({'image_data': image_data})
                face_locations = fr.face_locations(frame)
                face_encodings = fr.face_encodings(frame, face_locations)
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = fr.compare_faces(known_name_encodings, face_encoding)
                    user = ""

                    face_distances = fr.face_distance(known_name_encodings, face_encoding)
                    best_match = np.argmin(face_distances)

                    if matches[best_match]:
                        user = known_names[best_match]

                    if user in known_names:
                        name = user
                        print(name)
                        cap.release()
                        dt = datetime.now()
                        login_date_time = dt
                        print(login_date_time)
                        cur.execute('INSERT INTO  user_logindetails(username,login) VALUES(%s,%s) ', (name, dt,))
                        con.commit()
                        emit('success', {'url': url_for('success')})

                    else:
                        cap.release()
                        emit('redirect', {'msg': "Couldn't recognise please login with password"})


@app.route('/success')
def success():
    return render_template("success.html")


@socketio.on('capture')
def save_img(img_base64):
    header, data = img_base64.split(',', 1)
    image_data = base64.b64decode(data)
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    # print(session['username'])
    # name = session['username']
    print(name)
    img_name = "{}.jpg".format(name)
    save_path = 'static/users_images'
    completeName = os.path.join(save_path, img_name)
    cv2.imwrite(completeName, image)
    status = "Hey {}..! Captured your pic. ".format(name)
    sleep(1.5)
    emit('redirect', {'url': url_for('success')})


@app.route('/capture')
def capture():
    return render_template('face.html')


@app.route('/food_intake', methods=['POST', 'GET'])
def food_intake():
    return render_template("exercise.html")


@app.route('/light_workout')
def light_workout():
    return render_template("light_workout.html")


@app.route('/light_biceps')
def biceps():
    return render_template("light_biceps.html")


@app.route("/light_timer")
def light():
    msg = "Get ready for squats..!"
    return render_template("timer.html", timer=5, counter="/light_squats", msg=msg)


@app.route('/light_squats')
def squats():
    return render_template("light_squats.html")


@app.route('/medium_workout')
def medium_workout():
    return render_template("medium_workout.html")


@app.route('/medium_lunges')
def lunges():
    return render_template("medium_lunges.html")


@app.route("/medium_timer")
def medium():
    msg = "Get ready for pushups..!"
    return render_template("timer.html", msg=msg, timer=5, counter="/medium_pushup")


@app.route('/medium_pushup')
def pushup():
    return render_template("medium_pushup.html")


@app.route('/heavy_workout')
def heavy_workout():
    return render_template("heavy_workout.html")


@app.route('/heavy_pushup')
def heavy_pushup():
    return render_template('heavy_pushup.html')


@app.route('/short_head_biceps')
def short_head_biceps():
    return render_template("short_head_biceps.html")


@app.route("/heavy_timer")
def heavy():
    msg = "Get ready for pushups..!"
    return render_template("timer.html", msg=msg, timer=5, counter="/medium_pushup")


@app.route("/thanks")
def thanks():
    print("thanks")
    return render_template("thanks.html")


@app.route('/logout')
def logout():
    dt = datetime.now()
    # cur, conn = connections()
    # cur.execute('INSERT INTO  user_logindetails(username,logout) VALUES(%s,%s) ', (name, dt))
    con.commit()
    con.close()
    return render_template("home.html")


if __name__ == '__main__':
    socketio.run(app)
