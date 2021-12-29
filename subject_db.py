from flask      import Flask, request, jsonify, current_app, render_template
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


db = {
    'user'     : 'root',
    'password' : '',
    'host'     : '127.0.0.1',
    'port'     : 3306,
    'database' : 'school'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"



def create_app(test_config=None):
    app=Flask(__name__)
    database=create_engine(DB_URL, encoding='utf-8', max_overflow=0)
    app.database=database

    @app.route("/status", methods=['GET'])
    def status():
        return "alive"


    @app.route("/show", methods=['GET'])
    def show():
        data=current_app.database.execute(text("""
            SELECT * from subjects
        """)).fetchall()

        temp1={}
        id=1
        for row in data:
            temp2={
                "name":row[0],
                "code":row[1],
                "department":row[2]
            }
            temp1[id]=temp2
            id+=1
        return temp1
    
    @app.route("/insert", methods=['POST'])
    def insert():
        info=request.json
        par={
            "name":info["name"],
            "code":info["code"],
            "department":info["department"]
        }

        current_app.database.execute(text("""
            INSERT INTO subjects(
                name,
                code,
                department
            ) VALUES(
                :name,
                :code,
                :department
            )
        """),par).lastrowid
        return 'Inserted\n'

    @app.route("/delete", methods=['POST'])
    def delete():
        info=request.json

        par={
            "name":info["name"],
            "code":info["code"],
            "department":info["department"]
        }

        current_app.database.execute(text("""
            DELETE FROM subjects
            WHERE name = :name
            AND code = :code
            AND department = :department
        """),par).lastrowid

        return 'Deleted\n'

    return app

