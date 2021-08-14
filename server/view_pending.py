import os
import socket
"""
This program gets the connection between the server and the user.
The program can delete the pending song\ stream it or approved this song and move it to the server's database
"""
def send_pending(conn, addr):
    file=open("pending_song_list.txt","r+")
    data1=file.read()
    file.close()
    print data1
    if len(data1)==0:
        conn.send("-1")
    else:
        conn.send(data1)
        song_choice=conn.recv(1024)
        if song_choice!="-1":   
            decision = conn.recv(1024)
            if(decision!="-1"): # if the user doesn't quit the program
                print song_choice
                m=data1.split("&&&&")
                if(decision=="1"):  # delete the pending  song               
                    data=""
                    print len(m)
                    os.remove(m[int(song_choice)])
                    m.remove(m[int(song_choice)])
                    i=0
                    while i<(len(m)):
                        data=data+str(m[i])+ "&&&&"
                        print data
                        i=i+1
                    data=data[:-4]
                    song_list=open('pending_song_list.txt', 'wb')
                    song_list.write(data)
                    song_list.close()
                if(decision =="2"):# stream the song to the user
                    file=open('port.txt','r+')
                    socketnum=file.read()
                    file.close()
                    socketnum=int(socketnum)
                    if socketnum==9999:
                        newsocketnum=1030
                    else:
                        newsocketnum=socketnum+1
                    file=open('port.txt','wb')
                    file.write(str(newsocketnum))
                    file.close()
                    conn.send(str(socketnum))
                    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    sock.bind(("0.0.0.0",socketnum))
                    (data,remote_address)=sock.recvfrom(1024)
                    print data
                    s=open(m[int(song_choice)],"rb")
                    d=s.read()
                    s.close()
                    i=0
                    m=d
                    songpart=""
                    ch=""
                    print len(d)
                    sock.sendto(str(len(d)),(remote_address))
                    (data,remote_address)=sock.recvfrom(1024)
                    print data
                    while len(m)>4096:
                        songpart=m[0:4096]
                        m=m[4096:len(m)]
                        sock.sendto(songpart,(remote_address))
                        (data,remote_address)=sock.recvfrom(1024)
                    sock.sendto(m,(remote_address))
                    print"l"
                    sock.close()
                if decision =="3": # approved this song.
                    song_name=m[int(song_choice)]
                    m.remove(m[int(song_choice)])
                    i=0
                    data =""
                    while i<(len(m)):
                        data=data+str(m[i])+ "&&&&"
                        print data
                        i=i+1
                    if len(m)>0:
                        data=data[:-4]
                    song_list=open('pending_song_list.txt', 'wb')
                    song_list.write(data)
                    song_list.close()
                    file=open("song_list.txt","r+")
                    data1=file.read()
                    file.close()
                    data1=data1+"&&&&"+ song_name
                    file=open("song_list.txt","wb")
                    file.write(data1)
                    print data1
                    file.close()
                        
               
            
