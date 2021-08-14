import socket
"""
This program gets the connection between the user and the server.
The program can delete users
"""
def remove_user(conn, addr):
    data=""
    user_list=open('user_database.txt', 'r+')
    print user_list
    m=user_list.read()
    user_list.close()
    conn.send(m)
    remove_user_number=conn.recv(1024)
    
    remove_user_number=int(remove_user_number)
    if remove_user_number !=-1:
            
        m=m.split("&&&&")
        print m
        i=0
        print remove_user_number
        while i<(len(m)):
            if (i!=remove_user_number) and (i!=remove_user_number+1) and (i!=remove_user_number+2):
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


    
    

