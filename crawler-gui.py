#coding:utf-8  #强制使用utf-8编码格式
import urllib2
import gzip,StringIO
import sys
import re
import tkMessageBox
import time
from datetime import datetime
import smtplib #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
from Tkinter import *
reload(sys)
sys.setdefaultencoding('utf-8')
my_sender='binjie_lee@163.com' #发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user='360256286@qq.com' #收件人邮箱账号，为了后面易于维护，所以写成了变量
flag=True
def mail():
	ret=True
  	try:
	    msg=MIMEText('for someone','plain','utf-8')
	    msg['From']=formataddr(["李斌杰",my_sender])  #括号里的对应发件人邮箱昵称、发件人邮箱账号
	    msg['To']=formataddr(["Zephyr",my_user])  #括号里的对应收件人邮箱昵称、收件人邮箱账号
	    msg['Subject']="come on, have seats!!!" #邮件的主题，也可以说是标题
	 
	    server=smtplib.SMTP("smtp.163.com",25) #发件人邮箱中的SMTP服务器，端口是25
	    server.login(my_sender,"holy520")  #括号中对应的是发件人邮箱账号、邮箱密码
	    server.sendmail(my_sender,my_user,msg.as_string())  #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
	    server.quit()  #这句是关闭连接的意思
	except Exception,e:
		print e
  	return ret

global count
count = 0
def accessPage():
	global count
	url = "http://www.testdaf.de/fuer-teilnehmende/die-pruefung/testzentren/testzentren-weltweit-von-a-bis-c/testzentren-weltweit-von-t-bis-z/#anker_t"
	headers = { 
           "host":"www.testdaf.de",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://www.testdaf.de/fuer-teilnehmende/die-pruefung/testzentren/testzentren-weltweit-von-a-bis-c/",
			"Cookie": "fe_typo_user=a422349c0b5c57880e7179ccd172b2cd",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1"
		}
	req=urllib2.Request(url,headers = headers)
	content = urllib2.urlopen(req).read()
	compressedstream = StringIO.StringIO(content)   
	gzipper = gzip.GzipFile(fileobj=compressedstream)      
	data = gzipper.read()
	fp_raw = open('temp2.txt',"w+")
	fp_raw.write(data)
	fp_raw.close()
	print "Get Information"
	content = ''
	fp = open('temp2.txt',"r")
	lines = fp.readlines()
	for line in lines:
		content += line
	fp.close()
	#print "Now Taibei: \n"
#pattern1 = re.compile(ur'National Kaohsiung First University of Science &amp; Technology\s*<\/a>\s*?<\/li>\s*?<a .*?>\s*?<li.*?>\s*<div.*?;">\s*?(.*?)\s*?<\/div>')
	pattern2 = re.compile(ur'The Language Training and Testing Center Taipei\s*<\/a>\s*?<\/li>\s*?<a .*?>\s*?<li.*?>\s*<div.*?;">\s*?(.*?)\s*?<\/div>')
#pattern2 = re.compile(ur'Hello language centre s.r.o.\s*<\/a>\s*?<\/li>\s*?<a .*?>\s*?<li.*?>\s*<div.*?;">\s*?(.*?)\s*?<\/div>')

	havingMatch2 = re.search(pattern2,content.decode('utf8'))
	if havingMatch2:
		time = datetime.now()
		print time, "    The Language Testing and Training Center Taibei has the seats"
		if count <= 3:
			ret = mail()
			count = count + 1
	else: 
		time = datetime.now()
		print time, "     No Seats Now..\n"
		count = 0
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.helloLabel = Label(self, text='考位提醒')
        self.helloLabel.pack()
        self.helloLabel = Label(self, text='请输入你的邮箱')
        self.helloLabel.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.helloLabel = Label(self, text='注：一旦发现有考位，立即发送邮件到您所填写的邮箱中去')
        self.helloLabel.pack()
        self.alertButton = Button(self, text='确认', command=self.recommand)
        self.alertButton.pack()
        self.alertButton = Button(self, text='停止', command=self.stoprun)
        self.alertButton.pack()
    def recommand(self):
        email = self.nameInput.get()
        my_user = email
        accessPage()
        tkMessageBox.showinfo('Message', '正在努力查询，请勿关闭！')
        flag = True
        while(1):
       		time.sleep(30)
       		accessPage()
       		if flag == False:
       			break
    def stoprun(self):
    	flag = False
    	tkMessageBox.showinfo('Message', '已关闭！')
app = Application()
# 设置窗口标题:
app.master.title('德语国外考位提醒')
# 主消息循环:
app.mainloop()