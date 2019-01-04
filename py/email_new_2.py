from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from email.utils import parseaddr,formataddr
import smtplib
# 输入Email地址和口令:
from_addr = input('From: ')
password = input('Password: ')
# 输入收件人地址:
to_addr = input('To: ')
# 输入SMTP服务器地址:
smtp_server = input('SMTP server: ')
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

msg=MIMEMultipart()
msg['From']=_format_addr('Python爱好者<%s>'%from_addr)
msg['To']=_format_addr('管理员<%s>'%to_addr)
msg['Subject']=Header('来自SMTP的问候。。。。。。','utf-8').encode()
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))

with open(r'C:\Users\拉布拉多搭\Desktop\1.png','rb') as f:
    mime=MIMEBase('image','png',filename='1.png')
    mime.add_header('Content-Disposition', 'attachment', filename='1.png')
    mime.add_header('Content-ID','<0>')
    mime.add_header('X-Attacheent-ID','0')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msg.attach(mime)
server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
#server.set_debuglevel(1)
#server.connect(smtp_server)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()