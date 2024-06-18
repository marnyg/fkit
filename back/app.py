from flask import Flask, request, jsonify
import psycopg2
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    app.logger.info('Connecting to database with the following parameters:')
    app.logger.info('dbhost=%s', os.environ['POSTGRES_HOST'])
    app.logger.info('dbname=%s', os.environ['POSTGRES_DB'])
    app.logger.info('user=%s', os.environ['POSTGRES_USER'])

    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST']
    )
    app.logger.info('Connected to database')
    return conn

@app.route('/execute', methods=['POST'])
def execute_query():
    app.logger.info('Request method: %s', request.method)
    data = request.get_json()
    app.logger.info('SQL Query: %s', data['query'])
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

