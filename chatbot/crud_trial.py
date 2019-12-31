import json

import psycopg2
from flask import Flask, request

app = Flask(__name__)  # app initialisation
conn = psycopg2.connect(database="crud_trials", user="crud_trials", password="crud_trials",
                        host="127.0.0.1", port="5432")
cur = conn.cursor()


# CREATE
@app.route('/create', methods=['POST'])
def create():
    name = request.json['Name']
    sql = "insert into data values('%s')" % name
    cur.execute(sql)
    conn.commit()
    response = {'Message': 'Success'}
    return json.dumps(response)


# READ
@app.route('/read', methods=['GET'])
def read():
    sql = """select * from data"""
    cur.execute(sql)
    data = cur.fetchall()
    response = {'Name': data[-1]}
    return json.dumps(response)


# UPDATE
@app.route('/update', methods=['PUT'])
def update():
    name = request.json['Name']
    sql = f"""update data set name = '{name}'"""
    cur.execute(sql)
    conn.commit()
    response = {'Message': 'Success'}
    return json.dumps(response)


# DELETE
@app.route('/delete', methods=['DELETE'])
def delete():
    name = request.json['Name']
    sql = f"""delete from data where name = '{name}'"""
    cur.execute(sql)
    conn.commit()
    response = {'Message': 'Success'}
    return json.dumps(response)


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=8000)
