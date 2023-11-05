from flask import Flask , render_template, request
import os
from email.message import EmailMessage
import ssl
import smtplib
# import csv
from func import topsis
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def getValue():
    # file=request.form['inputFile']
    weights=request.form['Weights']
    impacts=request.form['Impacts']
    email=request.form['email']
    f = request.files['filename']

    f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
    app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

    file = "static/files/"+f.filename

    try:
        weights=weights.split(',')
        impacts=impacts.split(',')
    except:
        print('Error:Split using , only')

    try:
        top=topsis(file,weights,impacts)
    except:
        return render_template('error.html')
    top.to_csv("static/files/result.csv",index=False)

    # app = Flask(__name__, template_folder='templates')

    email_sender = 'mudrika587@gmail.com'
    email_password = 'jibargttqhobsrzr'

    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = 'Mail'
    em.set_content("Hey! Here is your topsis result.")
    with open("static/files/result.csv", 'rb') as fp:
        file_data = fp.read()
    em.add_attachment(file_data, maintype='text',subtype='csv',filename="result.csv")


    context = ssl.create_default_context()
    email_receiver = email
    em['To'] = email_receiver
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    # df=pd.read_csv(sys.argv[1])
    return render_template('pass.html')

    # return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)