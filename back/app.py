from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host='db'
    )
    return conn

@app.route('/execute', methods=['POST'])
def execute_query():
    data = request.get_json()
    query = data['query']
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        if query.lower().startswith('select'):
            result = cur.fetchall()
        else:
            result = cur.statusmessage
        conn.commit()
    except Exception as e:
        result = str(e)
    finally:
        cur.close()
        conn.close()
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

