"""
The program gets username, password from the user and his choice (loggin or register).
The program can log in to the server or can creat a new user
"""
def loggin(uname, password,choice):
    f = open('user_database.txt', 'r+')
    m=f.read().split("&&&&")
    print len(m)
    i=0
    if choice=="1": # log in to the server 
        while i<(len(m)-1):
            if m[i] == uname and m[i+1] == password:
                print m[i+2]
                if str(m[i+2])=="y":
                    print "hi " + m[i] + "! you have succesfuly logged in as an admin. welcome to the system. "
                    user=[True,True]
                    f.close()
                    return user
                    break
                else:
                    print "hi " + m[i] + "! you have succesfuly logged in. welcome to the system."
                    user=[True,False]
                    f.close()
                    return user
                    break
            i=i+3
        user=[False,False]
        return user
    if choice=="2": # register to the server 
        f = open('user_database.txt', 'r+')
        m=f.read().split("&&&&")
        i=0
        while i<(len(m)-1):
            if m[i] == uname:
                user=[False,False]
                return user
                f.close()
            i=i+3
        user=[True,False]
        return user
    if choice == "3":
        f = open('user_database.txt', 'a')
        f.write("&&&&"+uname+"&&&&"+password+"&&&&n")
        print "welcome to the system"
        f.close()
        user=[True,False]
        return user
    
           
