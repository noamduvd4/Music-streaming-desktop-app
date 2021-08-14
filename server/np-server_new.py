import os
import socket
from threading import Thread
from Queue import Queue
from server_song_send import *
from login import *
from client_upload import *
from reportlog import *
from delete_song import *
from remove_user import *
from admin_creator import *
from view_pending import *
from send_report_log import *
CONCURRENT = 20
port=1262

q=Queue(CONCURRENT*2)
f=0
def doWork():
    while True:
        #pool next conncetion from the queue
        conn, addr=q.get()
        choice=conn.recv(1024)
        uname=conn.recv(1024)
        upassword=conn.recv(1024)
        if uname=="-1" or upassword=="-1":
            print "done"
            q.task_done()
        else:
            upassword=upassword.decode("base64")
            print uname
            userdata=loggin(uname,upassword,choice)
            
            if choice== "2":
                conn.send(str(userdata[0]))
                while not userdata[0]:
                    uname=conn.recv(1024)
                    upassword=conn.recv(1024)
                    userdata=loggin(uname,upassword,choice)
                    conn.send(str(userdata[0]))
                upassword=conn.recv(1024)
                upassword=upassword.decode("base64")
                if (upassword!=""):
                    userdata=loggin(uname,upassword,"3")
                    conn.send(str(userdata[0]))
                
            if choice == "1":
                print userdata
                conn.send(str(userdata[0]))
                print conn.recv(1024)
                conn.send(str(userdata[1]))
                while userdata[0]==False:
                    uname=conn.recv(1024)
                    upassword=conn.recv(1024)
                    upassword=upassword.decode("base64")
                    print uname
                    userdata=loggin(uname,upassword,choice)
                    print userdata
                    conn.send(str(userdata[0]))
                    print conn.recv(1024)
                    conn.send(str(userdata[1]))
                              
            choice = str(conn.recv(1024))
            print choice
            if choice =="-1":
                conn.close()
                q.task_done()
                print "done"
            while choice!="-1":
                if choice=="1":
                    song_request(conn, addr)
                if choice == "2":
                    client_song_upload(conn , addr)
                if choice =="3":
                    print"in 3"
                    reports(conn,addr,uname)
                if choice=="4":
                    conn.send(str(userdata[1]))
                    print userdata[1]
                    if str(userdata[1])== "True":
                        choice_4=conn.recv(1024)
                        if choice_4== "1":
                            print "in 4.1"
                            delete_song(conn, addr)
                            print "out"
                        if choice_4== "2":
                            remove_user(conn,addr)
                if choice == "5":
                    conn.send(str(userdata[1]))
                    print userdata[1]
                    if str(userdata[1])== "True":
                        make_admin(conn, addr)
                if choice == "6":
                    conn.send(str(userdata[1]))
                    print userdata[1]
                    if str(userdata[1])== "True":
                        print "in 6"
                        send_report_log(conn, addr)
                    
                if choice =="7":
                    conn.send(str(userdata[1]))
                    print userdata[1]
                    if str(userdata[1])== "True":
                        print "in 7"
                        send_pending(conn, addr)     
                choice=conn.recv(1024)  
        #print "Server log: Thread {} completed to serve request from: {}:{}".format(name,addr[0],str(addr[1]))
        q.task_done()

for i in xrange(CONCURRENT):
        t=Thread(target=doWork)
        t.daemon=True
        t.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', port))
server_socket.listen(1)
while True:
    conn, addr = server_socket.accept()
    print "Server log: New connection: {}:{}\n".format(addr[0],str(addr[1]))
    #Put info in queue and return to serve another client
    q.put((conn, addr))
##client_name = client_socket.recv(1024)
##client_socket.send('Hello ' + client_name)
##client_socket.close()
##server_socket.close()
