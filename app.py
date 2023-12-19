
from flask import (Flask,
    render_template,
    request, redirect,
    url_for, flash,
    session,
)

from werkzeug.utils import secure_filename
from functools import wraps
import os, random, secrets
import sqlite3 as sql

try: os.mkdir('static')
except: pass

try: os.mkdir('static/files')
except: pass

app=Flask(__name__)
app.app_context().push()

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key


UPLOAD_FOLDER ="static/files"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    con=sql.connect("mydb/db_sample.db")

    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=con.cursor()
        cur.execute("select UNAME from users where EMAIL=? and UPASS=?",(email,pwd))
        data=cur.fetchone()

        if data:
            session['logged_in']=True
            session['username']=data[0]
            flash('Login Successfully','success')
            return render_template('home.html')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")
  

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  

@app.route('/reg',methods=['POST','GET'])
def reg():
    # error = 'Only ADMIN can make CRUD Operation.'
    # return render_template('404.html', error=error), 404

    status=False
    con=sql.connect("mydb/db_sample.db")

    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=con.cursor()
        cur.execute("insert into users(UNAME,UPASS,EMAIL) values(?,?,?)",(name,pwd,email))
        con.commit()
        cur.close()
        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template("reg.html",status=status)


@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))


@app.route("/add_user/<database>/<table>", methods=['POST','GET'])
@is_logged_in
def add_user(database, table):

    con=sql.connect(f"mydb/{database}.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute(f"select * from {table}")    
    uname = []
    ques = []

    if request.method=='POST':
        col_name = [description[0] for description in cur.description[1:-1]]
        for i in col_name:
            uname.append(request.form[i])
            ques.append('?')

        if 'file' not in request.files:
            flash('No file part','danger')

        file = request.files['file']
        if file.filename == '':
            flash('No file selected','danger')

        if file:
            filename, file_extension = os.path.splitext(file.filename)
            new_filename = secure_filename(filename+str(random.randint(10000,99999))+"."+file_extension)
            file.save(os.path.join(app.root_path, UPLOAD_FOLDER, new_filename))

            uname.append(new_filename)
            col_name.append('FILE')
            ques.append('?')

        ques = ','.join([i for i in ques])
        col_name = ','.join([i for i in col_name])

        cur.execute(f"insert into {table}({col_name}) values ({ques})", tuple(uname))
        con.commit()

        flash('Currency Added','success')
        cur.execute(f"select * from {table}")
        data=cur.fetchall()

        col_name = [description[0] for description in cur.description[1:-1]]
        con.commit()

        return render_template("index.html", 
            datas=data, 
            database=database,
            table=table,
            ecol_name=enumerate(col_name),
            col_name=col_name,
        )

    col_name = [description[0] for description in cur.description[1:-1]]
    return render_template("add_user.html", 
        table=table,
        database=database,
        col_name=enumerate(col_name)
    )


@app.route("/edit_user/<database>/<table>/<string:uid>",methods=['POST','GET'])
@is_logged_in
def edit_user(database, table, uid):

    con=sql.connect(f"mydb/{database}.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute(f"select * from {table}")    
    uname = []

    if request.method=='POST':
        col_name = [description[0] for description in cur.description[1:-1]]

        for i in col_name:
            uname.append(request.form[i])

        if 'file' not in request.files:
            flash('No file part','danger')

        file = request.files['file']
        if file.filename == '':
            flash('No file selected','warning')
            col_name = ','.join([f'{i}=?' for i in col_name])

            uname.append(uid)
            cur.execute(f"update {table} set {col_name} where UID=?", tuple(uname))
            con.commit()

        else:
            if file:
                filename, file_extension = os.path.splitext(file.filename)
                new_filename = secure_filename(filename+str(random.randint(10000,99999))+"."+file_extension)
                file.save(os.path.join(app.root_path, UPLOAD_FOLDER, new_filename))

                uname.append(new_filename)
                col_name.append('FILE')

            col_name = ','.join([f'{i}=?' for i in col_name])
            data = cur.execute(f"select FILE from {table} where UID=?",(uid,)).fetchall()

            data = f'./static/files/{data[0][0]}'
            os.remove(data)

            uname.append(uid)
            cur.execute(f"update {table} set {col_name} where UID=?", tuple(uname))
            con.commit()

        flash('Currency Updated','success')
        cur.execute(f"select * from {table}")
        data=cur.fetchall()

        col_name = [description[0] for description in cur.description[1:-1]]
        con.commit()

        return render_template("index.html", 
            datas=data, 
            database=database,
            table=table,
            ecol_name=enumerate(col_name),
            col_name=col_name,
        )
    
    cur.execute(f"select * from {table} where UID=?",(uid,))
    data=cur.fetchone()

    col_name = [description[0] for description in cur.description[1:-1]]
    return render_template("edit_user.html", 
        table=table,
        datas=data,
        database=database,
        col_name=enumerate(col_name)
    )

@app.route("/delete_user/<database>/<table>/<string:uid>",methods=['GET'])
@is_logged_in
def delete_user(database, table, uid):

    con=sql.connect(f"mydb/{database}.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    data = cur.execute(f"select FILE from {table} where UID=?",(uid,)).fetchall()
    data = f'static/files/{data[0][0]}'
    os.remove(data)

    cur.execute(f"delete from {table} where UID=?",(uid,))
    con.commit()

    flash('Currency Deleted','warning')
    cur.execute(f"select * from {table}")
    data=cur.fetchall()

    col_name = [description[0] for description in cur.description[1:-1]]
    con.commit()

    return render_template("index.html", 
        datas=data, 
        database=database,
        table=table,
        ecol_name=enumerate(col_name),
        col_name=col_name,
    )
     
@app.route("/", methods=['GET', 'POST'])
@is_logged_in
def home():
    
    if request.method=='POST':
        mydb = request.form["mydb"]
        table = request.form["table"]
        
        sql3 = request.form["make_table"]
        my_db = f'mydb/{mydb}.db'

        sql3 = f'''CREATE TABLE IF NOT EXISTS {table} (
"UID" INTEGER PRIMARY KEY AUTOINCREMENT,
{sql3}
"FILE" TEXT
)'''

        con = sql.connect(my_db)
        cur = con.cursor()
        # cur.execute(f"DROP TABLE IF EXISTS {table}")
        
        cur.execute(sql3)
        con.commit()
        con.close()
        
        link = url_for('index', database=mydb, table=table)
        return redirect(link)
    else:
        return render_template('home.html')


@app.route("/index/<database>/<table>")
@is_logged_in
def index(database, table):
    con=sql.connect(f"mydb/{database}.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute(f"select * from {table}")
    data=cur.fetchall()
    col_name = [description[0] for description in cur.description[1:-1]]
    con.commit()

    return render_template("index.html", 
        datas=data, 
        database=database,
        table=table,
        ecol_name=enumerate(col_name),
        col_name=col_name,
    )


@app.errorhandler(404)
def page_not_found(e):
    error = 'Error 404, Page Not Found.'
    return render_template('404.html', error=error), 404


if __name__=='__main__':
    app.run(debug=True)
