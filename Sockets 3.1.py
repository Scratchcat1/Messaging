import sys,ast,time,socket,codecs,threading,urllib.request
import sqlite3 as sql
HOST = ''
PORT = 8000
def GetTime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print( 'Socket created')

try:
    s.bind((HOST, PORT))
except:
    print("Error binding port")
    s.close()
    sys.exit()
     
print( 'Socket bind complete')


s.listen(10)
print( 'Socket now listening')

class IP_Locator(threading.Thread):
    def __init__(self,IP,Username):
        threading.Thread.__init__(self)
        self.IP = IP
        self.Username = Username
    def run(self):
        data = codecs.decode(urllib.request.urlopen("http://ip-api.com/line/"+self.IP).read())
        data= data.split("\n")
        print("---IP Location---")
        print("Username  : "+ self.Username)
        print("IP ADDRESS: "+self.IP)
        try:
            if len(data) != 3:
                print("COUNTRY   : "+data[1])
                print("REGION    : "+data[4])
                print("CITY      : "+data[5])
                print("ZIP CODE  : "+data[6])
                print("LATITUDE  : "+data[7])
                print("LONGITUDE : "+data[8])
                print("COMPANY   : "+data[11])
            else:
                print("IP Lookup failed")
                print("Error message : " +data[1])
        except:
            pass
        print("-----------------")
        
            

class myThread (threading.Thread):
    def __init__(self, threadID, name, conn,address):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.conn = conn
        self.address = address
        print("Started Thread ID:"+str(self.threadID)+" for "+self.address[0]+":"+str(self.address[1]))
    def run(self):
        myHandeler = Handeler(self.conn,self.address)
        print("Closing thread ID "+str(self.threadID)+" for "+self.address[0]+":"+str(self.address[1]))
        
#----------------------------------------------------------------------------------
#                         Handeler section
#----------------------------------------------------------------------------------


class Handeler():
    
    def GetData(self):
        try:
            data = self.conn.recv(1024)
           # print("Recieved data from " +self.conn_info)
            data =  ast.literal_eval(codecs.decode(data))
        except:
            self.Socket_Close = True
            data = (1111,0)
        #print(data)
        return data
            
    def SendData(self,data):
        print("Sending Data to "+self.conn_info+" ...",end = "")
        self.conn.sendall(codecs.encode(str(data)))
        print(" OK ")

    #code 0
    def Login(self,Username,Password):
        pass
        

    def UsernameEntity(self,Username):
        self.Username = Username

        #code 1
    def NewUser(self, Username, Password):
        self.cur.execute("SELECT Username FROM user WHERE Username = ?",(Username,))
        if self.cur.fetchone() == None:
            self.cur.execute("INSERT INTO user VALUES(?,?,?)",(Username,Password,GetTime()))
            self.con.commit()
            print("Created User :"+Username)
            self.SendData(True)
        else:
            self.SendData(False)  # Username taken

    #code 2
    def GetNewMessages(self,GroupID= None,Since = None):  # Get messages since last connect for specific groupID
        if GroupID == None:
            self.cur.execute("SELECT * FROM user_groups WHERE Username = ?",(self.Username,))
            GroupIDs = self.cur.fetchall()
            result = []
            for Group in GroupIDs:
                GroupID = Group[0]
                if Since == None:
                    self.cur.execute("SELECT messages.* FROM messages,user WHERE  messages.GroupID =? AND datetime(messages.DateSent) > datetime(user.LastConnect)",(GroupID,))
                else:
                    self.cur.execute("SELECT messages.* FROM messages,user WHERE  messages.GroupID =? AND datetime(messages.DateSent) > ?",(GroupID,Since))
                result.append(self.cur.fetchall())
        else:
            if Since == None:
                self.cur.execute("SELECT * FROM messages,user WHERE  messages.GroupID =? AND datetime(messages.DateSent) > datetime(user.LastConnect)",(GroupID,))
            else:
                self.cur.execute("SELECT * FROM messages,user WHERE  messages.GroupID =? AND datetime(messages.DateSent) > ?",(GroupID,Since))
            result = (self.cur.fetchall(),)
        self.SendData(result)


    def GetGroupIDs(self,Username):
        self.cur.execute("SELECT GroupID FROM user_groups WHERE Username = ?",(self.Username,))
        return self.cur.fetchall()
    #code 3
    def GetGroups(self): # get groups which are assosiated with the user id and all data
        result = self.GetGroupIDs(self.Username)
        result2 =[]
        for item in result:
            self.cur.execute("SELECT * FROM groups WHERE GroupID = ?",(item))
            result2.append(self.cur.fetchall()[0])
        self.SendData(result2)
        
        
    #code 4
    def NewGroup(self,GroupName):
        self.cur.execute("INSERT INTO groups VALUES(NULL,?,?,?)",(GroupName,self.Username,GetTime()))
        GroupID = self.cur.lastrowid
        print("Created Group.  ID:"+str(GroupID)+ "  Name:"+GroupName)
        self.AddUserToGroup(self.Username,GroupID,True)
        self.con.commit()

    #code 5
    def AddUserToGroup(self,Username,GroupID,new= False):
        self.cur.execute("SELECT 1 FROM user_groups WHERE Username = ? AND GroupID = ?",(Username,GroupID))
        if self.cur.fetchall() == [] or new == True:
            self.cur.execute("SELECT 1 FROM user_groups WHERE Username = ? AND GroupID = ?",(Username,GroupID))
            ingroup = self.cur.fetchall()
            print("hi")
            if ingroup == []:
                print("Added "+Username+ " to Group ID "+str(GroupID))
                self.cur.execute("INSERT INTO user_groups VALUES(?,?,?)",(GroupID,Username,GetTime()))
            self.con.commit()
        else:
            print("User ["+ Username +"] already in Group ID ["+str(GroupID)+"]")
    #code 6
    def RemoveUserFromGroup(self,Username,GroupID):
        self.cur.execute("DELETE FROM user_groups WHERE Username = ? AND GroupID = ?",(Username,GroupID))
        self.con.commit()
    #code 7
    def DeleteUser(self,Username):
        User_Groups = self.GetGroupIDs(Username)
        for grp in User_Groups:
            self.RemoveUserFromGroup(Username,grp[0])
        self.cur.execute("DELETE FROM user WHERE Username = ?",(Username,))
        print("Deleted User :"+Username)
        self.con.commit()
    #code 8
    def AddMessage(self,data):
        self.cur.execute("INSERT INTO messages VALUES(?,?,?,?)",(data))#(self.Username,GroupID,Message,GetTime()))
        self.con.commit()
##        self.cur.execute("SELECT * FROM messages")
##        print(self.cur.fetchall())

    #code 9
    def GetLastMessages(self,GroupID,number):
        self.cur.execute("SELECT Username,Message,DateSent FROM messages WHERE GroupID =? ORDER BY DateSent DESC",(GroupID,))
        MessageList=[]
        try:
            for q in range(number):
                MessageList.append(self.cur.fetchone())
        except:
            print("")
            
        return MessageList

    def Reset(self):
        print("Database is being reset...")
        TABLES = ["user","groups","messages","user_groups"]
        for item in TABLES:
            self.cur.execute("DROP TABLE IF EXISTS {0}".format(item))
                

        #Date used is str seconds    
        self.cur.execute("CREATE TABLE user(Username TEXT PRIMARY KEY , Name TEXT, Password TEXT, LastConnect TEXT,Time_Joined INT,Last_IP TEXT,IP_Switches INT)") #Time_Joined = time since unix in days    IP Switches starts at 1
        
        self.cur.execute("CREATE TABLE groups(GroupID INTEGER PRIMARY KEY, GroupName TEXT,Creator TEXT, DateOfCreation TEXT)")
        self.cur.execute("CREATE TABLE user_groups(GroupID INT, Username TEXT, DateJoined TEXT)")
        
        self.cur.execute("CREATE TABLE messages(Username TEXT,GroupID INT,Message TEXT,DateSent TEXT)")
        self.con.commit()
        print("Database sucessfully reset")

    def Time_Days(self,Value=None):
        if Value == None:
            return int(time.time()/(60*60*24))
        else:
            return int(Value/(60*60*24))
    
    def Main(self):
        data = (42,)
        while data[0] != 1111 and not self.Socket_Close:
##            if data[0] == 0:
##                self.Login(*data[1])
##
##            elif data[0] == 1:
##                self.NewUser(*data[1])

            if data[0] == 2:
                self.GetNewMessages(*data[1])

            elif data[0] == 3:
                self.GetGroups()

            elif data[0] == 4:
                self.NewGroup(*data[1])

            elif data[0] == 5:
                self.AddUserToGroup(*data[1])

            elif data[0] == 6:
                self.RemoveUserFromGroup(*data[1])

            elif data[0] == 7:
                self.DeleteUser(*data[1])

            elif data[0] == 8:
                try:
                    self.AddMessage(data[1])
                except:
                    print("Error adding messages from :"+self.Username)
                        
                
            elif data[0] == 9:
                self.GetLastMessages(*data[1])
            data = self.GetData()

    #------------------------------------------------------
    #                     Main SECTION
    #------------------------------------------------------
    def __init__(self,conn,address):
        #try:
        print("Handeler created")
        self.address = address
        self.conn_info = self.address[0]+":"+str(self.address[1])
        self.conn = conn
        Close = False
        self.Socket_Close = False
        self.con = sql.connect("main.db")
        self.cur = self.con.cursor()
        #self.Reset()

        
        data = self.GetData()
        if data[0] == 0:
            self.cur.execute("SELECT Username FROM user WHERE Username = ? AND Password = ?",(data[1]))
            if len(self.cur.fetchall()) == 0:
                print("Authentication Failed, dropping connection...")
                Close = True
            else:
                self.Username = data[1][0]
                self.cur.execute("UPDATE user SET Last_IP = ? ,IP_Switches = IP_Switches +1 WHERE Last_IP <> ? AND Username = ?",(self.address[0],self.address[0],self.Username))
                
        elif data[0] == 1:
            self.cur.execute("SELECT Username FROM user WHERE Username = ?",(data[1][0],))
            if len(self.cur.fetchall()) == 0:
                print("Creating new user...")
                self.cur.execute("INSERT INTO user(Username,Password,LastConnect,Time_Joined,Last_IP,IP_Switches) VALUES(?,?,?,?,?,?)",(data[1][0],data[1][1],GetTime(),self.Time_Days(),self.address[0],1))
                self.Username = data[1][0]
                self.con.commit()
            else:
                print("User already exists, cancelling...")
                Close = True
                
        if Close:
            print("Failed Logon from "+self.conn_info)
            self.SendData(False)
        
        if not Close:
            self.SendData(True)
            IP_Locator(self.address[0],self.Username).start()
            self.Main()

            print("Connection error")
            
            if hasattr(self,"Username"):
                self.cur.execute("UPDATE user SET LastConnect = ? WHERE Username = ?",(GetTime(),self.Username))

        #except:
        #    pass
        print("Closing connection...")
        self.conn.close()
        print("Connection Closed")
        
try:            
    counter = 1
    while 1:
        conn, addr = s.accept()
        print( 'Connected with ' + addr[0] + ':' + str(addr[1]))
        myThread(counter,"",conn,addr).start()
        counter +=1
        
finally:
    print("Closing Socket...",end = "")
    s.close()
    print(" OK ")
    print("Exiting...")
