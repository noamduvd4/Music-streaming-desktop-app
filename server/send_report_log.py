import os
import socket
def send_report_log(conn, addr):
    addres_to_file=".\\report_folder\\"
    file=open("report_list.txt","r+")
    data1=file.read()
    file.close()
    if len(data1)!=0:
        print data1
        conn.send(data1)
        report_name=conn.recv(1024)
        if report_name!= "-1":
            print report_name
            decision=conn.recv(1024)
            print decision
            if decision=="2":
                file=open(addres_to_file+report_name,"r+")
                report=file.read()
                file.close()
                print report
                conn.send(report)
           
            if decision =="1":
                os.remove(addres_to_file+report_name)
                file=open("report_list.txt","r+")
                data1=file.read()
                file.close()
                m=data1.split("&&&&")
                m.remove(report_name)
                i=0
                data=""
                while i<(len(m)):
                    data=data+str(m[i])+ "&&&&"
                    i=i+1
                if len(data)>0:
                    data=data[:-4]
                file=open("report_list.txt","wb")
                file.write(data)
                file.close()
    else:
        print "-1"
        conn.send("-1")
