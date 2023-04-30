from flask import Flask,render_template, request, flash, redirect, url_for, send_from_directory, session
from flask import Blueprint
import pymysql 
# from io import BytesIO
# from PIL import Image
# import base64
# import flask 
import os 
import uuid as uuid 
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Karnal@123',
                             database='users',
)


app= Flask(__name__)
app.config['SECRET_KEY'] = 'cop290'
UPLOAD_FOLDER = 'D:/IIT-D/sem 4/almost final/finally_kaam/finally_kaam/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# def save_photos(photos):
#     filenames = []
#     for photo in photos:
#         if photo:
#             filename = secure_filename(photo.filename)
#             photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             filenames.append(filename)
#     return filenames


@app.route('/', methods=['GET'])
def login():
    with connection.cursor() as cur:
        if request.method == 'GET':
            email = request.args.get('email')
            password = request.args.get('password')
            session['email']=email
            try:
                cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(type(user))
                # print(2)
                if user:

                    # password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    # cur.execute("SELECT * FROM users2 WHERE password=%s",(password,))
                    # result=cur.fetchone()
                    # cur.execute("GET users2 ")
                    print(user[3])
                    print(password)
                    print(check_password_hash(user[3],password))
                    if check_password_hash(user[3],password):

                    
                        
                        
                        print(user[1])
                        print(user[5])
                        return render_template('profile.html',user=user)
                        
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
            print(4)
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password-verify')
            image=request.files['myfile']

            
            print(username)
            print(type(image))
            filename = secure_filename(image.filename)
            # print(image.filename)
            # image=bytes(image_str,'utf-8')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(image.filename)))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file to {image_path}")
            name= request.form.get('fullname')
            bio=request.form.get('text')
            print(1)
            try:
                print(1)
                cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(1)
                if user:
                    print(type(user))
                    flash("Email already exists")
                    return redirect(url_for('signup'))
                else:
                    print(type(user))
                    print(password)
                    print(password2)
                    
                    if password==password2:
                        #image.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(image.filename)))
                        password = generate_password_hash(password , method = 'sha256')
                        sql = f"INSERT INTO `users2` (username,email,password,image,bio) VALUES (%s,%s,%s,%s,%s)"
                        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

                        print(type(username))
                        print(password)
                        print(type(name))
                        print(type(bio))
                        cur.execute(sql,(username,email,password,filename,bio))
                        print("2")
                        userid = cur.lastrowid
                        print("2")
                        connection.commit()
                    else:
                        return render_template('signup.html')
                    return render_template('login.html')
            except Exception as e:
                # flash(f"Error creating user: {e}")
                return render_template('signup.html')
    return render_template('signup.html')

@app.route('/forgotpassword', methods=['GET'])
def forgotpassword():
    with connection.cursor() as cur:
        print(1)
        if request.method == 'GET':
            email = request.args.get('email')
            try:
                print(2)
                cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(3)
                print(type(user))
                # print(user[0])
                # print(2)
                if user:
                    print(4)
                    return render_template('forgotpasswordverify.html')
                else:
                    print(5)
                    flash("Email invalid")
                    return render_template('forgotpassword.html')
            except Exception as e:
                return render_template('signup.html')
    return render_template('forgotpassword.html')

 
@app.route('/forgotpasswordverify', methods = ['GET','UPDATE'])
def forgotpasswordverify():
    with connection.cursor() as cur:
        if request.method == 'GET':
            password = request.args.get('password')
            password2 = request.args.get('password-verify')

            if password==password2:
                sql = f"UPDATE INTO `users2` (password) VALUES (%s,%s,%s,%s,%s)"
                cur.execute(sql,(password))
                print("2")
                connection.commit()
                return render_template('login.html')
            else:
                flash ("Passwords dpo not match")
                return render_template('forgotpasswordverify.html')
        return render_template('forgotpasswordverify.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    email=session.get('email')
    with connection.cursor() as cur:
        if request.method == 'GET':
                cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
                user=cur.fetchone()

    return render_template('profile.html',user=user)

@app.route('/edit_profile' , methods = ['GET','POST'])
def edit_profile():
        email=session.get('email')
        
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
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
                    sql = f"UPDATE users2 SET username=%s,bio=%s,password=%s WHERE email = %s"
                    cur.execute(sql,(username,bio,password1,email))
                    connection.commit()
                    print(3)
                    cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
                    user=cur.fetchone()

                    return render_template('profile.html', user=user)
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

@app.route('/AddPost', methods = ['GET' , 'POST'])
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
    print("me")


    with connection.cursor() as cur:
        if request.method == 'POST' :
            print("slef")
            email=session.get('email')
            post_title = request.form.get('comments')
            image = request.files.get('image')
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            cur.execute(create_table_query)
            cur.execute("SELECT * FROM users2 WHERE email=%s",(email,))
            user=cur.fetchone()
            cur.execute(insert_post_query, (post_title, filename,user[0]))
            connection.commit()
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return render_template('profile.html',user=user,posttext=post_title,postimage=image)
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
    return render_template('professional.html')
@app.route('/homecook', methods = ['GET' , 'POST'])
def homecook():
    return render_template('homecook.html')
@app.route('/foodie', methods = ['GET' , 'POST'])
def foodie():
    return render_template('foodie.html')

if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True)
