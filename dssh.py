#!/usr/bin/env python

"""
Name: DSSH
Author: Michel Gutardo Ramos de Lima
Description: Delete single history chat from Skype on local machine
Support: Linux and Windows >= 7
"""
version = 0.01

import sqlite3
import os
import platform
import psutil



###################################################
## Print Start Logo
###################################################
def printLogo():
    print '''

`7MM"""Yb.    .M"""bgd  .M"""bgd `7MMF'  `7MMF'
  MM    `Yb. ,MI    "Y ,MI    "Y   MM      MM
  MM     `Mb `MMb.     `MMb.       MM      MM
  MM      MM   `YMMNq.   `YMMNq.   MMmmmmmmMM
  MM     ,MP .     `MM .     `MM   MM      MM
  MM    ,dP' Mb     dM Mb     dM   MM      MM
.JMMmmmdP'   P"Ybmmd"  P"Ybmmd"  .JMML.  .JMML.

| Michel Gutardo Ramos de Lima | C40 |
| Delete Single Skype History: v.%s  |
''' % version


#::::::::::::::::::::::::::::::::::::::::::::::::::
## Description
#::::::::::::::::::::::::::::::::::::::::::::::::::
def printDescription():
    print '''
    Skype just allow you to delete all history of all partners chat. This simple tool allows you delete just a single
    chat from a single partner.

    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    :Just enter your Skype's username and partner's name(username):
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    Ps.: This will delete only local history. Your partner still having all history chat.

    :::Enjoy:::
    '''

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Check OS to get correct directory skype history
#::::::::::::::::::::::::::::::::::::::::::::::::::
def getPlatformDir():
    global baseDir
    if platform.platform()[0] == "L":
        baseDir = os.path.join(os.environ['HOME'],".Skype")

    elif platform.platform()[0] == "W":
        baseDir = os.path.join(os.environ['USERPROFILE'],"APPDATA","ROAMING","SKYPE")

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Choose account name
#::::::::::::::::::::::::::::::::::::::::::::::::::
def getSkypeUserName():
    global skypeName
    skypeName = ""
    while skypeName == "":
        skypeName = raw_input("Enter with your Skype's name: ").lower()

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Choose partner to work
#::::::::::::::::::::::::::::::::::::::::::::::::::
def getPartnerChatDelete():
    global partnerName
    partnerName = ""
    while partnerName == "":
        partnerName = raw_input("Enter partner's name that you want to delete history: ").lower()

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Connect to main user skype local db
#::::::::::::::::::::::::::::::::::::::::::::::::::
def connectDB():
    global cn
    database = "main.db"
    cn = sqlite3.connect(os.path.join(baseDir, skypeName ,database))

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Show history local chat
#::::::::::::::::::::::::::::::::::::::::::::::::::
def showHistory():
    for row in cn.execute("SELECT * FROM Messages WHERE chatname LIKE ?",('%'+partnerName+'%',)):
        print row

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Delete Chat partner
#::::::::::::::::::::::::::::::::::::::::::::::::::
def deleteChat():
    cn.execute("DELETE FROM Chats WHERE name LIKE ?",('%'+partnerName+'%',))
    cn.commit()

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Delete messages' chat partner
#::::::::::::::::::::::::::::::::::::::::::::::::::
def deleteMessages():
    cn.execute("DELETE FROM Messages WHERE chatname LIKE ?",('%'+partnerName+'%',))
    cn.commit()

#::::::::::::::::::::::::::::::::::::::::::::::::::
## Kill all Skype's process running
#::::::::::::::::::::::::::::::::::::::::::::::::::
def killSkypeProcess():
    for process in psutil.process_iter():
        if process.name().lower() =="skype":
            print process.kill()



#::::::::::::::::::::::::::::::::::::::::::::::::::
## Main function
#::::::::::::::::::::::::::::::::::::::::::::::::::
def main():

    printLogo()

    printDescription()

    getPlatformDir()

    getSkypeUserName()

    getPartnerChatDelete()

    killSkypeProcess()

    connectDB()

    confirmShowHistory = raw_input("Do you want to see all chat history?[s|y] ")
    if confirmShowHistory.lower()[0] == "y" or confirmShowHistory.lower()[0] == "s":
        showHistory()

    confirmDelHistory = raw_input("Do you really want to delete this all chat history?[s|y] ")
    if confirmDelHistory.lower()[0] == "y" or confirmDelHistory.lower()[0] == "s":
        deleteMessages()
        deleteChat()

    print("DONE! ###BYE###")

###################################
## Calling Main
###################################
if __name__ == "__main__":
    main()

