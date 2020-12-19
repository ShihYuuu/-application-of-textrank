from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import smtplib   
from email.mime.multipart import MIMEMultipart #email內容載體
from email.mime.text import MIMEText #用於製作文字內文
from email.mime.base import MIMEBase #用於承載附檔
from email import encoders #用於附檔編碼
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ajax.html')

@app.route('/getjob/')
def getjob():
    job = str(request.args.get('pro'))
    address = str(request.args.get('add'))
    print('==========')
    print(address)
    
    contents = makeMail(job)
    sendMail(contents, address)
    
    return job

def makeMail(job):
    mapping = {
        'engineer' : pd.read_csv("profession/engineer.csv", encoding='UTF-8'),
        'teacher' : pd.read_csv("profession/teacher.csv", encoding='UTF-8'),
        'waiter' : pd.read_csv("profession/waiter.csv", encoding='UTF-8')
    } 
    df = mapping.get(job)
    num = random.randint(0,3)
    
    text_company = df.at[num, '公司名稱']
    text_introduce = df.at[num, '公司簡介']
    text_job = df.at[num, '職缺名稱']
    text_content = df.at[num, '工作內容']
    text_url = df.at[num, '網址']
    
    contents = text_company
    contents += '\n\n求職者您好，在此提供您本公司的職缺介紹\n'
    contents += '\n公司簡介：\n' + text_introduce +'\n'
    contents += '\n職缺介紹：' + text_job + '\n' + text_content + '\n'
    contents += '\n如您有意應徵本公司，請參考以下網址：\n' + text_url
    
    print('========== write an e-mail ==========')
    return contents
    
def sendMail(contents, address):
    #設定要使用的Gmail帳戶資訊
    gmail_sender = 'thankyou0829@gmail.com'
    gmail_password = 'shihyu0111'
    gmail_receiver = address

    #開始組合信件內容
    mail = MIMEMultipart()
    mail['From'] = 'NTHU Job Site'
    mail['To'] = gmail_receiver
    mail['Subject'] = '企業徵才'
    mail.attach(MIMEText(contents))
    
    #設定smtp伺服器並寄發信件    
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(gmail_sender, gmail_password)
    smtpserver.sendmail(gmail_sender, gmail_receiver, mail.as_string())
    smtpserver.quit()
    print('========== send an e-mail ==========')
    return

if __name__ == '__main__':
    app.run()