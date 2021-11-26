import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import pandas as pd
import numpy as np
import streamlit as st
import re
import base64
from streamlit.type_util import to_bytes
import streamlit_authenticator as stauth



"""
# Stylumia's Apollo For Caratlane - InSeason Demand Forecasting 
"""
names = ['Stylumia']
usernames = ['Stylumia']
passwords = ['Stylumia@321']


hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)

name, authentication_status = authenticator.login('Login','main')

if authentication_status:
    st.write('Welcome *%s*' % (name))

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    def check(email):
        #more custom email validation scenarios yet to be added here   

        '''
        Function which takes in an email address and returns a boolean value based on whether or not the email is valid.
        '''
        if(re.search(regex,email)):   
                  return True   
        else:   
             return False  
    st.write("Please Enter the Recipent's Email Adresses: ")
    Email=st.text_input("Enter your email address: ")
    st.write('Entered Email Address is :',Email)
    Email=Email.replace(" ","")
    Email=Email.split(",")
    st.write('Entered Email Address is :',Email)

    #st.write((type(Email)))

    if Email==['']:
        st.error("Please Enter Alteast one  Email Address")
    else:
        for i in Email:
            if check(i)==False:
                st.error("Please Enter Valid Email Address")
                break
            else:
                st.success("Valid Email Address, Enter Submit Button To Send Email")
                #convert Email into a list of tuples with length of 1
                Email=(list(map(lambda x: (x), Email)))
                #convert a list of emails into a list of tuples and remove comma
                Email=list(map(lambda x: (x.replace(",","")), Email))
                st.write((Email)) 
                Submit=st.button("Send Email:")

                if Submit:

                    message = Mail(

                        from_email='chaithanya.kumar@stylumia.com',
                        to_emails=Email,
                        # to_emails=[('chaithanya.kumar@stylumia.com')],
                         subject='[Test Email - Email Integration]- Caratlane In-Season Demand Forecasting',
                        html_content='<h3>Hi Everyone PFA , Jan 2022 Dateblock Level TDP and Optimised Predictions</h3>', )

                with open('Oct And Nov 21 Rolling Forecast 2.xlsx', 'rb') as f:
                     data = f.read()
                     f.close()
                encoded_file = base64.b64encode(data).decode()
                attachment = Attachment(
                    FileContent(encoded_file),
                    FileName('Oct And Nov 21 Rolling Forecast 2.xlsx'),
                    FileType('application/vnd.ms-excel'),
                    Disposition('attachment'),
                )
                

                message.attachment = attachment

                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                    st.success("Email Sent Successfully")
                except Exception as e:
                    st.error("Error While Sending Email")
                    st.write(e)  
                    print(e) 
            break

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')



