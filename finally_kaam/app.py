from flask import Flask,render_template, request, flash, redirect, url_for, send_from_directory
from flask import Blueprint
import pymysql 
# from io import BytesIO
# from PIL import Image
# import base64
# import flask 
import os
# import os
# from flask_session import Session

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Karnal@123',
                             database='users',
)


app= Flask(__name__)
# upload_folder = os.path.join('static','uploads')
app.config['SECRET_KEY'] = 'cop290'
# app.config['UPLOAD']= upload_folder
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/photos/<filename>')
# def serve_photo(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# def save_photos(photos):
#     filenames = []
#     for photo in photos:
#         if photo:
#             filename = secure_filename(photo.filename)
#             photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             filenames.append(filename)
#     return filenames

# @app.route("/photos/<int:id>", methods=['GET', 'POST'])
# def photos(id):
#     if request.method == 'POST':
#         description = request.form.get('description')
#         photo1 = request.files.get('photo1')
#         photo2 = request.files.get('photo2')
#         photo3 = request.files.get('photo3')
#         photo_filenames = save_photos([photo1, photo2, photo3])
#         with engine.connect() as conn:
#             conn.execute(text("UPDATE user_table SET User_description=:description, Photolink1=:photo1, Photolink2=:photo2, Photolink3=:photo3 WHERE User_ID=:id"), {'description': description, 'photo1': photo_filenames[0], 'photo2': photo_filenames[1], 'photo3': photo_filenames[2], 'id': id})
#             conn.commit()
#         USER = database.get_photo_links(id)




@app.route('/', methods=['GET'])
def login():
    with connection.cursor() as cur:
        if request.method == 'GET':
            email = request.args.get('email')
            password = request.args.get('password')
            try:
                cur.execute("SELECT * FROM users1 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(type(user))
                # print(2)
                if user:
                    # print(3)
                    # cur.execute("SELECT * FROM users1 WHERE password=%s",(password,))
                    # result=cur.fetchone()
                    # cur.execute("GET users1 ")
                    print(user[3])
                    if password==user[3]:
                        print(4)
                        # print(user[0])
                        # print(user[1])

                        user_image=user[4].decode('utf-8')
                        print(user_image)
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
        if request.method == 'GET':
            username = request.args.get('username')
            email = request.args.get('email')
            password = request.args.get('password')
            password2 = request.args.get('password-verify')
            image=request.args.get('myfile')
            # image=request.files.get('myfile')
            print(username)
            print(image)
            # image=bytes(image_str,'utf-8')
            name= request.args.get('fullname')
            bio=request.args.get('text')
            print(1)
            try:
                print(1)
                cur.execute("SELECT * FROM users1 WHERE email=%s",(email,))
                user=cur.fetchone()
                print(1)
                if user:
                    print(type(user))
                    flash("Email already exists")
                    return redirect(url_for('signup'))
                else:
                    print(type(user))
                    if password==password2:
                        sql = f"INSERT INTO `users1` (username,email,password,image_name,bio) VALUES (%s,%s,%s,%s,%s)"
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
                        print(type(username))

                        print(type(name))
                        print(type(bio))
                        cur.execute(sql,(username,email,password,image,bio))
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
                cur.execute("SELECT * FROM users1 WHERE email=%s",(email,))
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


def get_photo_link(email):
    with connection.cursor() as conn:
        result = conn.execute(
        conn.execute("SELECT image FROM users1 WHERE email=%s",(email,)),
        user=conn.fetchone()
        )
        
        result_set = result.fetchall()
        links = []
        for row in result_set:
            links.append(row._asdict())
    return links[0]

@app.route('/forgotpasswordverify', methods = ['GET','UPDATE'])
def forgotpasswordverify():
    with connection.cursor() as cur:
        if request.method == 'GET':
            password = request.args.get('password')
            password2 = request.args.get('password-verify')

            if password==password2:
                sql = f"UPDATE INTO `users1` (password) VALUES (%s,%s,%s,%s,%s)"
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
    return render_template('profile.html')



@app.route('/edit_profile' , methods = ['GET','POST'])
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/profile.js')
def serve_js():
    return send_from_directory(app.static_folder, 'profile.js')

@app.route('/login.js')
def serve_js_login():
    return send_from_directory(app.static_folder, 'login.js')

@app.route('/AddPost', methods = ['GET' , 'POST'])
def AddPost():
    # create_table_query = """
    # CREATE TABLE IF NOT EXISTS posts (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     title VARCHAR (1000),
    #     content TEXT,
    #     user_id INT,
    #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    # )
    # """
    # insert_post_query = "INSERT INTO posts (title, content, user_id) VALUES (%s,%s, %s)"

    # with connection.cursor() as cur:
    #     if request.method == 'GET' :
    #         # email = request.args.get('email')
    #         post_title = request.args.get('comments')
    #         post_content = request.args.get('image')
    #         # user_id = fetch the user id using the user email from the users database table
    #         cur.execute(create_table_query)
    #         cur.execute(insert_post_query, (post_title, post_content, user_id))
    #         connection.commit()
    return render_template('AddPost.html')


@app.route('/index', methods = ['GET' , 'POST'])
def Home():
    return render_template('index.html')
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

