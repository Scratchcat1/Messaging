import sqlite3 as sql

from tkinter import *
import socket,ast,time,sys,random,codecs#,tkinter
# communication is via tuple of style (code,(parameters))
def GetTime():
    return time.strftime('%Y-%m-%d %H:%M:%S')
remote_ip = 1
remote_ip = socket.gethostbyname("google.co.uk" )
remote_ip = "192.168.0.19"
PORT = 8000
def Connect(remote_ip,PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((remote_ip, PORT))
        print("Connected to > "+ remote_ip+":"+str(PORT))
        return s
    except:
        print("Error binding port")
        print("Check address and port is up")
        print("Otherwise check server is functional")
        print("Exiting...")
        sys.exit()

class window(Frame):
    def __init__(self, parent,Colour):
        self.Reconnect()
        Frame.__init__(self, parent, background=Colour)    
        self.parent = parent
        self.Column_Weights()
        self.Name = "John"
        self.Objectlist =[]
        self.Main_Window()
        self.con = sql.connect("tkinter.db")
        self.cur = self.con.cursor()
        self.GroupID = -1
        #self.SetUser("None","None")
        self.MessageLimit = 20
        #self.Reset()
        self.Menubar()
        self.Group_Option_List((-1,))
    
    def Menubar(self):
        menubar = Menu(self.main)
        menubar.add_command(label = "Set User",command = self.User_Entry_Window)
        menubar.add_command(label = "Delete User",command = self.Delete_User_Window)
        
        groupmenu = Menu(menubar,tearoff = 1)
        groupmenu.add_command(label = "New Group",command = self.New_Group_Window)
        groupmenu.add_command(label = "Group Details",command = self.GroupDetails)
        menubar.add_cascade(label = "Group",menu = groupmenu)

        advmenu = Menu(menubar,tearoff = 1)
        advmenu.add_command(label = "Refresh",command = self.Refresh)
        advmenu.add_command(label = "Reconnect",command = self.Reconnect)
        advmenu.add_command(label = "Reset",command = self.Reset_Dialog)
        menubar.add_cascade(label = "Advanced",menu = advmenu)
        
        self.parent.config(menu = menubar)

    def Group_Option_List(self,Options):
        if hasattr(self,"Group_Option_Box"):
            Group_Option_Box.destroy()
        if len(Options) == 0:
            Options.append("No Groups")    
        self.Group_Option_Variable = IntVar()
        self.Group_Option_Variable.set(Options[0])
        Group_Option_Box = OptionMenu(self.main,self.Group_Option_Variable,*Options)
        Group_Option_Box.grid(row = 0,column = 3,padx =5 , pady = 5,sticky= "NESW")

        self.Group_Option_Variable2 = IntVar()
        self.Group_Option_Variable2.set(Options[0])
        Group_Option_Box2 = OptionMenu(self.main,self.Group_Option_Variable2,*Options)
        Group_Option_Box2.grid(row = 1,column = 3,padx =5 , pady = 5,sticky= "NESW")

    def Group_Options_Update(self,GroupData):
        GroupIDs = []
        GroupIDLocation = GroupData[0].index("GroupID")
        for group in GroupData:
            GroupIDs.append(group[GroupIDLocation])
        GroupIDs.pop(0)
        self.Group_Option_List(GroupIDs)
        
    def Column_Weights(self):
        self.parent.grid_columnconfigure(0,weight = 40)
##        self.parent.grid_columnconfigure(1,weight = 15)
##        self.parent.grid_columnconfigure(2,weight = 15)
##        self.parent.grid_columnconfigure(3,weight = 15)
##        self.parent.grid_columnconfigure(4,weight = 15)

        
    
    def Main_Window(self):
        self.parent.title("SQL test")
        self.main = self.parent
        
##        SetupLabel = Label(self.main, text="-")
##        SetupLabel.grid(row=0)
##        self.Objectlist.append(SetupLabel)
        x = 0
        self.Message_Var = StringVar()
        Message_Entry = Entry(self.main,textvariable = self.Message_Var)
        Message_Entry.grid(row = 0,column = x,padx =5 , pady = 5,sticky= "NESW")
##        self.Objectlist.append(Message_Entry)
        
        InsertButton = Button(self.main,text = "Insert",command = lambda : self.Enter(self.Message_Var.get()))
        InsertButton.grid(row=0,column = x+1,padx = 5, pady = 5,sticky = "NESW")
##        self.Objectlist.append(InsertButton)
        
##        DisplayButton = Button(self.main,text = "Display",command = lambda : self.ClearDisplay())
##        DisplayButton.grid(row=0,column = 3,padx = 5, pady = 5)
##        self.Objectlist.append(DisplayButton)
       
##        Group_Entry = Entry(self.main,width = 5)
##        Group_Entry.grid(row = 0,column = 5,padx =5 , pady = 5,sticky= "NESW")
    
        
        GroupButton = Button(self.main,text = "Group",command = lambda : self.SetGroup(self.Group_Option_Variable.get()))
        GroupButton.grid(row=0,column = x+4,padx = 5, pady = 5,sticky = "NESW")

##        ResetButton = Button(self.main,text = "Reset",command = lambda : self.Reset())
##        ResetButton.grid(row=0,column = 7,padx = 5, pady = 5)

####################################################
        

        LinkLabel = Label(self.main, text="User-Group")
        LinkLabel.grid(row=1,column = 1)                
    
        Link_User_Entry = Entry(self.main,width = 5)
        Link_User_Entry.grid(row = 1,column = 2,padx =5 , pady = 5,sticky= "NESW")

##        Link_Group_Entry = Entry(self.main,width = 5)
##        Link_Group_Entry.grid(row = 1,column = 3,padx =5 , pady = 5,sticky= "NESW")

        LinkButton = Button(self.main,text = "Link!",command = lambda : self.AddUserToGroup(Link_User_Entry.get(),self.Group_Option_Variable2.get()))
        LinkButton.grid(row=1,column = 4,padx = 5, pady = 5,sticky = "NESW")
        
    def Enter(self,Message):
        self.Message_Var.set("")
        #self.cur.execute("INSERT INTO messages SELECT ?,?,?,? WHERE NOT EXISTS (SELECT Username FROM messages WHERE Username = ? AND GroupID = ? AND Message = ? AND DateSent = ?)",(self.Username,self.GroupID,Message,GetTime(),     self.Username,self.GroupID,Message,GetTime()))
        self.con.commit()
        self.Display(self.FetchMessages(self.MessageLimit))
        self.SendData((8,(self.Username,self.GroupID,Message,GetTime())))

    def FetchMessages(self,limit):
        self.cur.execute("SELECT Message,Username,DateSent FROM messages WHERE GroupID =? ORDER BY DateSent DESC LIMIT ?",(self.GroupID,limit))
        result =[("Message","Username","DateSent")]
        result+=self.cur.fetchall()
        return result

    def FetchGroups(self):
        self.cur.execute("SELECT * FROM user_groups WHERE Username = ? ORDER BY GroupID,DateJoined",(self.Username,))
        result =[("GroupID","Username ID","DateJoined")]
        result += self.cur.fetchall()
        return result

    def ClearDisplay(self):
        for item in self.Objectlist:
            item.destroy()
        self.Objectlist =[]
        

    def Display(self,data):
        self.ClearDisplay()
        for x,item in enumerate(data):
            for y,item2 in enumerate(item):
                self.Objectlist.append(Label(self.main, text=str(item2),relief = RIDGE))
                self.Objectlist[-1].grid(row=x+2,column = y,padx = 5,pady = 5,ipadx = 2,ipady = 1,sticky = "NESW")
    
    def SetUser(self,username,password,New_User):
        data = (New_User,(username,password))
        self.SendData(data)
        try:
            worked = False
            response = self.GetData()
            print("Data received from "+remote_ip)
            if response == True:
                self.Username = username
                self.Password = password
                self.Display_Group_User()
                GroupData = self.FetchGroups()
                self.Group_Options_Update(GroupData)
                self.Display(GroupData)
                worked = True
                self.RefreshLoop()
        except:
            pass
        if not worked:
            self.Reconnect()
            print("Error logging in")
            print("Check username and password, alternativly try create user again")
        else:
            print("Logged on as [ "+self.Username+ " ] to [ "+remote_ip+":"+str(PORT)+" ]")

        
    def SetGroup(self,choice):
##        self.cur.execute("SELECT GroupID FROM user_groups WHERE Username = ?",(self.Username,))
##        result = self.cur.fetchall()
##        print(result)
        self.GroupID = int(choice)
        self.Display(self.FetchMessages(self.MessageLimit))
        self.Display_Group_User()
        
        
    def AddUserToGroup(self,Username,GroupID):
##      self.cur.execute("INSERT INTO user_groups SELECT ?,?,? WHERE NOT EXISTS(SELECT * FROM user_groups WHERE GroupID = ? AND Username = ?)",(GroupID,Username,GetTime(),GroupID,Username))
##      self.con.commit()
        self.GroupDetails(GroupID)
        self.Display_Group_User()#GroupID)
##        GroupData = self.FetchGroups()
##        self.Group_Options_Update(GroupData)
        data = (5,(Username,GroupID))
        self.SendData(data)
            
    def Reset_Dialog(self):
        top = Toplevel()
        top.wm_geometry("300x120+450+450")
        top.title("RESET")
        
        UsernameMessage = Message(top,text = "Warning!\nThis will wipe your entire local database and may take a long time.\nAre you sure you want to continue?",width = 250)
        UsernameMessage.grid(row=1,columnspan = 3,padx = 5, pady = 5,sticky = "NESW")
        OkButton = Button(top,text = "Delete",command = lambda : self.Reset_Dialog_Done(top,True))
        OkButton.grid(row = 2, column = 0,padx = 5, pady = 5)
 
        CancelButton = Button (top,text = "Cancel",command = lambda : self.Reset_Dialog_Done(top,False))
        CancelButton.grid(row = 2,column = 1,padx = 5, pady = 5)

        
    def Reset_Dialog_Done(self,top,Choice= False):
        if Choice == True:
            self.Reset()
        top.destroy()
        
    def Reset(self):
        TABLES = ["user","groups","messages","user_groups"]
        for item in TABLES:
            self.cur.execute("DROP TABLE IF EXISTS {0}".format(item))
                

        #Date used is str seconds    
        self.cur.execute("CREATE TABLE user(Username INTEGER PRIMARY KEY , Name TEXT, Password TEXT, LastConnect TEXT)")
        
        self.cur.execute("CREATE TABLE groups(GroupID INTEGER PRIMARY KEY, GroupName TEXT,Creator TEXT, DateOfCreation TEXT)")
        self.cur.execute("CREATE TABLE user_groups(GroupID INT, Username INT, DateJoined TEXT)")
        
        self.cur.execute("CREATE TABLE messages(Username INT,GroupID INT,Message TEXT,DateSent TEXT)")
        self.con.commit()
        self.Display(self.FetchMessages(self.MessageLimit))

    def GroupDetails(self,GroupID = None):
        if GroupID == None:
            self.cur.execute("SELECT Username,DateJoined FROM user_groups WHERE GroupID = ?",(self.GroupID,))
        else:
            self.cur.execute("SELECT Username,DateJoined FROM user_groups WHERE GroupID = ?",(GroupID,))
        memebers = [("Username","Date Joined")]
        memebers += self.cur.fetchall()
        self.Display(memebers)


    def User_Entry_Window(self):
        top = Toplevel()
        top.wm_geometry("160x140+450+450")
        top.title("User Selection")
        Username_Label = Label(top,text = "Username")
        Username_Label.grid(row=0)
        Username_Entry = Entry(top,width = 10)
        Username_Entry.grid(row = 0,column = 1,padx =5 , pady = 5,sticky= "NESW")


        Password_Label = Label(top,text = "Password")
        Password_Label.grid(row=1)
        Password_Entry = Entry(top,width = 10)
        Password_Entry.grid(row = 1,column = 1,padx =5 , pady = 5,sticky= "NESW")

        New_User_Var = IntVar()
        New_User_Check = Checkbutton(top,text = "New User",variable = New_User_Var)
        New_User_Check.grid(row = 2,column = 1)
        
        UsernameButton = Button(top,text = "Go!",width = 10,command = lambda : self.On_Click_User_Entry_Window(Username_Entry.get(),Password_Entry.get(),New_User_Var.get(),top))
        UsernameButton.grid(row=3,column = 1,padx = 5, pady = 5,sticky = "NESW")

    def On_Click_User_Entry_Window(self,Entry_Value,Password_Value,New_User,top):
        self.SetUser(Entry_Value,Password_Value,New_User)
        top.destroy()



    def New_Group_Window(self):
        top = Toplevel()
        top.wm_geometry("160x140+450+450")
        top.title("New Group")
        Group_Label = Label(top,text = "Group Name")
        Group_Label.grid(row=0)
        Group_Entry = Entry(top,width = 10)
        Group_Entry.grid(row = 0,column = 1,padx =5 , pady = 5,sticky= "NESW")
        
        GroupButton = Button(top,text = "Go!",width = 10,command = lambda : self.On_Click_New_Group_Window(Group_Entry.get(),top))
        GroupButton.grid(row=1,column = 1,padx = 5, pady = 5,sticky = "NESW")

    def On_Click_New_Group_Window(self,GroupName,top):
        self.SendData(  (4,(GroupName,)))
        top.destroy()

    def Delete_User_Window(self):
        top = Toplevel()
        top.wm_geometry("160x140+450+450")
        top.title("Delete User")
        Delete_Label = Label(top,text = "Username")
        Delete_Label.grid(row=0)
        Delete_Entry = Entry(top,width = 10)
        Delete_Entry.grid(row = 0,column = 1,padx =5 , pady = 5,sticky= "NESW")
        
        DeleteButton = Button(top,text = "Delete",width = 10,command = lambda : self.On_Click_Delete_User_Window(Delete_Entry.get(),top))
        DeleteButton.grid(row=1,column = 1,padx = 5, pady = 5,sticky = "NESW")

    def On_Click_Delete_User_Window(self,Username,top):
        self.SendData(  (7,(Username,)))
        top.destroy()
    

    def Display_Group_User(self,GroupID = None):
        if hasattr(self,"UserLabel"):
            self.UserLabel.destroy()
        if GroupID == None:
            data = "Group:  "+str(self.GroupID)
        else:
            data = "Group:  "+str(GroupID)
        self.UserLabel = Label(self.main,text = ("User:"+self.Username+"    "+data))
        self.UserLabel.grid(row = 1)
        

##    def GroupWindow(self):
##        group  = Tk()
    def RefreshLoop(self):
        #try:
        self.Refresh()
        #except:
            #print("Error while refreshing")
        self.after(20000,self.RefreshLoop)

    def Refresh(self):
        if hasattr(self,"Username"):
            print("Refreshing ...")
            self.SendData( (2,()))
            message_list = self.GetData()[0]
            for q in range(0,len(message_list)):
                message_list[q] += message_list[q]
##                print(len(message_list[q]))
##            print(message_list)
##            for item in message_list:
##                print(str(len(item))+"  " +str(item))
            self.cur.executemany("INSERT INTO messages(Username,GroupID,Message,DateSent) SELECT ?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM messages WHERE Username =? AND GroupID =? AND Message =? AND DateSent = ?)",message_list)


            
            self.SendData((3,))
            GroupData =self.GetData()
            for item in GroupData:
                item2 = item + (item[0],)
                #print(item2)
                self.cur.execute("INSERT INTO Groups(GroupID,GroupName,Creator,DateOfCreation) SELECT ?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM Groups WHERE GroupID = ?)",(item2))
            #print(GroupData)
            GroupData = ["GroupID"]+ GroupData
            self.Group_Options_Update(GroupData)
            print("Refresh  OK ")
            
    def Reconnect(self):
        if hasattr(self,"conn"):
            self.conn.close()
            print("Closed existing connection")
        self.conn = Connect(remote_ip,PORT)
    def Decode(self,data):
        return ast.literal_eval(codecs.decode(data))
    def SendData(self,data):
        print("Sending Data to "+remote_ip+":"+str(PORT)+" ...",end = "")
        self.conn.sendall(codecs.encode(str(data)))
        print(" OK ")
    def GetData(self):
        data = self.conn.recv(1024)
        return ast.literal_eval(codecs.decode(data))









    

def main_window():
    root = Tk()
    root.geometry("600x600+300+300")
    wind = window(root,"white")
    root.after(20000,wind.Refresh)
    root.mainloop()


main_window()
