import socket
import re
import os
import sys
"""
This program gets the connection between the user and the server.
The program gets the song that the user upload, and save it in server's database.
"""
def client_song_upload(conn,addr):
    t="True"
    song_name=conn.recv(1024)
    if song_name!="-1":
        song_list=open('song_list.txt', 'r+') # open the song list. 
        m=song_list.read()
        song_list.close()
        m=m.split("&&&&")
        i=0
        while i<len(m):
            if song_name==m[i]:
                t="False"
            i=i+1
##        chekpending="True"
##        song_list=open('pending_song_list.txt', 'r+') # open the pending song list. 
##        m=song_list.read()
##        song_list.close()
##        m=m.split("&&&&")
##        i=0
##        while i<len(m) :
##            if song_name==m[i]:
##                chekpending="False"
##            i=i+1
    
        print t
        conn.send(t)
        ll=conn.recv(1024)
        # if the song is not exsist in the server databese:
        if t=="True":
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
            (sonlen,remote_address)=sock.recvfrom(1024)
            sock.sendto("",(remote_address))
            length=int(sonlen)
            i=0
            data3=""
            length=length/4096
            print length
            while(i<length-1):
                sock.sendto("rf",remote_address)
                (song,remote_address)=sock.recvfrom(4096)
                data3=data3+song
                i=i+1
            sock.sendto("rf",remote_address)
            print "done"
            sock.close
            file=open(song_name,"wb")
            file.write(data3)
            file.close()
            song_list=open('pending_song_list.txt', 'a')
            song_list.write(song_name+"&&&&")
            song_list.close()
            print "ttt"
            


