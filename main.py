from flask import Flask, render_template, request
import pymysql.cursors
from google.cloud import storage
import os
app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'quiz7-cloud-project-6acfa86a258e.json'
connection = pymysql.connect(host="35.222.35.31",
                                 user="root",
                                 password="clouddbpassword",
                                 db="clouddb",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

sql = '''SELECT * FROM data'''

cursor = connection.cursor()
cursor.execute(sql,)
#result = cursor.fetchall()


def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    #blob.upload_from_filename(source_file_name)
    blob.upload_from_file(source_file_name)
@app.route('/')
def hello_world():
    #create_bucket('veryveryuniquename')
    return render_template('common.html',)

@app.route('/question1')
def question1():
    return render_template('question1.html')
@app.route('/question1_execute', methods=['POST'])
def question1_execute():
    file = request.files['file']
    #upload_blob('veryveryuniquename',file,'my_image')
    print(file.filename)
    return 'success'

@app.route('/question2')
def question2():
    return render_template('question2.html')
@app.route('/question2_execute', methods=['POST'])
def question2_execute():
    sql = "SELECT * FROM data"
    cursor.execute(sql,)
    result = cursor.fetchall()
    print(result)
    url = []
    year = []
    fname = []
    fdesc = []
    for row in result:
        url.append(row['url'])
        year.append(row['year'])
        fname.append(row['name'])
        fdesc.append(row['desc'])


    return render_template('question2.html',result=result,url=url,year=year,fname=fname, fdesc=fdesc)

@app.route('/question3')
def question3():
    return render_template('question3.html')
@app.route('/question3_execute', methods=['GET'])
def question3_execute():
    year = str(request.args.get('year'))
    cname = str(request.args.get('cname'))
    if year !='' and cname !='':
        print('1')
        sql = "SELECT * FROM data where name = " + "'" +cname + "'"+" and year = " + year
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        lent = len(result)
        url = []
        year = []
        fname = []
        fdesc = []
        for row in result:
            url.append(row['url'])
            year.append(row['year'])
            fname.append(row['name'])
            fdesc.append(row['desc'])
    # return render_template('question3.html', result=result, url=url, year=year, fname=fname, fdesc=fdesc)
    if year is not None and cname  == '':
        print('2')
        sql = "SELECT * FROM data where year = " + year
        cursor.execute(sql)
        result = cursor.fetchall()
        lent = len(result)
        url = []
        year = []
        fname = []
        fdesc = []
        for row in result:
            url.append(row['url'])
            year.append(row['year'])
            fname.append(row['name'])
            fdesc.append(row['desc'])
    if cname is not None and year == '':
        print('2')
        sql = "SELECT * FROM data where name = " + "'" + cname + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        lent = len(result)
        url = []
        year = []
        fname = []
        fdesc = []
        for row in result:
            url.append(row['url'])
            year.append(row['year'])
            fname.append(row['name'])
            fdesc.append(row['desc'])
    return render_template('question3.html', result=result, url=url, year=year, fname=fname, fdesc=fdesc,lent=lent)
if __name__ == '__main__':
    app.run()
