from flask import Flask,render_template, request
from flask import Blueprint
app= Flask(__name__)
app.config['SECRET KEY'] = 'cop290'
@app.route('/', methods=['GET','POST'])

def login():
    if request.method == 'POST':
        email = request.form('email')
        password = request.form('password')
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
       username = request.form('username')
       email = request.form('email')
       password1 = request.form('password')
       password2 = request.form('confirm-password')
    return render_template('signup.html')

@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form('email')
    return render_template('forgotpassword.html')

@app.route('/forgotpasswordverify')
def forgotpasswordverify():
    return render_template('forgotpasswordverify.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')
@app.route('/AddPost')
def AddPost():
    return render_template('AddPost.html')
if __name__ =="__main__":
    app.run(debug=True)
