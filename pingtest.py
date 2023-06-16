import time,os,datetime,platform,smtplib,ssl,requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path

template = Template(Path("message.html").read_text())
ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT')

def check_ping(hostname):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'
    response = os.system("ping "+parameter+" 1 " + hostname)#windows
    if response == 0:
        pingstatus = f"Active"
    else:
        pingstatus = f"Inactive"
    return pingstatus

def check_status(hostname):
    try:
      code=requests.get("https://"+hostname).status_code
    except Exception as err:
      code=err
    return code

def Send_Mail(subject,message,ctx):
    body = template.substitute({ "message": message})
    smtp=smtplib.SMTP_SSL('mail server',port,context = ctx) # set mail server and port,default 465
    smtp.ehlo()
    # smtp.starttls()
    smtp.login(stmp_user,stmp_password)
    content["subject"] = subject  #mail title
    content.attach(MIMEText(body,"html"))
    status=smtp.send_message(content)
    if status=={}:
        print(subject,"mail send successful!")
    else:
        print(subject,"mail send failed!")
    smtp.quit()
    
content = MIMEMultipart()  
content["from"] = ""  #sender
content["to"] = "" #recive

## set here
hostname_list=[''] # webserver url
stmp_user='' # sender username
stmp_password='' # sender password

Send_Mail("Server Start Check Notify "+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),message,ctx)
while 1:
    now=(datetime.datetime.now().hour,datetime.datetime.now().minute)
    pingstatus_list=[]
    status_code_list=[]
    Warning=False
    message=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"""
        <table border="1" style="border-collapse:collapse;">
        <tr >
          <th style="padding: 10px;">主機</th>
          <th style="padding: 10px;">Ping</th>
          <th style="padding: 10px;">Status</th>
        </tr>
        <tr>
    """
    for _ in hostname_list:
        ping=check_ping(_)
        code=check_status(_)
        print(_,ping,code)
        message+=f'<td align="center" style="padding: 10px;">{_}</td>'
        if ping=='Inactive':
             message+=f'<td style="padding: 10px; background-color: rgba(255, 0, 0, 0.63);" align="center">{ping}</td>'
             Warning=True
        else:
             message+=f'<td align="center" style="padding: 10px;">{ping}</td>'

        if code==requests.codes.ok:
             message+=f'<td align="center" style="padding: 10px;">{code}</td>'
        else:
             message+=f'<td style="padding: 10px; background-color: rgba(255, 0, 0, 0.63);" align="center">{code}</td>'
             Warning=True
        message+="</tr>"
    
    message+="""
    </tr>
      </table>
    """

    #print(message)
    if Inactive: # when webserver is abnormal will send a notify mail
        Send_Mail("Server Abnormal Notify "+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),message,ctx)
    else:
        if now[0]==7: # when 7 o'clock will send a daliy mail
            Send_Mail("Daliy Check Server Status "+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),message,ctx)
    time.sleep(60*30) # check each half hour
