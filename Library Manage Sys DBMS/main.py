from flask import Flask, render_template, request, redirect
from flask_mysqldb import *
import config_lib as conf

app = Flask(__name__)

# dbobj = yaml.load(open('config.yaml'))
app.config['MYSQL_HOST'] = conf.getHost()
app.config['MYSQL_USER'] = conf.getuser()
app.config['MYSQL_PASSWORD'] = conf.getPwd()
app.config['MYSQL_DB'] = conf.getDatabase()

mysql = MySQL(app)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        user_role = userDetails['select']

        if user_role.lower() == "admin":
            print(username, password, user_role)
            cur = mysql.connection.cursor()
            result = cur.execute(f"select username from adminTable where pwd='{password}'")
            cur.close()
            if result > 0:
                print(result)
                return render_template("homePage_admin.html")
        elif user_role.lower() == "student":
            cur = mysql.connection.cursor()
            result = cur.execute(f"select username from studentTable where pwd='{password}'")
            cur.close()
            if result > 0:
                print(result)
                return render_template("homePage_student.html")
        else:
            return "User doesn't exist!"

    return render_template("loginPage.html")


@app.route('/bookStatus')
def bookStatus():
    return render_template("bookStatus.html")


@app.route('/libInventory')
def bookInventory():
    cur = mysql.connection.cursor()
    result = cur.execute("select * from inventoryBook")
    if result > 0:
        bookDetails = cur.fetchall()
        return render_template("inventoryBook.html", bookDetails=bookDetails)


@app.route('/allotBook')
def allot_book():
    return render_template("allot_book.html")


@app.route('/returnBook')
def returnBook():
    return render_template("return_book.html")


@app.route('/homePage_ad')
def homePage_admin():
    return render_template("homePage_admin.html")


@app.route('/homePage_stu')
def homePage_student():
    return render_template("homePage_student.html")


# add new entities
@app.route('/add_book')
def new_book():
    userDetails = request.form
    username = userDetails['username']
    password = userDetails['password']
    user_role = userDetails['select']
    return render_template("add_book.html")


@app.route('/add_admin')
def new_admin():
    return render_template("add_admin.html")


@app.route('/add_student')
def new_student():
    return render_template("add_student.html")


# remove entities
@app.route('/remove_book')
def remove_book():
    return render_template("remove_book.html")


@app.route('/remove_admin')
def remove_admin():
    return render_template("remove_admin.html")


@app.route('/remove_student')
def remove_student():
    return render_template("remove_student.html")


if __name__ == '__main__':
    app.run(debug=True)
