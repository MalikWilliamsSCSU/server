'''
Script for client side
@author: hao
'''
import protocol
import config
from socket import *
import os

class client:
    
    fileList=[] # list to store the file information

    #Constructor: load client configuration from config file
    def __init__(self):
        self.serverName, self.serverPort, self.clientPort, self.downloadPath, self.uploadPath = config.config().readClientConfig()

    # Function to produce user menu 
    def printMenu(self):
        print("Welcome to simple file sharing system!")
        print("Please select operations from menu")
        print("--------------------------------------")
        print("1. Review the List of Available Files")
        print("2. Download File")
        # *******************************
        # ADD one line here for uploading files
        print("3. Upload File")
        print("4. Quit")

    # Function to get user selection from the menu
    def getUserSelection(self):       
        ans=0
        # only accept option 1-3
        # ******************************
        # When you add upload option, you need to modify the number of options
        # you accept
        while ans>4 or ans<1:
            self.printMenu()
            try:
                ans=int(input())
            except:
                ans=0
            if (ans<=4) and (ans>=1):
                return ans
            print("Invalid Option")

    # Build connection to server
    def connect(self):
        serverName = self.serverName
        serverPort = self.serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        return clientSocket

    # Get file list from server by sending the request
    def getFileList(self):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_REQUEST," "))
        header, msg=protocol.decodeMsg(mySocket.recv(1024).decode())
        mySocket.close()
        if(header==protocol.HEAD_LIST): 
            files=msg.split(",")
            self.fileList=[]
            for f in files:
                self.fileList.append(f)
        else:
            print ("Error: cannnot get file list!")

    # function to print files in the list with the file number
    def printFileList(self):
        count=0
        for f in self.fileList:
            count+=1
            print('{:<3d}{}'.format(count,f))

    # Function to select the file from file list by file number,
    # return the file name user selected
    def selectDownloadFile(self):
        if(len(self.fileList)==0):
            self.getFileList()
        ans=-1
        while ans<0 or ans>len(self.fileList)+1:
            self.printFileList()
            print("Please select the file you want to download from the list (enter the number of files):")
            try:
                ans=int(input())
            except:
                ans=-1
            if (ans>0) and (ans<len(self.fileList)+1):
                return self.fileList[ans-1]
            print("Invalid number")

    # Function to send download request to server and wait for file data
    def downloadFile(self,fileName):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_DOWNLOAD, fileName))
        with open(self.downloadPath+"/"+fileName, 'wb') as f:
            print ('file opened')
            while True:
                #print('receiving data...')
                data = mySocket.recv(1024)
                #print('data=%s', (data))
                if not data:
                    break
            # write data to a file
                f.write(data)
        print(fileName+" has been downloaded!")
        mySocket.close()

    #********************************************
    # Please complete the upLoadFile function, the function takes a file name as
    # an input
    def uploadFile(self,fileName):
        mySocket = self.connect()

        mySocket.send(protocol.prepareMsg(protocol.HEAD_UPLOAD, fileName))

        try:
        # Open the file to read and send it in chunks
            with open(self.uploadPath + "/" + fileName, 'rb') as f:
                print(f"Uploading file: {fileName}")
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    mySocket.send(data)
            print(f"{fileName} uploaded successfully!")
        except Exception as e:
            print(f"Error uploading file: {e}")
        finally:
            mySocket.close()


    #********************************************
    # Please complete the select Upload file function,
    # The function should print out a list of files from upload folder for user to
    # select, and user need to chose one file.
    # The reture value should be a file name

    def selectUploadFile(self):
        uploadFiles = os.listdir(self.uploadPath)
        if len(uploadFiles) == 0:
            print("No files available to upload")
            return ""
        print("Available files: ")
        count = 0
        for f in uploadFiles:
            count += 1
            print('{:<3d} {}'.format(count, f))

        ans = -1
        while ans < 1 or ans > len(uploadFiles):
            try:
                ans = int(input("Enter a file to upload: "))
            except ValueError:
                ans = -1
            
            if 1 <= ans <= len(uploadFiles):
                return uploadFiles[ans - 1]
            else:
                print("Invalid selection. Please choose a valid file number.")
            
    def start(self):
        opt=0
        while opt!=4:
            opt=self.getUserSelection()
            if opt==1:
                if(len(self.fileList)==0):
                    self.getFileList()
                self.printFileList()                  
            elif opt==2:
                self.downloadFile(self.selectDownloadFile())
            elif opt==3:
                self.uploadFile(self.selectUploadFile())
            #**************************
            # You need another option for uploading files
            else:
                pass

def main():
    c=client()
    c.start()
main()