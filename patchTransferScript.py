#!/usr/bin/python

import paramiko
import re
import os
import sys
import time
import datetime
from subprocess import Popen,PIPE

ServerNodes=[‘server1,’server2’,’server3,’server4’,’server5’]
user = ‘admin’

def sendTrap(hostname,error_state,ua,message):

    # Acquire Epoch time for notification
    ep_time_now = int(time.time())
    ep_time_fut = ep_time_now + (7 * 86400)

    
    SN_CLASSNAME=host
    SN_INSTANCENAME=host
    SN_EVENTNAME =  ua + " Patch transfer status FAILED to " + host
    SN_ELEMENTCLASS=host
    SN_ELEMENTNAME=host
    SN_EVENT_SEVERITY="4"
    SN_EVENTTEXT =  "SNTEST Host -  " + host + ";;;  " + message
    SN_FIRSTNOTIFY=ep_time_now
    SN_EVENT_SUMMARY=ua + " Patch trasfer status FAILED to " + host
    SN_EVENTID=ua + " Patch trasfer status FAILED to " + host
    SN_KIA="";
    SN_PLATFORM="UNIX/LINUX";

    # Sending notification email
    


NotificationSent = 'False'
PatchPath = os.listdir('/local/path/Patches')

for PatchID in PatchPath:	
    if re.search('.L7P',PatchID):
        localpath=‘/local/path/Patches/'+PatchID
        remotepath=‘/remote/Patches/‘+PatchID

        if (os.path.isfile(localpath)):
            for node in ServerNodes:
                try:
                    host = node
                    password = os.popen('/usr/bin/wget -O- -q --no-check-certificate https://'+host+':8443/getPwd?p=admin').read()
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        client.connect(host, username=user, password=password)
                        sftp = client.open_sftp()
                    except:
                        print 'host: %s: %s' % (host, "Password retrieved for admin user is not CORRECT. Kindly UPDATE it before running this script again!!!!")
                        warn_mess = "Transfer script failed to copy PatchID"+PatchID+". Password retrieved for admin user is not CORRECT."
                        print warn_mess
                        patchtrasfer_state = "warning"
                        sendTrap(host,patchtrasfer_state,"Patch transfer Notification: Transfer Failed",warn_mess)
                        NotificationSent = 'True'
                    print("Please Wait.......")
                    print 'host: %s: %s' % (host, "Provided patch ID is coping to remote server.....")
                    info=sftp.put(localpath, remotepath)
                    sftp.close()
                    client.close()
                    Localstatinfo = os.stat(localpath)
                    if (Localstatinfo.st_size == info.st_size):
                        print 'host: %s: %s %s' % (host, PatchID, "patch successfully transferred to remote server.")
                    else:
                        print 'host: %s: %s %s' % (host, PatchID, "patch transfer FAILED or INTERRUPTED!!")
                        warn_mess = "Transfer script failed to copy PatchID"+PatchID+". Transfer FAILED or INTERRUPTED!!"
                        print warn_mess
                        patchtrasfer_state = "warning"
                        sendTrap(host,patchtrasfer_state,"Patch transfer Notification: Transfer Failed",warn_mess)
                except:
                    if (NotificationSent == 'False'):
                        print 'host: %s: %s %s' % (host, PatchID,"patch transfer FAILED to remote server.")
                        warn_mess = "Transfer script failed to copy PatchID"+PatchID+". Transfer FAILED or INTERRUPTED!!"
                        print warn_mess
                        patchtrasfer_state = "warning"
                        sendTrap(host,patchtrasfer_state,"Patch transfer Notification: Transfer Failed",warn_mess)
