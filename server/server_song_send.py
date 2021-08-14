import socket
import re
import os
import sys

"""
This program gets the connection between the user and the server.
The program streaming a song form the server data-base to the user.
"""
def song_request(conn, addr):
    newsocketnum=0
    song_list=open('song_list.txt', 'r+')
    print song_list
    m=song_list.read()
    song_list.close()
    print m
    conn.send(m)
    print m
    song_choice=conn.recv(1024)
    print song_choice
    if song_choice !="-1":
        m=m.split("&&&&")
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
        print socketnum
        print newsocketnum
        conn.send(str(socketnum))
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)# open UDP connection to make the streaming go faster. 
        sock.bind(("0.0.0.0",int(socketnum)))
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
        print "server log: Closing connection for: {}:{}\n".format(addr[0],str(addr[1]))
