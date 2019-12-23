# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:48:46 2019

@author: Parth
"""
import concurrent.futures 
import pickle
import re
import smtplib
import dns.resolver
import time
import psycopg2
start_time = time.time()

print("Connecting to database")
try:     
    conn = psycopg2.connect(database='Hiranandani', user = "postgres", password = "parth123n@#*", host = "127.0.0.1", port = "5432")    
except:
    print("Create database first")

mycursor=conn.cursor()

table='emails'

def verify(inputAddress):
    valid_emails=list()
#    for inputAddress in emails:
    try:
        fromAddress= 'abc@gmail.com'
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        
        addressToVerify= str(inputAddress)
        
        match=re.match(regex,addressToVerify)
        
        if match==None:
            print('Bad syntax')
            raise ValueError("Bad syntax")
            
        splitAddress= addressToVerify.split('@')
        domain=str(splitAddress[1])
        
        records= dns.resolver.query(domain,'MX')
        mxRecord= records[0].exchange
        mxRecord= str(mxRecord)
        
        server=smtplib.SMTP()
        server.set_debuglevel(0)
        
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(fromAddress)
        code,message =server.rcpt(str(addressToVerify))
        server.quit()
        
        if code==250:
            valid_emails.append(inputAddress)
            print(inputAddress)
            print("Success")
            #sql = "INSERT INTO 'emails' (valid) VALUES (%s)"
            #val = (str(addressToVerify))
            #mycursor.execute(sql, val)
            #conn.commit()
        else:
            print("Bad")
    except Exception as e:
        print(e)
   # return valid_emails

with open('emails.pickle', 'rb') as f:
    emails = pickle.load(f)


verify(emails)
print("--- %s seconds ---" % (time.time() - start_time))

verify('nagaarkarparth@gmail.com')

conn.close()
'''
with concurrent.futures.ThreadPoolExecutor(4) as executor:
    future = executor.submit(verify, emails[:12])
    return_value = future.result()
'''