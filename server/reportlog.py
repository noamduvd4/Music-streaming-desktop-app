import os
import socket
"""
Save the report on the serve data
"""
def reports(conn,addr,uname):
    addres_to_file=".\\report_folder\\" #get the file address
    t=False
    print " not yet"
    data=conn.recv(1024)
    print data
    if data!= "-1":
        file=open(addres_to_file+uname+".txt","wb")# creat new file
        file.write(data)
        print " write"
        file.close
        file=open("report_list.txt","r+")
        data=file.read()
        file.close()
        split_data=data.split("&&&&")
        i=0
        while i<len(split_data):
            if split_data[i]==uname+".txt":
                t=True
                break
            i=i+1
        if t==False:
            data=data+"&&&&"+uname+ ".txt"
            file=open("report_list.txt","wb") # change the list of the report 
            file.write(data)
            file.close()
        print "done"
            
