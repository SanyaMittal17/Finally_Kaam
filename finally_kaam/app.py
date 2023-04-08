from flask import Flask,render_template
from flask import Blueprint
app= Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/forgotpassword')
def forgotpassword():
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