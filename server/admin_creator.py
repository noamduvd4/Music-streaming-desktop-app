import socket
import socket
"""
This program gets the socket connection between the clients the program makes the specific user into an admin
"""
def make_admin(conn, addr):
    data=""
    user_list=open('user_database.txt', 'r+') # open the file that contains the user data
    print user_list
    m=user_list.read()
    user_list.close()
    conn.send(m)
    make_admin_num=conn.recv(1024) # gets the user that the program will make into an admin
    make_admin_num=int(make_admin_num)
    print make_admin_num
    if make_admin_num!=-1:
        m=m.split("&&&&")
        m[make_admin_num+2]="y"
        print m
        i=0
        print make_admin_num
        while i<(len(m)):
            data=data+str(m[i])+ "&&&&"
            print data
            i=i+1
            
        print data
        data=data[:-4]
        print data
        song_list=open('user_database.txt', 'wb')
        song_list.write(data)
        song_list.close()
    return()
