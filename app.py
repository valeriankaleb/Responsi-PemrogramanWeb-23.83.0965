from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from mysql import connector
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db = connector.connect(
    host = "r77at.h.filess.io",
    database = "dbkuliah0965_impossible",
    port = "3307",
    user = "dbkuliah0965_impossible",
    password = "edb82a415186170afa6207e88f7f34e81589f0ca"
)

if db.is_connected():
    print('open connection successful')

@app.route('/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("select * from tbl_mahasiswa")
    res = cur.fetchall()
    cur.close()
    return render_template('index.html', hasil=res)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim  = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    cur = db.cursor()
    cur.execute('INSERT INTO tbl_mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)', (nim, nama, asal))
    db.commit()
    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    cur = db.cursor()
    cur.execute('select * from tbl_mahasiswa where nim=%s', (nim,))
    res = cur.fetchall()
    cur.close()
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    no_mhs  = request.form['nim_ori']
    nim     = request.form['nim']
    nama    = request.form['nama']
    asal    = request.form['asal']
    cur = db.cursor()
    sql = "UPDATE tbl_mahasiswa SET nim=%s, nama=%s, asal=%s WHERE nim=%s"
    value = (nim, nama, asal, no_mhs)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('halaman_awal'))

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    cur = db.cursor()
    cur.execute('DELETE from tbl_mahasiswa where nim=%s', (nim,))
    db.commit()
    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run()