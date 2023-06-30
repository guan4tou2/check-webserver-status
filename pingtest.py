import time,os,datetime,platform,smtplib,ssl,requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path

ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT')
template = Template(Path("message.html").read_text())

#config here
#####################################################
sender=""
recipient=""
cc_list=["",""]
hostname_list=['','']
stmp_user=''
stmp_password=''
delay_time=60*30 #check every half hour
####################################################


def now():
    return datetime.datetime.now()

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
        result=requests.get("https://"+hostname).status_code
        print(hostname,result)
        return result
    except Exception as err:
        print(hostname,err)
        return err

def Send_Mail(subject,message,ctx):
    content = MIMEMultipart() 

    content["from"] = sender  
    content["to"] = recipient 
    # content["cc"] = ",".join(cc_list) # if need cc,remove this comment out
    content["subject"] = subject 

    smtp=smtplib.SMTP_SSL('mail.nfu.edu.tw',465,context = ctx)
    smtp.ehlo()
    # smtp.starttls()
    smtp.login(stmp_user,stmp_password)
    
    body = template.substitute({ "message": message})
    content.attach(MIMEText(body,"html"))
    status=smtp.send_message(content)
    if status=={}:
        print(subject,"郵件傳送成功!")
    else:
        print(subject,"郵件傳送失敗!")
    smtp.quit()

Send_Mail("Server Check Start "+now().strftime("%Y/%m/%d %H:%M:%S"),"Start daily check",ctx)

flag=True
while 1:
    pingstatus_list=[]
    status_code_list=[]
    Inactive=False
    message=now().strftime("%Y/%m/%d %H:%M:%S")+"""
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
        message+=f'<td align="center" style="padding: 10px;">{_}</td>'
        if ping=='Inactive':
             message+=f'<td style="padding: 10px; background-color: rgba(255, 0, 0, 0.63);" align="center">{ping}</td>'
        else:
             message+=f'<td align="center" style="padding: 10px;">{ping}</td>'

        if code==requests.codes.ok:
             message+=f'<td align="center" style="padding: 10px;">{code}</td>'
        else:
             message+=f'<td style="padding: 10px; background-color: rgba(255, 0, 0, 0.63);" align="center">{code}</td>'
        message+="</tr>"

    message+="""
    </tr>
      </table>
    """
    if now().hour!=7:
        flag=True
    if Inactive:
        Send_Mail("Server Inactive Notify "+now().strftime("%Y/%m/%d %H:%M:%S"),message,ctx)
    else:
        if now().hour==7 and flag:
            Send_Mail("Daliy Check Server Status "+now().strftime("%Y/%m/%d %H:%M:%S"),message,ctx)
            flag=False
    time.sleep(delay_time)  
