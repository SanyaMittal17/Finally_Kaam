from flask import Flask,render_template, request, flash, redirect, url_for
from flask import Blueprint
import pymysql 
from io import BytesIO
from PIL import Image
import base64

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Karnal@123',
                             database='users',
)


app= Flask(__name__)
app.config['SECRET_KEY'] = 'cop290'

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.args.get('email')
        password = request.args.get('password')
    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    with connection.cursor() as cur:
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            password = request.args.get('password')
            password2 = request.args.get('password-verify')
            image=request.args.get('myfile')
            # image=bytes(image_str,'utf-8')
            name= request.args.get('fullname')
            bio=request.args.get('text')
            try:
                print("1")
                cur.execute("SELECT * FROM users1 WHERE email=%s",(email,))
                user=cur.fetchone()
                if user:
                    flash("Email already exists")
                    return redirect(url_for('signup'))
                else:
                    if password==password2:
                        sql = f"INSERT INTO `users1` (username,email,password,image,bio) VALUES (%s,%s,%s,%s,%s)"
                        print(type(username))
                        print(type(image))
                        print(type(name))
                        print(type(bio))
                        cur.execute(sql,(username,email,password,image,bio))
                        print("2")
                        userid = cur.lastrowid
                        print("2")
                        connection.commit()
                    return render_template('login.html')
            except Exception as e:
                # flash(f"Error creating user: {e}")
                return render_template('signup.html')
    return render_template('signup.html')

@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form('email')
    return render_template('forgotpassword.html')

@app.route('/forgotpasswordverify', methods = ['UPDATE'])
def forgotpasswordverify():
    return render_template('forgotpasswordverify.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/edit_profile' , methods = ['GET','POST'])
def edit_profile():
    return render_template('edit_profile.html')
@app.route('/AddPost', methods = ['GET' , 'POST'])
def AddPost():
    return render_template('AddPost.html')
if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True)

