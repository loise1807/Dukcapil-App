from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from flask_restful import Resource, Api
import sqlite3 as sql

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
@app.route("/index",methods=['POST','GET'])
def index():
    nik = ''
    if request.method=='POST':
        nik=request.form['nik']
        con=sql.connect("dukcapil.db")
        cur=con.cursor()
        cur.execute("insert into t_dukcapil_check_result(nik_search) values (?)",(nik,))
        con.commit()
        flash('History Added','success')
    
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select *,m_religion.religion_name, m_marital_status.marital_status_desc from m_dukcapil_data join m_religion on m_religion.religion_id = m_dukcapil_data.religion_id join m_marital_status on m_marital_status.m_marital_status_id = m_dukcapil_data.martial_status where nik like '%" + nik +"%'")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/history",methods=['GET'])
def index_history():
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from t_dukcapil_check_result")
    data=cur.fetchall()
    return render_template("index_history.html",datas=data)


@app.route("/add_data",methods=['POST','GET'])
def add_data():
    if request.method=='POST':
        nik=request.form['nik']
        name=request.form['name']
        maiden_name=request.form['maiden_name']
        birth_date=request.form['birth_date']
        gender=request.form['gender']
        religion_id=request.form['religion_id']
        martial_status=request.form['martial_status']
        con=sql.connect("dukcapil.db")
        cur=con.cursor()
        cur.execute("select * from m_dukcapil_data where nik=?",(nik,))
        data=cur.fetchone()
        if data:
            flash('NIK ini sudah ada!','danger')
            return redirect(url_for("add_data"))
        else:
            cur.execute("insert into m_dukcapil_data(nik,name, maiden_name, birth_date, gender, religion_id, martial_status) values (?,?,?,?,?,?,?)",(nik,name, maiden_name, birth_date, gender, religion_id, martial_status))
            con.commit()
            flash('Data Added','success')
        return redirect(url_for("index"))
        
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from m_religion")
    data=cur.fetchall()
    cur2=con.cursor()
    cur2.execute("select * from m_marital_status")
    data2=cur2.fetchall()
    return render_template("add_data.html",datas=data, martials=data2)

@app.route("/edit_data/<string:m_dukcapil_data_id>",methods=['POST','GET'])
def edit_data(m_dukcapil_data_id):
    if request.method=='POST':
        nik=request.form['nik']
        name=request.form['name']
        maiden_name=request.form['maiden_name']
        birth_date=request.form['birth_date']
        gender=request.form['gender']
        religion_id=request.form['religion_id']
        martial_status=request.form['martial_status']
        con=sql.connect("dukcapil.db")
        cur=con.cursor()
        cur.execute("update m_dukcapil_data set nik=?, name=?, maiden_name=?, birth_date=?, gender=?, religion_id=?, martial_status=? where m_dukcapil_data_id=?",(nik,name, maiden_name, birth_date, gender, religion_id,martial_status,m_dukcapil_data_id))
        con.commit()
        flash('Data Updated','success')
        return redirect(url_for("index"))


    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from m_dukcapil_data where m_dukcapil_data_id=?",(m_dukcapil_data_id,))
    data=cur.fetchone()
    cur2=con.cursor()
    cur2.execute("select * from m_religion")
    dataR=cur2.fetchall()
    cur3=con.cursor()
    cur3.execute("select * from m_marital_status")
    dataM=cur3.fetchall()
    
    return render_template("edit_data.html",datas=data, dataR=dataR, dataM=dataM)

@app.route("/delete_data/<string:m_dukcapil_data_id>",methods=['GET'])
def delete_data(m_dukcapil_data_id):
    con=sql.connect("dukcapil.db")
    cur=con.cursor()
    cur.execute("delete from m_dukcapil_data where m_dukcapil_data_id=?",(m_dukcapil_data_id,))
    con.commit()
    flash('Data Deleted','warning')
    return redirect(url_for("index"))

@app.route("/add_religion",methods=['POST','GET'])
def add_religion():
    if request.method=='POST':
        religion_name=request.form['religion_name']
        con=sql.connect("dukcapil.db")
        cur=con.cursor()
        cur.execute("insert into m_religion(religion_name) values (?)",(religion_name,))
        con.commit()
        flash('Religion Added','success')
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from m_religion")
    data=cur.fetchall()
    return render_template("add_religion.html",datas=data)

@app.route("/add_martial",methods=['POST','GET'])
def add_martial():
    if request.method=='POST':
        marital_status_desc=request.form['marital_status_desc']
        con=sql.connect("dukcapil.db")
        cur=con.cursor()
        cur.execute("insert into m_marital_status(marital_status_desc) values (?)",(marital_status_desc,))
        con.commit()
        flash('Martial Status Added','success')
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from m_marital_status")
    data=cur.fetchall()
    return render_template("add_martial.html",datas=data)

@app.route("/detail_data?<string:nik>", methods=['GET'])
def detail_data(nik):
    
    con=sql.connect("dukcapil.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select *,m_religion.religion_name, m_marital_status.marital_status_desc from m_dukcapil_data join m_religion on m_religion.religion_id = m_dukcapil_data.religion_id join m_marital_status on m_marital_status.m_marital_status_id = m_dukcapil_data.martial_status where nik=?",(nik,))
    data=cur.fetchone()
    
    return render_template("detail_data.html",datas=data)




if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8000, debug=False)
