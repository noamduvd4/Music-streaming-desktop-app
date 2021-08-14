import socket
import re
import os
import sys
"""
This program gets the connection between the user and the server.
The prgram delete the song that the user chose from the server database.
"""
def delete_song(conn, addr):
    data=""
    song_list=open('song_list.txt', 'r+')
    print song_list
    m=song_list.read()
    song_list.close()
    conn.send(m)
    remove_song_number=conn.recv(1024)
    p=int(remove_song_number)
    print remove_song_number
    if remove_song_number !="-1":
        remove_song_number=int(remove_song_number)
        m=m.split("&&&&")
        print m
        print len(m)
        remove_song=str(m[p])
        os.remove(remove_song)
        i=0
        m.remove(m[p])
        print m
        while i<(len(m)-1):
            data=data+str(m[i])+ "&&&&"
            print data
            i=i+1
        data=data+str(m[i])
        print data
        song_list=open('song_list.txt', 'wb')
        song_list.write(data)
        song_list.close()
    return()


    
    
    
