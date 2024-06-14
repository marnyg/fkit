from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        if 'query' in request.form:
            sql_query = request.form['query']
            response = requests.post('http://backend:5001/execute', json={'query': sql_query})
            result = response.json()
    return render_template_string(FORM_TEMPLATE, result=result)

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
