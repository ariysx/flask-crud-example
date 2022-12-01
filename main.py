from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'helloworld'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.170.86.71'
mysql.init_app(app)

@app.route("/add") #Add Student
def add():
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email) # kludge - use stored proc or params
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Success"}' # uhm

@app.route("/remove")
def remove():
  id = request.args.get('id')
  cur = mysql.connection.cursor()
  s='''DELETE FROM students WHERE studentID = {}'''.format(id)
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Success"}' # uhm

@app.route("/update")
def update():
  id = request.args.get('id')
  name = request.args.get('name')
  email = request.args.get('email')
  cur = mysql.connection.cursor()
  s='''UPDATE students SET studentName='{}', email='{}' WHERE studentID = {}'''.format(name, email, id)
  cur.execute(s)
  mysql.connection.commit()

  return '{"Result":"Success"}' # uhm

@app.route("/view")
def view():
  cur = mysql.connection.cursor()  # create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''')  # execute an SQL statment
  rv = cur.fetchall()  # Retreive all rows returend by the SQL statment
  Results = []
  strHTML = ""
  for row in rv:  # Format the Output Results and add to return string
    Result = {}
    Result['Name'] = row[0].replace('\n', ' ')
    Result['Email'] = row[1]
    Result['ID'] = row[2]
    Results.append(Result)
    strHTML += "<tr><td>"+str(row[2])+"</td><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
  return "<table style=\"border: 2px solid #abc5f9; margin: auto; padding: 2rem;\"><tr><th>ID</th><th>Name</th><th>Email</th></tr>" + strHTML + "</table>"

@app.route("/hello") #Add Student
def hello():
  return '{"Result":"Success"}' # Really? maybe we should check!  
  
@app.route("/") #Default - Show Data
def read(): # Name of the method
  cur = mysql.connection.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080

