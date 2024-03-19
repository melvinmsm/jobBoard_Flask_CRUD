from flask import Flask, render_template, jsonify, request
from flasgger import Swagger, swag_from
from db import mydb

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/')
def home():
    return render_template("index.html")

 
@app.route('/api/jobs', methods=['GET'])
@swag_from('swagger/get_jobs.yml')
def get_jobs():
    my_cur=mydb.cursor()
    my_cur.execute("SELECT * FROM JobBoard")
    jobs = my_cur.fetchall()
    return jsonify(jobs), 200


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
@swag_from('swagger/get_job.yml')
def get_job(job_id):
    my_cur=mydb.cursor()
    my_cur.execute("SELECT * FROM JobBoard WHERE jobID = %s", (job_id,))
    job = my_cur.fetchone()
    my_cur.close()
    if job:
        return jsonify(job), 200
    else:
        return jsonify({'error': 'Job Id not found'}), 404


@app.route('/api/jobs', methods=['POST'])
@swag_from('swagger/add_job.yml')
def add_job():
    data = request.json
    jobId=data.get('jobId')
    jobName = data.get('jobName')
    jobDescription = data.get('jobDescription')
    postingDate = data.get('postingDate')
    location = data.get('location')
    if jobId and jobName and jobDescription and postingDate and location:
        my_cur=mydb.cursor()
        my_cur.execute("INSERT INTO JobBoard (jobId, jobName, jobDescription, postingDate, location) VALUES (%s, %s, %s, %s, %s)", (jobId, jobName, jobDescription, postingDate, location))
        mydb.commit()
        return jsonify({'message': 'Job added successfully'}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
@swag_from('swagger/update_job.yml')
def update_job(job_id):
    data = request.json
    jobName = data.get('jobName')
    jobDescription = data.get('jobDescription')
    postingDate = data.get('postingDate')
    location = data.get('location')
    
    if jobName and jobDescription and postingDate and location:
        my_cur=mydb.cursor()
        my_cur.execute("UPDATE JobBoard SET jobName=%s, jobDescription=%s, postingDate=%s, location=%s WHERE jobId=%s", (jobName, jobDescription, postingDate, location, job_id))
        mydb.commit()
        return jsonify({'message': 'Job updated successfully'}), 200
    else:
        return jsonify({'error': 'Missing required fields'}), 400

    
@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
@swag_from('swagger/delete_job.yml')
def delete_job(job_id):
    my_cur = mydb.cursor()
    my_cur.execute("DELETE FROM JobBoard WHERE jobId = %s", (job_id,))
    mydb.commit()
    if my_cur.rowcount > 0:
        return jsonify({'message': 'Job deleted successfully'}), 200
    else:
        return jsonify({'error': 'Job not found'}), 404
    


if __name__ == '__main__':
    app.run(debug=True)