from flask import Flask,render_template, request, flash, redirect, url_for, send_from_directory, session
from flask import Blueprint
import pymysql 
# from io import BytesIO
# from PIL import Image
# import base64
# import flask 
import requests
import os 
import uuid as uuid 
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json 




connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Karnal@123',
                             database='users',
)


app= Flask(__name__)
app.config['SECRET_KEY'] = 'cop290'
UPLOAD_FOLDER = 'D:/IIT-D/sem 4/almost_final_2/finally_kaam 2/static/' # where u run pls check the path 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





@app.route('/', methods=['GET'])
def login():
    with connection.cursor() as cur:
        if request.method == 'GET':
            email = request.args.get('email')
            password = request.args.get('password')
            session['email']=email
            try:
                cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(type(user))
                # print(2)
                if user:

                    # password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    # cur.execute("SELECT * FROM users3 WHERE password=%s",(password,))
                    # result=cur.fetchone()
                    # cur.execute("GET users3 ")
                    print(user[3])
                    print(password)
                    print(check_password_hash(user[3],password))
                    if check_password_hash(user[3],password):
                        cur.execute("SELECT * FROM post1 WHERE user_id=%s ORDER BY created_at DESC LIMIT 10", (user[0],))
                        post = cur.fetchall()


                    
                        
                        
                        
                        return render_template('profile.html',user=user,post=post)
                        
                    # home.html
                    else:
                        print(5)
                        flash("incorrect password")
                        return redirect(url_for('login'))
                else:
                    print(4)
                    # flash('email id does not exist')
                    return render_template('login.html')
                    

            except Exception as e:
                # flash(f"Error creating user: {e}")
                return render_template('login.html')
            

    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    with connection.cursor() as cur: 
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password-verify')
            image=request.files['myfile']
            tag = request.form.get('tag')             
            if tag!="Professional" or tag!="Home Cook" or tag!="Foodie":
                flash("Enter Appropriate Tag as mentioned in the form Professional/Home Cook/Foodie")
                return render_template('signup.html')
            print(username)
            print(type(image))
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(image.filename)))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file to {image_path}")
            name= request.form.get('fullname')
            bio=request.form.get('text')
            print(1)
            try:
                print(1)
                cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(1)
                if user:
                    print(type(user))
                    flash("Email already exists")
                    return redirect(url_for('signup'))
                else:

                    print(password)
                    print(password2)
                    
                    if password==password2:
                        #image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(image.filename)))
                        password = generate_password_hash(password , method = 'sha256')
                        sql = f"INSERT INTO `users3` (username,email,password,image,bio,tag) VALUES (%s,%s,%s,%s,%s,%s)"
                        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

                        print(type(username))
                        print(password)
                        print(type(name))
                        print(type(bio))
                        cur.execute(sql,(username,email,password,filename,bio,tag))
                        print("2")
                        userid = cur.lastrowid
                        print("2")
                        connection.commit()
                        return redirect('/')
                    else:
                        flash("Passwords did not match")
                        return render_template('signup.html')
                    # return redirect('/')
            except Exception as e:
                # flash(f"Error creating user: {e}")
                return render_template('signup.html')
            
    return render_template('signup.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    with connection.cursor() as cur:
        print(1)
        if request.method == 'POST':
            print(2)
            email = request.form.get('email')
            session['email']=email
            print(3)
            try:
                cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
                user=cur.fetchone()

                if user:
                    print("me")
                    return redirect(url_for('forgotpasswordverify'))
                else:
                    
                    flash("Email invalid")
                    return render_template('forgotpassword.html')
            except Exception as e:
                return render_template('signup.html')
    return render_template('forgotpassword.html')

 
@app.route('/forgotpasswordverify', methods = ['GET','POST'])
def forgotpasswordverify():
    print(2)
    email=session.get('email')
    print(email)
    with connection.cursor() as cur:
        print("me")
        if request.method == 'POST':
            print("me")
            password = request.form.get('password')
            password2 = request.form.get('password-verify')
            if password==password2:
                password = generate_password_hash(password , method = 'sha256')
                sql = f"UPDATE users3 SET password=%s WHERE email = %s"
                cur.execute(sql,(password,email))
                print("2")
                connection.commit()
                return redirect('/')
            else:
                flash ("Passwords do not match")
                return render_template('forgotpasswordverify.html')
        return render_template('forgotpasswordverify.html')



@app.route('/profile', methods=['GET','POST'])
def profile():
    with connection.cursor() as cur:

        email=session.get('email')
        with connection.cursor() as cur:
            if request.method == 'GET':
                cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
                user=cur.fetchone()

        # assuming hmare paas email id hain
                # sort_query = "SELECT * FROM post1 ORDER BY user_id ASC, created_at DESC"
                # id = cur.execute("SELECT user_id FROM users3 WHERE email=%s",(email,))
                # query = "SELECT * FROM post1 WHERE user_id=%s LIMIT 6"
                # cur.execute(sort_query)
                # cur.execute(query,(id,))
                # post = cur.fetchone()
                cur.execute("SELECT * FROM post1 WHERE user_id=%s ORDER BY created_at DESC LIMIT 10", (user[0],))
                post = cur.fetchall()
        
        # print(email)
    return render_template('profile.html',user=user,post=post)
@app.route('/edit_profile' , methods = ['GET','POST'])
def edit_profile():
        email=session.get('email')
        
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
            user=cur.fetchone()
            print(4)
            if request.method == 'POST':
                name = request.form.get('fname')
                username = request.form.get('username')
                bio = request.form.get('bio')
                password1 = request.form.get('password')
                password2 = request.form.get('password-verify')
                print(username)
                print(bio)
                print(1)
                if password1==password2:
                    print(2)
                    sql = f"UPDATE users3 SET username=%s,bio=%s,password=%s WHERE email = %s"
                    cur.execute(sql,(username,bio,password1,email))
                    connection.commit()
                    print(3)
                    cur.execute("SELECT * FROM users3 WHERE email=%s",(email,))
                    user=cur.fetchone()
                    cur.execute("SELECT * FROM post1 WHERE user_id=%s ORDER BY created_at DESC LIMIT 10", (user[0],))
                    post = cur.fetchall()

                    return render_template('profile.html', user=user,post=post)
                else:
                    flash ("Passwords do not match")
                    return render_template('edit_profile.html')
            return render_template('edit_profile.html')
        return render_template('edit_profile.html')

@app.route('/profile.js')
def serve_js():
    return send_from_directory(app.static_folder, 'profile.js')

@app.route('/login.js')
def serve_js_login():
    return send_from_directory(app.static_folder, 'login.js')

@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory(app.static_folder['UPLOAD FOLDER'], filename)

@app.route('/AddPost', methods=['GET', 'POST'])
def AddPost():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS post1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR (1000),
            content TEXT,
            user_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FULLTEXT (title)
        )
    """
    insert_post_query = "INSERT INTO post1 (title, content,user_id) VALUES (%s,%s,%s)"

    with connection.cursor() as cur:
        if request.method == 'POST':
            email = session.get('email')
            post_title = request.form.get('comments')
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(2)
            print((os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            cur.execute(create_table_query)
            cur.execute("SELECT * FROM users3 WHERE email=%s", (email,))
            user = cur.fetchone()

            # Call Eden AI object detection API to check if the image contains food
            headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDk5YjI1MTAtMTU5OC00NzU5LWFhYWItMzQ0NjdjNmI3YTdhIiwidHlwZSI6ImFwaV90b2tlbiJ9.QAbNhqI7De_JkOzpivc99dqiqS4EQqozR7KtohMB5O8"}
            url = "https://api.edenai.run/v2/image/object_detection"
            # json_payload = {"providers": "google, amazon", "file_url":(os.path.join(app.config['UPLOAD_FOLDER'], filename))}
            data = {"providers":"google,amazon"}
            files={'file':open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')}
            response = requests.post(url, data=data,files=files, headers=headers)
            result = json.loads(response.text)
            

            # Check if any item in the response contains the "Food" label
            contains_food = False
            print(result["amazon"]["items"])
            for item in result["amazon"]["items"]:
                if item["label"] == "Food":
                    print("food")
                    contains_food = True
                    break
            for item in result["google"]["items"]:
                if item["label"] == "Food":
                    print("food")
                    contains_food = True
                    break

            # Insert the post into the database only if it contains food
            if contains_food:
                cur.execute(insert_post_query, (post_title, filename, user[0]))
                connection.commit()
                cur.execute("SELECT * FROM post1 WHERE user_id=%s ORDER BY created_at DESC LIMIT 10", (user[0],))
                post = cur.fetchall()
                return render_template('profile.html', user=user,post=post)
            else:
                flash ("Please upload a food image!")
                return render_template('AddPost.html')
    return render_template('AddPost.html')


@app.route('/index', methods = ['GET' , 'POST'])
def Home():
    with connection.cursor() as cur:
        if request.method == 'POST' :
            search_query= request.form['query']
            cur.execute("SELECT * FROM post1 WHERE title LIKE %s OR content LIKE %s", ('%'+search_query+'%', '%'+search_query+'%'))
            search_results = cur.fetchall()
            print(search_results)
            return render_template('search.html',posts=search_results)
        else:
            cur.execute("SELECT * from post1")
            posts=cur.fetchall()
            
            return render_template('index.html',posts=posts)

    # SELECT * from post1 WHERE MATCH(title) AGAINST ();
    # return render_template('index.html')
@app.route('/professional', methods = ['GET' , 'POST'])
def professional():
    with connection.cursor() as cur:
        email = session.get('email')
        posts = []
        cur.execute("SELECT * FROM users3 WHERE tag='Professional'")
        t= cur.fetchall()
        print(t)
        l=len(t)
        for i in range(l):
            cur.execute("SELECT * FROM post1 WHERE user_id=%s",(t[i][0],))
            user=cur.fetchall()
            k=len(user)
            for i in range(k):
               posts = posts+[user[i]]
            

        # print(posts)    

    return render_template('professional.html',posts=posts)
@app.route('/homecook', methods = ['GET' , 'POST'])
def homecook():
    with connection.cursor() as cur:
        posts = []
        cur.execute("SELECT * FROM users3 WHERE tag='Home Cook'")
        t= cur.fetchall()
        print(t)
        l=len(t)
        for i in range(l):
            cur.execute("SELECT * FROM post1 WHERE user_id=%s",(t[i][0],))
            user=cur.fetchall()
            k=len(user)
            for i in range(k):
               posts = posts+[user[i]]
    return render_template('homecook.html',posts=posts)
@app.route('/foodie', methods = ['GET' , 'POST'])
def foodie():
    with connection.cursor() as cur:
        email = session.get('email')
        posts = []
        cur.execute("SELECT * FROM users3 WHERE tag='Foodie'")
        t= cur.fetchall()
        print(t)
        l=len(t)
        for i in range(l):
            cur.execute("SELECT * FROM post1 WHERE user_id=%s",(t[i][0],))
            user=cur.fetchall()
            k=len(user)
            for i in range(k):
               posts = posts+[user[i]]
    return render_template('foodie.html',posts=posts)




if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True)
