from Tkinter import *
from tkFileDialog   import askopenfilename      

master =Tk()
p=""
import os
import socket
admin="127.0.0.1"
port= 1262
adminpermition="False"
remove=[]
for q in xrange(0,30,1):
    remove.append(False)
print remove

cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cSocket.connect((admin,port))
"""
returns you to the admin main screen
"""
def return_to_admin_main():
    global cSocket
    global current_master
    current_master.destroy()
    cSocket.send("-1")
    admin_main2()
'''
returns you to the regular user main screen
'''
def return_to_main():
    global cSocket
    global current_master
    current_master.destroy()
    cSocket.send("-1")
    main()
'''
exit the system
'''
def quit_button():
    global cSocket
    global current_master
    cSocket.send("-1")
    cSocket.send("-1")
    cSocket.close()
    current_master.destroy()
'''
The main administer screen
'''
def admin_main2():
    '''
    view the pending reports submitted by users
    '''
    def view_reports():
        '''
        no reports found
        '''
        def error():
            def return_admin():
                master_pending.destroy()
                admin_main2()
            master_pending=Tk()
            
            master_mainB2=Button(master_pending, text="there are no reports left", command=return_admin)
            master_mainB2.pack()
        global cSocket
        admin_main.destroy()
        cSocket.send("6")
        reportlist=cSocket.recv(4096)
        reportlist=cSocket.recv(4096)
        if reportlist=="-1":
            error()
        else:
            m=reportlist.split("&&&&")
            master_pending=Tk()
            def remove_b():
                global remove
                for i in xrange (0, len(remove), 1):
                    remove[i]=False
                master_b=Tk()
                '''
                moving all the check boxes to the unchecked possision
                '''
                def remove_button(i):
                    global remove
                    if remove[i]:
                        remove[i]=False
                    else:
                        remove[i]=True
                '''
                remove report
                '''
                def remove_report():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            break
                    if remove[i]==True:
                        cSocket.send(str(m[i]))
                        cSocket.send("1")
                        master_b.destroy()
                        admin_main2()
                '''
                view the submitted report
                '''
                def read_report():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            break
                    if remove[i]==True:
                        '''
                        delete the report file from your hard drive
                        '''
                        def done_reading():
                            os.remove("report.txt")
                            close_report.destroy()
                        close_report=Tk()
                        print m[i]
                        cSocket.send(str(m[i]))
                        cSocket.send("2")
                        data=cSocket.recv(1024)
                        print "check"
                        print data
                        file=open("report.txt","wb")
                        file.write(data)
                        file.close()
                        os.startfile("report.txt")
                        master_b.destroy()
                        master_mainB2=Button(close_report, text='done reading', command=done_reading)
                        master_mainB2.pack()
                        admin_main2()
                            
                i=0
                while (i<len(m) and i<30):
                    button = i
                    button = Checkbutton(master_b, text = m[i],  command = lambda name=i:remove_button(name))
                    button.pack()
                    i=i+1
                master_b.title("reports")
                master_b.geometry("400x400")
                master_pending.destroy()
                master_mainB2=Button(master_b, text='remove report', command=remove_report)
                master_mainB2.pack()
                master_mainB3=Button(master_b, text='read this report', command=read_report)
                master_mainB3.pack()
                global current_master
                current_master=master_b
                master_mainb1=Button(master_b, text='return to main ',fg="orange" ,command=return_to_admin_main)
                master_mainb1.pack()
                
            master_mainB1=Button(master_pending, text='view reports', command=remove_b)
            master_mainB1.pack()
            
    '''
    view submitted songs before adding them to the database
    '''
    def view_pending():
        def error():
            def return_admin():
                master_pending.destroy()
                admin_main2()
            master_pending=Tk()
            master_mainB2=Button(master_pending, text="there are no pendings left", command=return_admin)
            master_mainB2.pack()
        global cSocket
        admin_main.destroy()
        cSocket.send("7")
        m=cSocket.recv(4096)
        m=cSocket.recv(4096)
        if m=="-1":
            error()
        else:
            m=m.split("&&&&")
            m.remove(m[-1])
            master_pending=Tk()
            def remove_b():
                global remove
                for i in xrange (0, len(remove), 1):
                    remove[i]=False
                master_b=Tk()
                def remove_button(i):
                    global remove
                    if remove[i]:
                        remove[i]=False
                    else:
                        remove[i]=True
                '''
                remove a selected pending song
                '''
                def remove_songs():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            break
                    if remove[i]==True:
                        cSocket.send(str(i))
                        cSocket.send("1")
                        master_b.destroy()
                        admin_main2()
                '''
                listen to the sellected pending song
                '''
                def listen_to_pending_song():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            break
                    if remove[i]==True:
                        print m[i]
                        cSocket.send(str(i))
                        cSocket.send("2")
                        socketNum=cSocket.recv(1024)
                        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto("hii",(admin,int(socketNum)))
                        (sonlen,remote_address)=sock.recvfrom(1024)
                        print "sonlen= "+sonlen
                        length=int(sonlen)
                        i=0
                        data3=""
                        length=length/4096
                        print length
                        #transfering fragmented the song 
                        while(i<length):
                            sock.sendto("rf",remote_address)
                            (song,remote_address)=sock.recvfrom(4096)
                            data3=data3+song
                            i=i+1
                        sock.sendto("rf",remote_address)
                        print "done"
                        file=open("song.mp3","wb")
                        file.write(data3)
                        file.close()
                        os.startfile("song.mp3")
                        os.remove("song.mp3")
                        print "ttt"
                        sock.close
                        master_b.destroy()
                        admin_main2()
                '''
                perminantly add song to the databse
                '''
                def add_song():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            break
                    if remove[i]==True:
                        print m[i]
                        cSocket.send(str(i))
                        cSocket.send("3")
                        master_b.destroy()
                        admin_main2()
                i=0         
                while (i<len(m) and i<30):
                    button = i
                    button = Checkbutton(master_b, text = m[i],  command = lambda name=i:remove_button(name))
                    button.pack()
                    i=i+1
                master_pending.destroy()
                master_b.title("pending songs")
                master_b.geometry("400x400")
                master_mainB2=Button(master_b, text='remove song', command=remove_songs)
                master_mainB2.pack()
                master_mainB3=Button(master_b, text='listen to this song', command=listen_to_pending_song)
                master_mainB3.pack()
                master_mainB3=Button(master_b, text='add this song to the database', command=add_song)
                master_mainB3.pack()
                global current_master
                current_master=master_b
                master_mainb1=Button(master_b, text='return to main ',fg="orange", command=return_to_admin_main)
                master_mainb1.pack()
            
            master_mainB1=Button(master_pending, text='view songs', command=remove_b)
            master_mainB1.pack()
    '''
    uploading a song to the server
    '''
    def client_upload1():
        admin_main.destroy()
        master_clupload=Tk()
        global cSocket
        cSocket.send("2")
        '''
        selecting a song from your hard drive and uploading it
        '''
        def callback1():
            path= askopenfilename()
            song_name=path.split("/")
            cSocket.send(song_name[-1])
            print song_name[-1]
            acception = cSocket.recv(1024)
            cSocket.send("H")
            print acception
            if acception == "True":
                socketnum=cSocket.recv(1024)
                file=open(path,"rb")
                song=file.read()
                file.close()
                len_song=len(song)
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock.sendto(str(len_song),(admin,int(socketnum)))
                (data,remote_address)=sock.recvfrom(1024)
                songpart=""
                while len_song>4096:
                    songpart=song[0:4096]
                    song=song[4096:len(song)]
                    len_song=len(song)
                    sock.sendto(songpart,(remote_address))
                    (data,remote_addrwess)=sock.recvfrom(1024)
                sock.sendto(song,remote_address)
                print "work"
                sock.close()
                print "work"
            master_clupload.destroy()
            admin_main2()
        errmsg = 'Error!'
        Button(master_clupload,text='File Open', command=callback1).pack(fill=X)
        global current_master
        current_master= master_clupload
        Quit=Button(master_clupload, fg="red", text='return to main ', command=return_to_admin_main)
        Quit.pack()
        global cSocket
    '''
    stream a song
    '''
    def admin_song_request():
        global j
        j=0
        global cSocket
        cSocket.send("1")
        '''
        search for a specific song
        '''    
        def search_songs():
            master_choice.destroy()
            global cSocket
            '''
            sending your search to the server
            '''
            def send_search():
                def error2():
                    admin_main2()
                    master_error.destroy()
                global cSocket
                sname=master4_e3.get()
                sname=sname+".mp3"
                master_send.destroy()
                for i in xrange(0,len(m),1):
                    if m[i]==sname:
                        print m[i]
                        cSocket.send(str(i))
                        socketNum=cSocket.recv(1024)
                        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto("hii",(admin,int(socketNum)))
                        (sonlen,remote_address)=sock.recvfrom(1024)
                        print "sonlen= "+sonlen
                        length=int(sonlen)
                        i=0
                        data3=""
                        length=length/4096
                        print length
                        while(i<length):
                            sock.sendto("rf",remote_address)
                            (song,remote_address)=sock.recvfrom(4096)
                            data3=data3+song
                            i=i+1
                        sock.sendto("rf",remote_address)
                        print "done"
                        file=open("song.mp3","wb")
                        file.write(data3)
                        file.close()
                        os.startfile("song.mp3")
                        os.remove("song.mp3")
                        print "ttt"
                        sock.close
                        admin_main2()
                        master_send.destroy()
                #in case the song was not found:
                cSocket.send("-1")
                master_error=Tk()
                b2=Button(master_error, text='no song with such name', command=error2)
                b2.pack()
            master_send=Tk()
            master4_e3 = Entry(master_send)
            master4_e3.grid(row=2, column=2, sticky=W, pady=4)
            master4_e3.pack()
            var = StringVar()
            var.set("enter song name")
            label = Label( master_send, textvariable=var )
            label.pack()
            label.place(x = 0, y = 100)
            print "wait"
            songlist=cSocket.recv(4096)
            m=songlist.split("&&&&")
            admin_main.destroy()
            master_send.title("song search")
            master_send.geometry("400x400")
            b2=Button(master_send, text='search for a song ', command=send_search)
            b2.pack()
            global current_master
            current_master=master_send
            master_mainb1=Button(master_send, text='return to main ',fg="orange",command=return_to_admin_main)
            master_mainb1.pack()

        '''
        select a song from the song list
        '''
        def button_choice():
            def more_button_choice():
                global counter
                global current_master
                current_master.destroy()
                counter=counter+1
                print counter
                global remove
                for i in xrange (0, len(remove), 1):
                    remove[i]=False
                master_b2=Tk()
                def remove_button(i):
                    print i
                    global remove
                    if remove[i]:
                        remove[i]=False
                    else:
                        remove[i]=True
                    print remove
                '''
                send selected song number and stream said song
                '''
                def print1():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            print m[i]
                            cSocket.send(str(i))
                            socketNum=cSocket.recv(1024)
                            sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                            sock.sendto("hii",(admin,int(socketNum)))
                            (sonlen,remote_address)=sock.recvfrom(1024)
                            print "sonlen= "+sonlen
                            length=int(sonlen)
                            i=0
                            data3=""
                            length=length/4096
                            print length
                            while(i<length):
                                sock.sendto("rf",remote_address)
                                (song,remote_address)=sock.recvfrom(4096)
                                data3=data3+song
                                i=i+1
                            sock.sendto("rf",remote_address)
                            print "done"
                            file=open("song.mp3","wb")
                            file.write(data3)
                            file.close()
                            os.startfile("song.mp3")
                            os.remove("song.mp3")
                            print "ttt"
                            sock.close
                            master_b2.destroy()
                            admin_main2()
                global j
                counter =counter+4
                while j<counter:
                    print counter
                    if counter>len(m):
                        counter=len(m)
                    button = j
                    button = Checkbutton(master_b2, text = m[j],  command = lambda name=j:remove_button(name))
                    button.pack()
                    j=j+1
                global current_master
                current_master=master_b2
                master_b2.title("view songs")
                master_b2.geometry("400x400")
                master_mainB2=Button(master_b2, text='done', command=print1)
                master_mainB2.pack()
                master_mainb1=Button(master_b2, text='return to main ',fg="orange",command=return_to_admin_main)
                master_mainb1.pack()
                if counter<len(m):
                    master_mainb3=Button(master_b2, text='view more songs ',fg="orange",command=more_button_choice)
                    master_mainb3.pack()

            global counter
            counter=counter+1
            master_choice.destroy()
            print "destroy"
            print "wait"
            songlist=cSocket.recv(4096)
            print "wait"
            print songlist
            m=songlist.split("&&&&")
            global remove
            for i in xrange (0, len(remove), 1):
                remove[i]=False
            master_b=Tk()
            admin_main.destroy()
            def remove_button(i):
                print i
                global remove
                if remove[i]:
                    remove[i]=False
                else:
                    remove[i]=True
                print remove
            '''
            send selected song number and stream said song
            '''
            def print1():
                for i in xrange(0,len(m),1):
                    if remove[i]==True:
                        print m[i]
                        cSocket.send(str(i))
                        socketNum=cSocket.recv(1024)
                        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto("hii",(admin,int(socketNum)))
                        (sonlen,remote_address)=sock.recvfrom(1024)
                        print "sonlen= "+sonlen
                        length=int(sonlen)
                        i=0
                        data3=""
                        length=length/4096
                        print length
                        while(i<length):
                            sock.sendto("rf",remote_address)
                            (song,remote_address)=sock.recvfrom(4096)
                            data3=data3+song
                            i=i+1
                        sock.sendto("rf",remote_address)
                        print "done"
                        file=open("song.mp3","wb")
                        file.write(data3)
                        file.close()
                        os.startfile("song.mp3")
                        os.remove("song.mp3")
                        print "ttt"
                        sock.close
                        master_b.destroy()
                        admin_main2()
            global j
            counter =counter+4
            while j<counter:
                if counter> len(m):
                    counter=len(m)
                print counter
                button = j
                button = Checkbutton(master_b, text = m[j],  command = lambda name=j:remove_button(name))
                button.pack()
                j=j+1
            global current_master
            current_master=master_b
            master_b.title("view songs")
            master_b.geometry("400x400")
            master_mainB2=Button(master_b, text='done', command=print1)
            master_mainB2.pack()
            master_mainb1=Button(master_b, text='return to main ',fg="orange",command=return_to_admin_main)
            master_mainb1.pack()
            if counter<len(m):
                master_mainb3=Button(master_b, text='view more songs ',fg="orange",command=more_button_choice)
                master_mainb3.pack()
        master_choice=Tk()
        master_choice.title("song selection")
        b1=Button(master_choice, text='view songs ', command=button_choice)
        b1.pack()
        b2=Button(master_choice, text='search for a song ', command=search_songs)
        b2.pack()
        global counter
        counter =0
        
    '''
    changing a regular user into an administrater
    '''
    def add_admin():
        admin_main.destroy()
        cSocket.send("5")
        true=cSocket.recv(4096)
        m=cSocket.recv(4096)
        m=m.split("&&&&")
        global remove
        for i in xrange (0, len(remove), 1):
            remove[i]=False
        master_b1=Tk()
        master_b1.title("make a user an admin")
        master_b1.geometry("400x400")
        def remove_button(i):
            print i
            global remove
            if remove[i]:
                remove[i]=False
            else:
                remove[i]=True
            print remove
        '''
        sending selected user number to be changed into an admin
        '''
        def print1():
            if check=="True":
                for i in xrange(0,len(m),1):
                    if remove[i]==True:
                        break
                if remove[i]==True:
                    print m[i]
                    cSocket.send(str(i))
                    master_b1.destroy()
                    admin_main2()
            else:
                master_b1.destroy()
                admin_main2()
        check="False"
        i=0
        while (i<len(m) and i<30):
            if m[i+2]=="n":
                check="True"
                button = i
                button = Checkbutton(master_b1, text = m[i],  command = lambda name=i:remove_button(name))
                button.pack()
            i=i+3
        if check=="True":
            master_mainB2=Button(master_b1, text='done', command=print1)
            master_mainB2.pack()
            global current_master
            current_master= master_b1

            Quit=Button(master_b1, text='return to main ', fg="orange",command=return_to_admin_main)
            Quit.pack()
        else:
            master_mainB2=Button(master_b1, text='all of the users are admins', command=print1)
            cSocket.send("-1")
            master_mainB2.pack()
    '''
    selcet a user to be removed
    '''
    def remove_user():
        admin_main.destroy()
        cSocket.send("4") 
        cSocket.send("2")
        true=cSocket.recv(4096)
        m=cSocket.recv(4096)
        m=m.split("&&&&")
        master_remove=Tk()
        def remove_b():
            global remove
            for i in xrange (0, len(remove), 1):
                remove[i]=False
            master_b=Tk()
            def remove_button(i):
                print i
                global remove
                if remove[i]:
                    remove[i]=False
                else:
                    remove[i]=True
                print remove
            '''
            sending selected user number to be deleted
            '''
            def print1():
                for i in xrange(0,len(m),1):
                    if remove[i]==True:
                        break
                        print m[i]
                if remove[i]==True:
                    cSocket.send(str(i))
                    master_b.destroy()
                    admin_main2()
            i=0
            while (i<len(m) and i<30):
                button = i
                button = Checkbutton(master_b, text = m[i],  command = lambda name=i:remove_button(name))
                button.pack()
                i=i+3
            master_b.title("remove users")
            master_b.geometry("400x400")
            master_mainB2=Button(master_b, text='done', command=print1)
            master_mainB2.pack()
            global current_master
            current_master=master_b
            master_mainb1=Button(master_b, text='return to main ',fg="orange", command=return_to_admin_main)
            master_mainb1.pack()
            master_remove.destroy()
        master_mainB1=Button(master_remove, text='remove user', command=remove_b)
        master_mainB1.pack()
    '''
    select a song from the song list to be removed
    '''
    def remove_song():
        admin_main.destroy()
        cSocket.send("4") 
        cSocket.send("1")
        true=cSocket.recv(4096)
        m=cSocket.recv(4096)
        m=m.split("&&&&")
        master_remove=Tk()
        def remove_b():
            global remove
            for i in xrange (0, len(remove), 1):
                remove[i]=False
            master_b=Tk()
            def remove_button(i):
                print i
                global remove
                if remove[i]:
                    remove[i]=False
                else:
                    remove[i]=True  
                print remove
            '''
            sending selected song number to be deleted from the database
            '''
            def print1():
                for i in xrange(0,len(m),1):
                    if remove[i]==True:
                        break
                if remove[i]==True:
                    print m[i]
                    cSocket.send(str(i))
                    master_b.destroy()
                    admin_main2()
            i=0
            while (i<len(m) and i<30):
                button = i
                button = Checkbutton(master_b, text = m[i],  command = lambda name=i:remove_button(name))
                button.pack()
                i=i+1
            master_b.title("remove songs")
            master_b.geometry("400x400")
            master_remove.destroy()
            master_mainB2=Button(master_b, text='done', command=print1)
            master_mainB2.pack()
            global current_master
            current_master=master_b
            master_mainb1=Button(master_b, text='return to main ',fg="orange",command=return_to_admin_main)
            master_mainb1.pack()
            
        master_mainB1=Button(master_remove, text='remove song', command=remove_b)
        master_mainB1.pack()

    admin_main=Tk()
    admin_main.title("admin Main")
    admin_main.geometry("400x400")
    master_mainB1=Button(admin_main, text='stream a song', command=admin_song_request)
    master_mainB1.pack()
    master_mainB2=Button(admin_main, text='upload a song', command=client_upload1)
    master_mainB2.pack()
    master_mainB3=Button(admin_main, text='remove user', command=remove_user)
    master_mainB3.pack()
    master_mainB3=Button(admin_main, text='remove song', command=remove_song)
    master_mainB3.pack()
    master_mainB3=Button(admin_main, text='make user an admin', command=add_admin)
    master_mainB3.pack()
    master_mainB3=Button(admin_main, text='view pending songs', command=view_pending)
    master_mainB3.pack()
    master_mainB3=Button(admin_main, text='view reports', command=view_reports)
    master_mainB3.pack()
    global current_master
    current_master= admin_main
    Quit=Button(admin_main, fg="red", text='Quit', command=quit_button)
    Quit.pack()
'''
regular user's home page
'''
def main():
    '''
    send a report to be viewed by the admins
    '''
    def report():
        global cSocket
        cSocket.send("3")
        '''
        send your report
        '''
        def send_report():
            global cSocket
            data  = master1e1.get("1.0",'end-1c')
            print data
            cSocket.send(data)
            print "sent"
            master_report.destroy()
            main()
        master_main.destroy()
        master_report=Tk()
        master_report.title("report")
        master_report.geometry("450x400")
        var = StringVar()
        var.set("enter a report of up to 1000 charecters")
        label = Label( master_report, textvariable=var )
        label.pack()
        label.place(x = 0, y = 1) 
        master1e1 = Text(master_report, height=20, width=40)
        master1e1.pack()
        master1e1.place(x = 0, y =30 )
        master_reportB3=Button(master_report, text='send the report', command=send_report)
        master_reportB3.pack()
        master_reportB3.place(x = 0, y =350 )
        global current_master
        current_master=master_report
        master_mainb1=Button(master_report, text='return to main ', fg="orange",command=return_to_main)
        master_mainb1.pack()
        master_mainb1.place(x = 150, y =350 )
    '''
    upload a song to the server
    '''
    def client_upload():
        master_main.destroy()
        master_clupload=Tk()
        global cSocket
        cSocket.send("2")
        '''
        transfer the selected song from your hard drive
        '''
        def callback1():
            path= askopenfilename()
            song_name=path.split("/")
            cSocket.send(song_name[-1])
            print song_name[-1]
            acception = cSocket.recv(1024)
            cSocket.send("H")
            if acception == "True":
                socketnum=cSocket.recv(1024)
                file=open(path,"rb")
                song=file.read()
                file.close()
                len_song=len(song)
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                sock.sendto(str(len_song),(admin,int(socketnum)))
                (data,remote_address)=sock.recvfrom(1024)
                songpart=""
                while len_song>4096:
                    songpart=song[0:4096]
                    song=song[4096:len(song)]
                    len_song=len(song)
                    sock.sendto(songpart,(remote_address))
                    (data,remote_address)=sock.recvfrom(1024)
                sock.sendto(song,remote_address)
                print "work"
                sock.close()
                print "work"
            master_clupload.destroy()
            main()
        errmsg = 'Error!'
        Button(master_clupload,text='File Open', command=callback1).pack(fill=X)
        global current_master
        current_master=master_clupload
        master_mainb1=Button(master_clupload, text='return to main ', fg="orange",command=return_to_main)
        master_mainb1.pack()
    '''
    stream a song from the server
    '''
    def client_song_request():
        global j
        j=0
        global cSocket
        cSocket.send("1")
        '''
        search for a specific song
        '''    
        def search_songs():
            master_choice.destroy()
            global cSocket
            '''
            sending your search to the server
            '''
            def send_search():
                def error2():
                    main()
                    master_error.destroy()
                global cSocket
                sname=master4_e3.get()
                sname=sname+".mp3"
                master_send.destroy()
                for i in xrange(0,len(m),1):
                    if m[i]==sname:
                        print m[i]
                        cSocket.send(str(i))
                        socketNum=cSocket.recv(1024)
                        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto("hii",(admin,int(socketNum)))
                        (sonlen,remote_address)=sock.recvfrom(1024)
                        print "sonlen= "+sonlen
                        length=int(sonlen)
                        i=0
                        data3=""
                        length=length/4096
                        print length
                        while(i<length):
                            sock.sendto("rf",remote_address)
                            (song,remote_address)=sock.recvfrom(4096)
                            data3=data3+song
                            i=i+1
                        sock.sendto("rf",remote_address)
                        print "done"
                        file=open("song.mp3","wb")
                        file.write(data3)
                        file.close()
                        os.startfile("song.mp3")
                        os.remove("song.mp3")
                        print "ttt"
                        sock.close
                        main()
                        master_send.destroy()
                #in case the song was not found:
                cSocket.send("-1")
                master_error=Tk()
                b2=Button(master_error, text='no song with such name', command=error2)
                b2.pack()
            master_send=Tk()
            master4_e3 = Entry(master_send)
            master4_e3.grid(row=2, column=2, sticky=W, pady=4)
            master4_e3.pack()
            var = StringVar()
            var.set("enter song name")
            label = Label( master_send, textvariable=var )
            label.pack()
            label.place(x = 0, y = 100)
            print "wait"
            songlist=cSocket.recv(4096)
            m=songlist.split("&&&&")
            master_main.destroy()
            master_send.title("search for a song")
            master_send.geometry("400x400")
            b2=Button(master_send, text='search for a song ', command=send_search)
            b2.pack()
            global current_master
            current_master=master_send
            b3=Button(master_send, text='return to main ',fg="orang", command=return_to_main )
        '''
        select a song from the song list
        '''
        def button_choice():
            def more_button_choice():
                global counter
                global current_master
                current_master.destroy()
                counter=counter+1
                print counter
                global remove
                for i in xrange (0, len(remove), 1):
                    remove[i]=False
                master_b2=Tk()
                def remove_button(i):
                    print i
                    global remove
                    if remove[i]:
                        remove[i]=False
                    else:
                        remove[i]=True
                    print remove
                '''
                send selected song number and stream said song
                '''
                def print1():
                    for i in xrange(0,len(m),1):
                        if remove[i]==True:
                            print m[i]
                            cSocket.send(str(i))
                            socketNum=cSocket.recv(1024)
                            sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                            sock.sendto("hii",(admin,int(socketNum)))
                            (sonlen,remote_address)=sock.recvfrom(1024)
                            print "sonlen= "+sonlen
                            length=int(sonlen)
                            i=0
                            data3=""
                            length=length/4096
                            print length
                            while(i<length):
                                sock.sendto("rf",remote_address)
                                (song,remote_address)=sock.recvfrom(4096)
                                data3=data3+song
                                i=i+1
                            sock.sendto("rf",remote_address)
                            print "done"
                            file=open("song.mp3","wb")
                            file.write(data3)
                            file.close()
                            os.startfile("song.mp3")
                            os.remove("song.mp3")
                            print "ttt"
                            sock.close
                            master_b2.destroy()
                            main()
                global j
                counter =counter+4
                while j<counter:
                    print counter
                    if counter>len(m):
                        counter=len(m)
                    button = j
                    button = Checkbutton(master_b2, text = m[j],  command = lambda name=j:remove_button(name))
                    button.pack()
                    j=j+1
                global current_master
                current_master=master_b2
                master_b2.title("select a song")
                master_b2.geometry("400x400")

                master_mainB2=Button(master_b2, text='done', command=print1)
                master_mainB2.pack()
                master_mainb1=Button(master_b2, text='return to main ',fg="orange",command=return_to_main)
                master_mainb1.pack()
                if counter<len(m):
                    master_mainb3=Button(master_b2, text='view more songs ',fg="orange",command=more_button_choice)
                    master_mainb3.pack()

            global counter
            counter=counter+1
            master_choice.destroy()
            print "destroy"
            print "wait"
            songlist=cSocket.recv(4096)
            print "wait"
            print songlist
            m=songlist.split("&&&&")
            global remove
            for i in xrange (0, len(remove), 1):
                remove[i]=False
            master_b=Tk()
            master_main.destroy()
            def remove_button(i):
                print i
                global remove
                if remove[i]:
                    remove[i]=False
                else:
                    remove[i]=True
                print remove
            '''
            send selected song number and stream said song
            '''
            def print1():
                for i in xrange(0,len(m),1):
                    if remove[i]==True:
                        print m[i]
                        cSocket.send(str(i))
                        socketNum=cSocket.recv(1024)
                        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto("hii",(admin,int(socketNum)))
                        (sonlen,remote_address)=sock.recvfrom(1024)
                        print "sonlen= "+sonlen
                        length=int(sonlen)
                        i=0
                        data3=""
                        length=length/4096
                        print length
                        while(i<length):
                            sock.sendto("rf",remote_address)
                            (song,remote_address)=sock.recvfrom(4096)
                            data3=data3+song
                            i=i+1
                        sock.sendto("rf",remote_address)
                        print "done"
                        file=open("song.mp3","wb")
                        file.write(data3)
                        file.close()
                        os.startfile("song.mp3")
                        os.remove("song.mp3")
                        print "ttt"
                        sock.close
                        master_b.destroy()
                        main()
            global j
            counter =counter+4
            while j<counter:
                if counter> len(m):
                    counter=len(m)
                print counter
                button = j
                button = Checkbutton(master_b, text = m[j],  command = lambda name=j:remove_button(name))
                button.pack()
                j=j+1
            global current_master
            master_b.title("select a song")
            master_b.geometry("400x400")
            current_master=master_b
            master_mainB2=Button(master_b, text='done', command=print1)
            master_mainB2.pack()
            master_mainb1=Button(master_b, text='return to main ',fg="orange",command=return_to_main)
            master_mainb1.pack()
            if counter<len(m):
                master_mainb3=Button(master_b, text='view more songs ',fg="orange",command=more_button_choice)
                master_mainb3.pack()
        master_choice=Tk()
        master_choice.title("selecting a song")
        master_choice.geometry("400x400")
        b1=Button(master_choice, text='view songs ', command=button_choice)
        b1.pack()
        b2=Button(master_choice, text='search for a song ', command=search_songs)
        b2.pack()
        global counter
        counter =0
        
    master_main=Tk()
    master_main.title(" Main")
    master_main.geometry("400x400")

    master_mainB1=Button(master_main, text='stream a song', command=client_song_request)
    master_mainB1.pack()
    master_mainB2=Button(master_main, text='upload a song', command=client_upload)
    master_mainB2.pack()
    master_mainB3=Button(master_main, text='send a report', command=report)
    master_mainB3.pack()
    global current_master
    current_master= master_main
    Quit=Button(master_main, fg="red", text='Quit', command=quit_button)
    Quit.pack()
'''
log in to the system
'''
def login():
    master.destroy()
    global cSocket
    cSocket.send("1")
    '''
    authenticating username and password with the server
    '''
    def check():
        global p
        global adminpermision     
        uname=master1e1.get()
        upassword=master1e2.get()
        if len(uname)>0 and len(upassword)>0:
            cSocket.send(uname)
            upassword=upassword.encode("base64")
            cSocket.send(upassword)
            acceptionlog=cSocket.recv(1024)
            cSocket.send(uname)
            adminpermition1=cSocket.recv(1024)
            if acceptionlog=="True":
                adminpermition=adminpermition1
                print acceptionlog
                print"adminpermition:"+ adminpermition
                master1.destroy()
                if adminpermition1=="True":
                    admin_main2()
                if adminpermition1=="False":
                    main()
            else:
                var = StringVar()
                var.set("wrong password or username!!!")
                label = Label( master1, text="wrong password or username!!!" )
                label.pack()
                label.place(x = 100, y = 130)
                
    master1=Tk()
    master1.title(" log in")
    master1.geometry("400x200")
    var1 = StringVar()

    var1.set("username: ")
    label = Label( master1, textvariable=var1 )
    label.pack()
    label.place(x = 0, y = 1)
    var = StringVar()
    var.set("password: ")
    label = Label( master1, textvariable=var )
    label.pack()
    label.place(x = 0, y = 20)
    master1e1 = Entry(master1)
    master1e1.pack()
    master1e2 = Entry(master1,show="*")
    master1e2.pack()
    global current_master
    current_master= master1
    B1=Button(master1,fg="brown", text='login', command=check)
    B1.pack()
    Quit=Button(master1, fg="red", text='Quit', command=quit_button)
    Quit.pack() 
'''
creating a new user
'''
def register():
    master.destroy()
    global cSocket
    cSocket.send("2")
    def create_user1():
        '''
        authenticating password
        '''
        def authenticate_password():
            if master4_e2.get() == master4_e3.get():
                if len(master4_e2.get())>6: 
                    upassword=master4_e2.get()
                    upassword=upassword.encode("base64")
                    cSocket.send(upassword)
                    acception_creat_new_user=cSocket.recv(1024)
                    adminpermition="False"
                    master4.destroy()
                    main()
                else:
                    txt="your password is shorter than 7 letters"
                    label = Label( master4, text=txt )
                    label.place(x=20,y=20)
                    label.pack()
                    
            else:
                txt="your passwords do not match"
                label = Label( master4, text=txt)
                label.place(x=20,y=20)
                label.pack()
                
        print "in create user"
        master4=Tk()
        print "in create user2"
        master4.title(" register")
        master4.geometry("900x500")
        master2.destroy()
        global current_master
        current_master= master4
        print "in create user2"
        label = Label( master4, text="enter your password" )
        label.pack()
        master4_e2 = Entry(master4,show="*")
        master4_e2.grid(row=1, column=1, sticky=W, pady=4)
        master4_e2.pack()
        label = Label( master4, text="renter your password" )
        label.pack()
        master4_e3 = Entry(master4,show="*")
        master4_e3.grid(row=2, column=1, sticky=W, pady=4)
        master4_e3.pack()
        master4_b1=Button(master4, text='create user', command=authenticate_password)
        master4_b1.grid(row=3, column=4, sticky=W, pady=4)
        master4_b1.pack()
        Quit=Button(master4, fg="red", text='Quit', command=quit_button)
        Quit.pack()  
        print "in create user2"
    '''
    making sure username is not already taken
    '''
    def check_uname():
        uname=e1.get()
        if (len(uname)>6):
            cSocket.send(uname)
            cSocket.send("lol".encode("base64"))
            acception_new_user=cSocket.recv(1024)
            print acception_new_user
            if  acception_new_user == "False" or acception_new_user == "FalseFalse":
                label = Label( master2, text="this user is already exist" )
                label.pack()
            else:
                create_user1()
        else:
                label = Label( master2, text="your user_name is shorter than 7 letters" )
                label.pack()
    global current_master
    master2=Tk()
    master2.title(" register")
    master2.geometry("800x400")
    
    e1 = Entry(master2)
    e1.grid(row=1, column=1, sticky=W, pady=4)
    e1.pack()
    check_name=Button(master2, text='check username', command=check_uname)
    check_name.pack()
    Quit=Button(master2, fg="red", text='Quit', command=quit_button)
    Quit.pack()
    current_master = master2
current_master = master
log=Button(master, text='login', command=login)
log.pack()
reg=Button(master, text='register', command=register)
reg.pack()
Quit=Button(master, fg="red", text='Quit', command=quit_button)
Quit.pack()
master.title(" hi, welcome to InterMusic")
master.geometry("450x150")


master.mainloop()
