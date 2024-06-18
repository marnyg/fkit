from flask import Flask, request, render_template_string
import requests
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
 
backend_host = os.getenv('BACKEND_HOST', 'backend')
backend_port = os.getenv('BACKEND_PORT', '5001')
backend_url = f'http://{backend_host}:{backend_port}/execute'

@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info('Request method: %s', request.method)
    if request.method == 'POST':
        sql_query = request.form['query']
        app.logger.info('SQL Query: %s', sql_query)
        response = requests.post(backend_url, json={'query': sql_query})
        result = response.json()
        return render_template_string(FORM_TEMPLATE, result=result['result'])
    return render_template_string(FORM_TEMPLATE)

FORM_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>SQL Executor</title>
</head>
<body>
    <h1>Enter SQL Query</h1>
    <form method=post>
        <textarea name=query rows=10 cols=40>{{ request.form.query }}</textarea>
        <br>
        <input type=submit value=Execute>
    </form>
    <button onclick="setQuery('CREATE TABLE test (id SERIAL PRIMARY KEY, name VARCHAR(50));')">Create Table</button>
    <button onclick="setQuery('INSERT INTO test (name) VALUES (\\'Sample Name\\');')">Insert Data</button>
    <button onclick="setQuery('SELECT * FROM test;')">Get Data</button>
    <p>{{ result }}</p>
    <script>
        function setQuery(query) {
            document.querySelector('textarea[name=query]').value = query;
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print('App started')
