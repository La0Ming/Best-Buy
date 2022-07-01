from flask import Flask

app = Flask(__name__)

@app.route('/')
def run_script():
    file = open(r'C:\Users\johnn\Downloads\database-project-master-windows\database-project-master-windows\cgi-bin\index.py', 'r').read()
    return exec(file)

if __name__ == "__main__":
    app.run(port='8000', debug=True)