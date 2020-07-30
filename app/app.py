from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import sys

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'bestActor'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Robert Deniro Complete List of Movie'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM robert_Deniro')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, Title=result)


@app.route('/view/<string:Title>', methods=['GET'])
def record_view(Title):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM robert_Deniro WHERE Title=%s', Title)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', movie=result[0])


@app.route('/edit/<string:Title>', methods=['GET'])
def form_edit_get(Title):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM robert_Deniro WHERE Title=%s', Title)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', movie=result[0])


@app.route('/edit/<string:Title>', methods=['POST'])
def form_update_post(Title):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Title'), request.form.get('Year'), request.form.get('Score'), Title)

    sql_update_query = """UPDATE robert_Deniro t SET t.Title = %s, t.Year = %s, t.Score = %s WHERE t.Title = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/Title/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Movie Form')


@app.route('/Title/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Title'), request.form.get('Year'), request.form.get('Score'))

    sql_insert_query = """INSERT INTO robert_Deniro (Title,Year,Score) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<string:Title>', methods=['POST'])
def form_delete_post(Title):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM robert_Deniro WHERE Title = %s """
    cursor.execute(sql_delete_query, Title)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/Title', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM robert_Deniro')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Title/<string:Title>', methods=['GET'])
def api_retrieve(Title) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM robert_Deniro WHERE Title=%s', Title)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Title/', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Title'], content['Year'], content['Score'])
    sql_insert_query = """INSERT INTO robert_Deniro (Title,Year,Score) 
    VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/Title/<string:Title>', methods=['PUT'])
def api_edit(Title) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    print("hello", file=sys.stderr)
    print(content, file=sys.stderr)
    inputData = (content['Title'], content['Year'], content['Score'], Title)
    sql_update_query = """UPDATE robert_Deniro t SET t.Title = %s, t.Year = %s, t.Score = %s WHERE t.Title = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Title/<string:Title>', methods=['DELETE'])
def api_delete(Title) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM robert_Deniro WHERE Title = %s """
    cursor.execute(sql_delete_query, Title)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)