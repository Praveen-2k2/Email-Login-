"""import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'posinapraveen2002@gmail.com'
SMTP_PASSWORD = 'ihlz tjgz cwqm ekro'
FROM_EMAIL = SMTP_USERNAME
TO_EMAIL = input("Enter TO_EMAIL:")
SUBJECT = 'Test Email from Python'
BODY = 'This is a test email sent using Python!'

def send_email():
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = SUBJECT

        # Attach the body with the msg instance
        msg.attach(MIMEText(BODY, 'plain'))

        # Create an SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        # Start TLS for security
        server.starttls()

        # Log in to the server
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Convert the message to a string and send it
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, TO_EMAIL, text)

        # Terminate the SMTP session and close the connection
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Call the function to send the email
send_email()"""




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# import smtplib
# from email.message import EmailMessage

# app = FastAPI()

# class EmailSchema(BaseModel):
#     recipient: EmailStr
#     subject: str
#     body: str

# def send_email(recipient: str, subject: str, body: str):
#     sender_email = "posinapraveen2002@gmail.com"
#     sender_password = "ihlz tjgz cwqm ekro"
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587

#     msg = EmailMessage()
#     msg['From'] = sender_email
#     msg['To'] = recipient
#     msg['Subject'] = subject
#     msg.set_content(body)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/send-email/")
# async def send_email_endpoint(email: EmailSchema):
#     send_email(email.recipient, email.subject, email.body)
#     return {"message": "Email sent successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)































#------------------------------------------------------sending a link--------------------------------------------------------------

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel, EmailStr
# #from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import  Session
# import uuid  
# import smtplib
# from email.message import EmailMessage
# from database import  engine, get_db
# from models import EmailsClicked, Base


# class EmailSchema(BaseModel):
#     recipient: EmailStr
#     subject: str
#     body: str
    


# # Asynchronous function to create all tables
# async def create_tables():
#     async with engine.begin() as conn:
#         # Recreate the table with the updated schema
#         await conn.run_sync(Base.metadata.create_all)

# app = FastAPI()


# def send_email(recipient: str, subject: str, body: str, is_html:bool=False):
#     sender_email = "posinapraveen2002@gmail.com"
#     sender_password = "ihlz tjgz cwqm ekro"
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587

#     msg = EmailMessage()
#     msg['From'] = sender_email
#     msg['To'] = recipient
#     msg['Subject'] = subject
#     msg.set_content(body)

#     if is_html:
#         msg.add_alternative(body,subtype='html')
#     else:
#         msg.set_content(body)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/send-email/")
# async def send_email_endpoint(email: EmailSchema, db: Session = Depends(get_db)):
#     #prepare HTML Content
#     html_body = f"""
#     <html>
#     <body>
#         <p>,History, Purpose and Usage</p>
#         <p>Please click <a href='https://www.youtube.com/results?search_query=how+to+send+unique+link+in+gamil+by+using+fastapi+python+and+postgresql'>here</a> to visit our website.</p>
#         <p>Best regards,<br>Your Company</p>
#         <!-- Add any additional HTML comments here -->
#     </body>
#     </html>
#     """

#     # Send the email
#     send_email(email.recipient, email.subject, html_body, is_html=True)

#     # Save to the database
#     db_email = EmailsClicked(recipient=email.recipient, subject=email.subject, body=email.body)
#     db.add(db_email)
#     db.commit()
#     db.refresh(db_email)
    
#     return {"message": "Email sent successfully", "email_id": db_email.id}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

















































#############---------------------------------------tracking link and email status----------------------------------------##############################

# """

# import logging
# import uuid
# from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status
# from fastapi.responses import RedirectResponse , Response
# from email.message import EmailMessage
# import aiosmtplib
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from pydantic import BaseModel, EmailStr

# from database import get_db#, engine, Base
# from models import EmailLinked

# app = FastAPI()

# #logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.WARNING)

# # Pydantic schemas
# class CreateEmailLinkedSchema(BaseModel):
#     generated_id: str
#     status: str
#     user_id: str
#     mail_id: EmailStr
#     message: str
#     subject: str
#     actual_link: str

# class EmailSchema(BaseModel):
#     mail_id: EmailStr
#     subject: str

# # # Asynchronous function to create all tables
# # async def create_tables():
# #     async with engine.begin() as conn:
# #         # Recreate the table with the updated schema
# #         await conn.run_sync(Base.metadata.create_all)



# # Run the create_tables function on startup
# @app.on_event("startup")
# async def on_startup():
#     from database import create_tables
#     await create_tables()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# async def send_email(email_data: EmailSchema, db: AsyncSession):
#     smtp_host = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_user = "posinapraveen2002@gmail.com"
#     smtp_password = "ihlz tjgz cwqm ekro"

#     msg = EmailMessage()
#     msg["From"] = smtp_user
#     msg["To"] = email_data.mail_id
#     msg["Subject"] = email_data.subject
#     msg.set_content("This is the email content.") # Set the plain text content

#     # Generate unique link and store email data
#     unique_id = str(uuid.uuid4())
#     #tracking_pixel_url = f"http://127.0.0.1:8000/track-email/{unique_id}"
#     # click_link_url = f"http://127.0.0.1:8000/click-link?link={unique_link}"

#     html_message = f"""
#     <html>
#     <body>
#         <p>History, Purpose and Usage</p>
#         <a href='http://127.0.0.1:8000/click-link?link={unique_id}'>Click me</a>
#         <p>Best regards,<br>Your Company</p>
#         <img src='http://127.0.0.1:8000/track-email/{unique_id}' alt="" style="display:none;"/>
#     </body>
#     </html>
# """

#     # Set the HTML content
#     msg.add_alternative(html_message, subtype='html')

#     try:
#         await aiosmtplib.send(
#             msg,
#             hostname=smtp_host,
#             port=smtp_port, 
#             start_tls=True, 
#             username=smtp_user, 
#             password=smtp_password
#             )
        
#         logging.info(f"Email sent to {email_data.mail_id}")

#         # Store email data into the database(Consistent Status Values)
#         new_click = CreateEmailLinkedSchema(
#             generated_id=unique_id,
#             status="sent",  # Status is "sent" initially
#             #link_status="link not opened ",   # opened is "not opened" initially
#             user_id='11',  # Default user_id
#             mail_id=email_data.mail_id,
#             message=html_message,
#             subject=email_data.subject,
#             actual_link=f'https://www.codetru.com'
#         )
#         new_db_click = EmailLinked(**new_click.dict())
#         db.add(new_db_click)
#         await db.commit()
#         await db.refresh(new_db_click)
#         logging.info(f"Stored email data into database: {new_db_click}")
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email sending failed")

# @app.post("/send-email/")
# async def send_email_endpoint(email_data: EmailSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
#     background_tasks.add_task(send_email, email_data, db)
#     return {"message": "Email has been sent"}


# # Endpoint to track email opening
# @app.get("/track-email/{unique_id}")
# async def track_email(unique_id: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status == "sent":
#                 email_data.status = "opened"
#                 await db.commit()
#                 await db.refresh(email_data)
#             return "Email opened"
#         return "Email not opened"
    
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

  
# # Endpoint to handle the email link click and redirect
# @app.get("/click-link")
# async def click_link(link: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == link))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status=="opened " or "sent":
#                 email_data.status = "clicked"
#                 await db.commit()
#                 await db.refresh(email_data)
#         return RedirectResponse(url=email_data.actual_link)
#     except Exception as e:
#         logging.error(f"Error handling link click: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

























































# praveen.test0123@gmail.com
# yezd okrr kgrm jktw



##########################________________________________________________________________________________________________________________________________________######################################################################    


















# smtp_host = "smtp.gmail.com"
# smtp_port = 587
# smtp_user = "praveen.test0123@gmail.com"
# smtp_password = "yezd okrr kgrm jktw"

from fastapi_pagination import add_pagination, paginate, LimitOffsetPage
from datetime import datetime, timedelta
# import webbrowser 
# import os
from collections import defaultdict

import imaplib
import email
from email.header import decode_header
from typing import List, Dict
import logging
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status, Request, Query
from fastapi.responses import RedirectResponse, Response
from email.message import EmailMessage
import aiosmtplib
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CreateEmailLinkedSchema, EmailSchema
from pydantic import BaseModel, EmailStr
from database import get_db
from models import EmailLinked

app = FastAPI(title="Email")

logging.basicConfig(level=logging.WARNING)


# # Pydantic schemas
# class CreateEmailLinkedSchema(BaseModel):
#     generated_id: str
#     status: str
#     user_id: str
#     mail_id: EmailStr
#     message: str
#     subject: str
#     actual_link: str

# class EmailSchema(BaseModel):
#     mail_id: EmailStr
#     subject: str

@app.on_event("startup")
async def on_startup():
    from database import create_tables
    await create_tables()
    # Start the background task to check for replies
    # asyncio.create_task(check_for_replies())

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def send_email(email_data: EmailSchema, db: AsyncSession):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "praveen.test0123@gmail.com"
    smtp_password = "yezd okrr kgrm jktw"

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = email_data.mail_id
    msg["Subject"] = email_data.subject
    msg.set_content("This is the email content.")

    unique_id = str(uuid.uuid4())

    html_message = f"""
    <html>
    <body>
        <p>History, Purpose and Usage</p>
        <a href='http://127.0.0.1:8000/click-link?link={unique_id}'>Click me</a>
        <p>Best regards,<br>Your Company</p>
        <img src='http://127.0.0.1:8000/track-email/{unique_id}' alt="" style="display:none;"/>
    </body>
    </html>
    """

    msg.add_alternative(html_message, subtype='html')

    try:
        await aiosmtplib.send(
            msg,
            hostname=smtp_host,
            port=smtp_port,
            start_tls=True,
            username=smtp_user,
            password=smtp_password
        )
        
        logging.info(f"Email sent to {email_data.mail_id}")

        new_click = CreateEmailLinkedSchema(
            generated_id=unique_id,
            status="sent",
            user_id='11',
            mail_id=email_data.mail_id,
            message=html_message,
            subject=email_data.subject,
            actual_link=f'https://www.codetru.com'
        )
        new_db_click = EmailLinked(**new_click.dict())
        db.add(new_db_click)
        await db.commit()
        await db.refresh(new_db_click)
        logging.info(f"Stored email data into database: {new_db_click}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email sending failed")

@app.post("/send-email/")
async def send_email_endpoint(email_data: EmailSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    background_tasks.add_task(send_email, email_data, db)
    return {"message": "Email has been sent"}

@app.get("/track-email/{unique_id}")
async def track_email(unique_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
        email_data = result.scalars().first()
        if email_data:
            if email_data.status == "sent":
                email_data.status = "opened"
                await db.commit()
                await db.refresh(email_data)
            return "Email opened"
        return "Email not opened"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/click-link")
async def click_link(link: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == link))
        email_data = result.scalars().first()
        if email_data:
            if email_data.status in ["opened", "sent"]:
                email_data.status = "clicked"
                await db.commit()
                await db.refresh(email_data)
        return RedirectResponse(url=email_data.actual_link)
    except Exception as e:
        logging.error(f"Error handling link click: {e}")     
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


# from personal.txt import Your_email, Your_password
# Gmail IMAP server details
IMAP_HOST = 'imap.gmail.com'
IMAP_PORT = 993
IMAP_USER = 'praveen.test0123@gmail.com'
IMAP_PASSWORD = 'yezd okrr kgrm jktw' 




@app.get("/imap/send_email_filter_by_date_range_&_page")
def fetch_inbox(from_date:str=Query(..., description="Fetching the date email in DD-MM-YYY "),
                to_date:str=Query(...,description="Fetching the date email in DD-MM-YYYY format format and the to_date will not display so that enter next day"),
                page:int = Query(1, description="Page number"),
                page_size:int = Query(10, description="Number of emails per page")
):   
    
    fetched_emails=[]
    # unique_id= str(uuid.uuid4())

    # unique_id=str(uuid.UUID)

    try:
        # Connect to the Gmail IMAP server
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

        # Log in to the Gmail account
        imap.login(IMAP_USER, IMAP_PASSWORD)

        # Select the "Sent Mail" folder
        imap.select('"[Gmail]/Sent Mail"')

        # Get the date formate
        start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

        # start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
        # end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
        # start_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
        # end_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
        # Get the date 24 hours ago
        # date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
        # date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
      
        # Search for emails in inbox that are newer than 24 hours
        # res, messages = imap.search(None, f'(SINCE "{date}")')
        # res, messages = imap.search(None, f'(ON "{date}")')
        res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')
        
        email_id=messages[0].split()

        #pagination
        total_email=len(email_id)
        start_page=(page-1)*page_size
        end_page=min(start_page+page_size,total_email)

        # Iterate over the email IDs
        for i in email_id[start_page:end_page]:
            res, msg = imap.fetch(i, "(uid RFC822)")

            # uid=None
            for i in msg:
                if isinstance(i, tuple):
                    # Extract UID from the response
                    unique_id= str(uuid.uuid4())
                    # uid = response[0].split()[2].decode()
                    msg = email.message_from_bytes(i[1])

                    # Get the UID from the response
                    # uid_response = msg[0].decode()
                    # uid = uid_response.split()[2]  # Extract the UID from the response


                    # Decode the email subject
                    subject = msg["Subject"]
                    # if subject is not None:
                    #     subject, encoding = decode_header(subject)[0]
                    #     if isinstance(subject, bytes):
                    #         subject = subject.decode(encoding if encoding else "utf-8")
                    # else:
                    #     subject = "(No subject)"

                    # Get sender, recipient, and date
                    From = msg["From"]
                    To = msg["To"]
                    date = msg["Date"]
                    # unique_id=msg["unique_id"]

                
                    # Append email details to the list
                    fetched_emails.append({
                        "id":unique_id,
                        "from": From,
                        "subject": subject,
                        "to": To,
                        "date": date
                    })
                    
        # Logout from the server
        imap.logout()

        return{
            "page":page,
            "page_size":page_size,
            "total_email":total_email,
            "email":fetched_emails
        }
    except Exception as e:
        return{'error':str(e)}
   

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)







@app.get("/imap/received_email_filter_by_date_page_category")
def fetch_inbox(
    from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
    to_date: str = Query(..., description="Date in DD-MM-YYYY format and the to_date will not display so that enter next day"),
    category: str = Query("primary", description="Category: primary, social, promotions"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of emails per page")
):
    fetched_emails = []
    # unique_id = str(uuid.uuid4())

    try:
        # Connect to Gmail IMAP server
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        imap.login(IMAP_USER, IMAP_PASSWORD)

        # Select the inbox folder
        imap.select("inbox")

        # Convert input date format
        start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

        
        if  category== "primary":
            res, messages = imap.search(None, "UNFLAGGED")
        elif category == "promotions":
            res, messages = imap.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_PROMOTIONS"')
        elif category== "social":
            res, messages = imap.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_SOCIAL"')
        else:
            raise ValueError("Invalid category")
        
        res, messages = imap.search(
            None, f'X-GM-RAW "category:{category}"', f'(SINCE "{start_date}" BEFORE "{end_date}")'
        )


        # # Define IMAP search categories based on Gmail's labels
        # category_label = {
        #     "primary": "CATEGORY_PERSONAL",
        #     "social": "CATEGORY_SOCIAL",
        #     "promotions": "CATEGORY_PROMOTIONS"
        # }.get(category.lower(), "CATEGORY_PERSONAL")  # Default to Primary if category not valid

        # # Search for emails in the specified category and date range
        # res, messages = imap.search(
        #     None, f'X-GM-RAW "category:{category_label}"', f'(SINCE "{start_date}" BEFORE "{end_date}")'
        # )

        email_id = messages[0].split()

        # Pagination logic
        total_email = len(email_id)
        start_page = (page - 1) * page_size
        end_page = min(start_page + page_size, total_email)

        # Iterate over email IDs in the current page
        for i in email_id[start_page:end_page]:
            res, msg = imap.fetch(i, "(UID RFC822)")

            for i in msg:
                if isinstance(i, tuple):
                    unique_id= str(uuid.uuid4())
                    msg = email.message_from_bytes(i[1])

                    # Decode email fields
                    subject = msg["Subject"]
                    # if subject:
                    #     subject, encoding = decode_header(subject)[0]
                    #     if isinstance(subject, bytes):
                    #         subject = subject.decode(encoding if encoding else "utf-8")
                    # else:
                    #     subject = "(No subject)"

                    From = msg["From"]
                    To = msg["To"]
                    date = msg["Date"]

                    # Append email details
                    fetched_emails.append({
                        "id": unique_id,
                        "from": From,
                        "subject": subject,
                        "to": To,
                        "date": date
                    })

        # Logout from the server
        imap.logout()

        return {
            "page": page,
            "page_size": page_size,
            "total_email": total_email,
            "category":category,
            "emails": fetched_emails
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)










class EmailThreader:
    def __init__(self):
        self.threads: Dict[str, List[Dict]] = defaultdict(list)

    def add_email(self, email_data: Dict):
        thread_id = email_data.get('thread_id') or email_data['message_id']
        self.threads[thread_id].append(email_data)

    def get_threaded_emails(self):
        return list(self.threads.values())

def parse_email(msg, unique_id):
    subject = msg["Subject"]
    if subject:
        subject, encoding = decode_header(subject)[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
    else:
        subject = "(No subject)"

    from_ = msg["From"]
    to = msg["To"]
    date = msg["Date"]
    message_id = msg["Message-ID"]
    in_reply_to = msg.get("In-Reply-To")
    references = msg.get("References", "").split()
    
    thread_id = in_reply_to or (references[-1] if references else None) or message_id

    return {
        "id": unique_id,
        "message_id": message_id,
        "thread_id": thread_id,
        "from": from_,
        "subject": subject,
        "to": to,
        "date": date,
        "in_reply_to": in_reply_to,
        "references": references
    }

@app.get("/imap/fetch_threaded_emails")
def fetch_threaded_emails():
    threader = EmailThreader()

    try:
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        imap.login(IMAP_USER, IMAP_PASSWORD)
        imap.select('"[Gmail]/Sent Mail"')

        res, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()

        for i in email_ids:
            res, msg = imap.fetch(i, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    unique_id = str(uuid.uuid4())
                    email_message = email.message_from_bytes(response[1])
                    email_data = parse_email(email_message, unique_id)
                    threader.add_email(email_data)

        imap.logout()

        threaded_emails = threader.get_threaded_emails()

        return {
            "total_threads": len(threaded_emails),
            "threads": threaded_emails
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
















@app.get("/imap/unread_email")
def fetch_unread():
    fetched_emails=[]

    try:
        imap=imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)
        imap.login(IMAP_USER,IMAP_PASSWORD)

        imap.select("inbox")

        res, messages = imap.search(None,f'(UNSEEN)')

        email_id = messages[0].split()

        for i in email_id:
            res, msg = imap.fetch(i, "(UID RFC822)")

            for response in msg:
                if isinstance(response, tuple):
                    unique_id= str(uuid.uuid4())
                    msg = email.message_from_bytes(response[1])

                    # Decode email fields
                    subject = msg["Subject"]
                    # if subject:
                    #     subject, encoding = decode_header(subject)[0]
                    #     if isinstance(subject, bytes):
                    #         subject = subject.decode(encoding if encoding else "utf-8")
                    # else:
                    #     subject = "(No subject)"

                    From = msg["From"]
                    To = msg["To"]
                    date = msg["Date"]

                    # Append email details
                    fetched_emails.append({
                        "id": unique_id,
                        "from": From,
                        "subject": subject,
                        "to": To,
                        "date": date
                    })

        imap.logout()            

        return fetched_emails

    except Exception as e:
        return {'error':str(e)}    

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)





@app.delete("/Imap/Delete_email")
async def delete_email(email_id:str=Query(description="enter the deleted email id")):
    # fetched_email=[]

    try:
        imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
        imap.login(IMAP_USER,IMAP_PASSWORD)

        # select all messages from the sender
        imap.select('INBOX')
        # res, messages = imap.uid('search', None,f'FROM "{email_id}"')
        res, messages = imap.search( None,f'FROM "{email_id}"')

        # delete the emails
        if messages[0]:
            for i in messages[0].split():
                imap.store( i, '+FLAGS', '\\Deleted')
                # imap.uid('store', i, '+FLAGS', '\\Deleted')
                #FOR PERMANENT DELETE FROM TRASH ALSO
                # imap.store("1:*",'+X-GM-LABELS', '\\Trash')

            imap.expunge()
            imap.logout()

        return {   
                "status": "success",
                "message": f"Email with email id {email_id} has been deleted",
             } 
    except Exception as e:
        return {'error': str(e)}      








# @app.delete("/Imap/Delete_email_subject")
# async def delete_email(subject: str = Query(description="enter the subject of emails you want to delete")):
#     try:
#         with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as imap:
#             imap.login(IMAP_USER, IMAP_PASSWORD)
#             imap.select("INBOX")
            
#             # Search for emails with the given subject
#             res, messages = imap.search(None, f'SUBJECT "{subject}"')
            
#             if not messages[0]:
#                 return {"status": "info", "message": f"No emails found with subject: {subject}"}
            
#             deleted_count = 0
#             for i in messages[0].split():
#                 # Fetch the email details
#                 res, msg_data = imap.fetch(i, "(RFC822)")
#                 for response_part in msg_data:
#                     if isinstance(response_part, tuple):
#                         email_body = email.message_from_bytes(response_part[1])
#                         email_subject = decode_header(email_body["subject"])[0][0]
#                         if isinstance(email_subject, bytes):
#                             email_subject = email_subject.decode()
                        
#                         # Double-check if the subject matches (case-insensitive)
#                         if subject.lower() in email_subject.lower():
#                             # Mark the email for deletion
#                             imap.store(i, "+FLAGS", "\\Deleted")
#                             deleted_count += 1
            
#             # Expunge to actually delete the marked emails
#             imap.expunge()
#             imap.logout()
            
#             return {
#                 "status": "success",
#                 "message": f"Deleted {deleted_count} email(s) with subject containing: {subject}",
#             }


#     except Exception as e:
#         return {'error': str(e)}
    
  





@app.delete("/Imap/Delete_by_range")
async def delete_email(from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
                       to_date: str = Query(..., description="Date in DD-MM-YYYY format and the to_date will not display so that enter next day")
                       ):
    # fetched_email=[]

    try:
        imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
        imap.login(IMAP_USER,IMAP_PASSWORD)

        # select all messages from the sender
        imap.select('INBOX')

        start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

        res, messages = imap.search( None,f'(SINCE "{start_date}" BEFORE "{end_date}")')

        # delete the emails
        if messages[0]:
            for uid in messages[0].split():
                imap.store( uid, '+FLAGS', '\\Deleted')
                #FOR PERMANENT DELETE FROM TRASH ALSO
                # imap.store("1:*",'+X-GM-LABELS', '\\Trash')

            imap.expunge()
            imap.logout()
            

        return {   
                "status": "success",
                "message": f"Email with email id's has been deleted in a given range",
             } 
    except Exception as e:
        return {'error': str(e)}    









@app.delete("/Imap/Delete_by_in_email_id_range")
async def delete_email(email_id:str=Query(description="enter the deleted email id"),
                       from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
                       to_date: str = Query(..., description="Date in DD-MM-YYYY format and the to_date will not display so that enter next day")
                       ):
    # fetched_email=[]

    try:
        imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
        imap.login(IMAP_USER,IMAP_PASSWORD)

        # select all messages from the sender
        imap.select('INBOX')

        start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
        end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

        result, messages = imap.uid('search', None,f'FROM "{email_id}"',f'(SINCE "{start_date}" BEFORE "{end_date}")')

        # delete the emails
        if messages[0]:
            for uid in messages[0].split():
                imap.uid('store', uid, '+FLAGS', '\\Deleted')
                #FOR PERMANENT DELETE FROM TRASH ALSO
                # imap.store("1:*",'+X-GM-LABELS', '\\Trash')

            imap.expunge()
            imap.logout()
            

        return {   
                "status": "success",
                "message": f"Email with email id {email_id} has been deleted in a given range",
             } 
    except Exception as e:
        return {'error': str(e)}    






    


# @app.delete("/Imap/Delete_email_through_email_id_&_sibject")
# async def delete_email(email_id: str = Query(description="enter the email_id that you want to delete"),
#                        subject: str = Query(description="enter the subject of the email tat you want to delete ")
#                        ):
#     try:
#         imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)
#         imap.login(IMAP_USER,IMAP_PASSWORD)

#         imap.select('Inbox')

#         res, messages=imap.search((None,f'FROM"{email_id}"'),(None,f'SUBJECT"{subject}"'))

#         if not messages[0]:
#             return {"status": "info", "message": f"No emails found with subject: {subject}"}
            
        
#         deleted_count = 0
#         for i in messages[0].split():
#             # Fetch the email details
#             res, msg_data = imap.fetch(i, "(RFC822)")
#             for response_part in msg_data:

#                 if isinstance(response_part, tuple):
#                     email_body = email.message_from_bytes(response_part[1])

#                     email_subject = decode_header(email_body["subject"])[0][0]
#                     if isinstance(email_subject, bytes):
#                         email_subject = email_subject.decode()
                            
#                          # Double-check if the subject matches (case-insensitive)
#                         if subject.lower() in email_subject.lower():
#                             # Mark the email for deletion
#                             imap.store(i, "+FLAGS", "\\Deleted")
#                             deleted_count += 1
                
#                 # Expunge to actually delete the marked emails
#             imap.expunge()
#             imap.logout()
            
#             return {
#                 "status": "success",
#                 "message": f"Deleted {deleted_count} email_id: {email_id} with subject containing: {subject}",
#                 }
        


#     except Exception as e:
#         return {"error ": str(e)}    

















# @app.delete("/Imap/Delete_email")
# async def delete_email(email_id:str=Query(description="enter the deleted email id")):
#     # fetched_email=[]

#     try:
#         imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
#         imap.login(IMAP_USER,IMAP_PASSWORD)

#         imap.select("inbox")

#         # res, messages = imap.search(None,f'HEADER "Message-ID" "{email_id}"')
#         res, messages = imap.search(None,f'FROM "{email_id}"')

#             # if not messages[0]:

#         for i in messages[0].split():

#             imap.store(i,"+FLAGS","\\DELETED")

#             res,msg=imap.fetch(i,"(RFC822)")

#             for i in msg:
#                 if isinstance(i,tuple):
#                     msg=email.message_from_bytes(i[1])

#                     #     # Decode email fields
#                     # subject = msg["Subject"]
#                     # if subject:
#                     #     subject, encoding = decode_header(subject)[0]
#                     #     if isinstance(subject, bytes):
#                     #         subject = subject.decode(encoding if encoding else "utf-8")
#                     # else:
#                     #     subject = "(No subject)"

#                     #     # subject = msg["subject"]
#                     #     sender = msg["from"]
            
#             # Expunge to actually delete the marked email
#             imap.expunge()

#             imap.logout()

#             return {   
#                 "status": "success",
#                 "message": f"Email with email id {email_id} has been deleted",
#             #     "details": {
#             #         "subject": subject,
#             #         "sender": sender
#              } 
             
#                 # imap.store(i,"+FLAGS","\\DELETED")

#         # # from the selected mailbox (in this case, INBOX)
#                 # imap.expunge()
#                 # return{"DELETED":email_id}
#     except Exception as e:
#         return {'error': str(e)}

    # finally:
    #     imap.close()
    #     imap.logout()


  
    # except imaplib.IMAP4.error as e:
    #     raise HTTPException(status_code=500, detail=f"IMAP error: {str(e)}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


# @app.delete("/Imap/Delete_email_subject")
# async def delete_email(subject:str=Query(description="enter the subject that you want to delete")):
#     # fetched_email=[]

#     try:
         
#         imap=imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
#         imap.login(IMAP_USER,IMAP_PASSWORD)

#         imap.select("inbox")

#         # res, messages = imap.search(None,f'SUBJECT"{subject}"')
#         status, messages = imap.search(None, f'SUBJECT "{subject}"')

#         if messages[0]:
#             for uid in messages[0].split():
#                 imap.uid('store', uid, '+FLAGS', '\\Deleted')
#             imap.expunge()

#         # for mail in messages:

#         #     imap.store(mail,"+FLAGS","\\DELETED")

#         #     res,msg=imap.fetch(mail,"(RFC822)")

#         #     for i in msg:
#         #         if isinstance(i,tuple):
#         #             msg=email.message_from_bytes(i[1])

#         #             subject=msg["subject"]

#         # Expunge to actually delete the marked email
#         imap.expunge()     
        
#         imap.logout()

#         return{   
#                 "status": "success",
#                 "message": f"Email with subject: {subject} has been deleted",
#             }   

#     except Exception as e:
#         return {'error': str(e)}
        


# @app.delete("/Imap/Delete_email_subject")
# async def delete_email(subject:str=Query(description="enter the subject that you want to delete")):
#     # fetched_email=[]

#     try:
         
#         imap=imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
#         imap.login(IMAP_USER,IMAP_PASSWORD)

#         imap.select("inbox")

#         # res, messages = imap.search(None,f'SUBJECT"{subject}"')
#         status, messages = imap.search(None, f'SUBJECT "{subject}"')

#         for mail in messages:

#             imap.store(mail,"+FLAGS","\\DELETED")

#             res,msg=imap.fetch(mail,"(RFC822)")

#             for i in msg:
#                 if isinstance(i,tuple):
#                     msg=email.message_from_bytes(i[1])

#                     subject=msg["subject"]
#         # Expunge to actually delete the marked email
#         imap.expunge()     
        
#         imap.logout()

#         return{   
#                 "status": "success",
#                 "message": f"Email with subject: {subject} has been deleted",
#                 # "details": {
#                 #     "subject": subject,
#                 #     "sender": sender
#             }   

#     except Exception as e:
#         return {'error': str(e)}
 
                    #  decode the email subject
                #     subject = decode_header(msg["Subject"])[0][0]
                #     if isinstance(subject, bytes):
                # # if it's a bytes type, decode to str
                #         subject = subject.decode()
      
    #                 subject=msg["subject"]

    #             return {"Deleting the subject : ":subject}    
    #     imap.store(mail,"+FLAGS","\\DELETED")

    # # from the selected mailbox (in this case, INBOX)
    #     # imap.expunge()
    #     # imap.close()
    #     imap.logout()    


    # except Exception as e:
    #     return {'error': str(e)}






























# @app.get("/IMAP/get_email_conversation")
# async def get_email_conversation():
#     try:
#         imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)
#         imap.login(IMAP_USER,IMAP_PASSWORD)
         
#         imap.select('INBOX') 

#         res, messages= imap.search(None,f'(HEADER Message-ID"")')
        
#         if messages[0]:
#             # Get the latest email in the conversation
#             latest_email=messages[0].split()[-1]
#             res,msg=imap.fetch(latest_email,'(RFC822)')
#             raw_email=msg[0][1]

#             #Parse the raw email
#             email_msg=email.message_from_bytes(raw_email)

#             #Extract sender
#             sender, encoding = decode_header(email_msg.get("From"))[0]
#             if isinstance(sender,bytes):
#                 sender=sender.decode(encoding or "utf-8")

                
    
#     except Exception as e:
#         return {'error':str(e)}


# from typing import List, Dict
# from dataclasses import dataclass
# from collections import defaultdict
# import re


# @dataclass
# class Email:
#     message_id: str
#     subject: str
#     from_: str
#     to: str
#     date: str
#     references: List[str]
#     in_reply_to: str

#     def __post_init__(self):
#         self.subject = self.normalize_subject(self.subject)
    
#     @staticmethod
#     def normalize_subject(subject: str) -> str:
#         return re.sub(r'^(Re|Fwd):\s*', '', subject, flags=re.IGNORECASE).strip()

# class EmailThreader:
#     def __init__(self):
#         self.threads: Dict[int, List[Email]] = defaultdict(list)
#         self.subject_to_thread: Dict[str, int] = {}

#     def thread_emails(self, emails: List[Email]) -> List[List[Email]]:
#         for email in emails:
#             self._add_email_to_thread(email)
#         return list(self.threads.values())

#     def _add_email_to_thread(self, email: Email):
#         thread_id = self._find_thread_id(email)
#         self.threads[thread_id].append(email)
#         self.subject_to_thread[email.subject] = thread_id

#     def _find_thread_id(self, email: Email) -> int:
#         thread_id = None

#         if email.in_reply_to:
#             thread_id = self._find_thread_by_message_id(email.in_reply_to)

#         if not thread_id and email.references:
#             thread_id = self._find_thread_by_references(email.references)

#         if not thread_id:
#             thread_id = self.subject_to_thread.get(email.subject, id(email))

#         return thread_id

#     def _find_thread_by_message_id(self, message_id: str) -> int:
#         for thread_id, thread in self.threads.items():
#             if any(e.message_id == message_id for e in thread):
#                 return thread_id
#         return None

#     def _find_thread_by_references(self, references: List[str]) -> int:
#         for thread_id, thread in self.threads.items():
#             if any(e.message_id in references for e in thread):
#                 return thread_id
#         return None

# @app.get("/imap/fetch_all_emails")
# def fetch_all_emails():
#     fetched_emails = []

#     try:
#         # Connect to Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox folder
#         imap.select("inbox")

#         # Search for all emails
#         res, messages = imap.search(None, 'ALL')
#         email_ids = messages[0].split()

#         # Iterate over email IDs
#         for email_id in email_ids:
#             res, msg = imap.fetch(email_id, "(RFC822)")

#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email fields
#                     subject = msg["Subject"]
#                     if subject:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     from_ = msg["From"]
#                     to = msg["To"]
#                     date = msg["Date"]
#                     message_id = msg["Message-ID"]
#                     references = msg.get("References", "").split()
#                     in_reply_to = msg.get("In-Reply-To")

#                     # Create Email object
#                     email_obj = Email(
#                         message_id=message_id,
#                         subject=subject,
#                         from_=from_,
#                         to=to,
#                         date=date,
#                         references=references,
#                         in_reply_to=in_reply_to
#                     )

#                     fetched_emails.append(email_obj)

#         # Logout from the server
#         imap.logout()

#         # Thread the emails
#         threader = EmailThreader()
#         threaded_emails = threader.thread_emails(fetched_emails)

#         # Convert threaded emails to JSON-serializable format
#         json_threads = []
#         for thread in threaded_emails:
#             json_thread = []
#             for email in thread:
#                 json_thread.append({
#                     "id": str(uuid.uuid4()),
#                     "message_id": email.message_id,
#                     "from": email.from_,
#                     "subject": email.subject,
#                     "to": email.to,
#                     "date": email.date
#                 })
#             json_threads.append(json_thread)

#         return {
#             "total_threads": len(json_threads),
#             "threads": json_threads
#         }

#     except Exception as e:
#         return {'error': str(e)}


















































































































































































































# # search for specific mails by sender
# status, messages = imap.search(None, 'FROM "googlealerts-noreply@google.com"')

# # to get mails by subject
# status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')

# # to get mails after a specific date
# status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
# # to get mails before a specific date
# status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')

# # to get all mails
# status, messages = imap.search(None, "ALL")


# for mail in messages:
#     _, msg = imap.fetch(mail, "(RFC822)")
#     # you can delete the for loop for performance if you have a long list of emails
#     # because it is only for printing the SUBJECT of target email to delete
#     for response in msg:
#         if isinstance(response, tuple):
#             msg = email.message_from_bytes(response[1])
#             # decode the email subject
#             subject = decode_header(msg["Subject"])[0][0]
#             if isinstance(subject, bytes):
#                 # if it's a bytes type, decode to str
#                 subject = subject.decode()
#             print("Deleting", subject)
#     # mark the mail as deleted
#     imap.store(mail, "+FLAGS", "\\Deleted")

# # permanently remove mails that are marked as deleted
# # from the selected mailbox (in this case, INBOX)
# imap.expunge()
# # close the mailbox
# imap.close()
# # logout from the account
# imap.logout()





# import imaplib
# import email
# from email.header import decode_header

# def delete_email_by_id(username, password, imap_server, message_id):
#     # Connect to the IMAP server
#     mail = imaplib.IMAP4_SSL(imap_server)
    
#     try:
#         # Login to the account
#         mail.login(username, password)
        
#         # Select the mailbox (e.g., "INBOX")
#         mail.select("INBOX")
        
#         # Search for the email with the specific Message-ID
#         _, message_numbers = mail.search(None, f'HEADER "Message-ID" "{message_id}"')
        
#         if message_numbers[0]:
#             for num in message_numbers[0].split():
#                 # Fetch the email message
#                 _, msg = mail.fetch(num, "(RFC822)")
#                 for response in msg:
#                     if isinstance(response, tuple):
#                         # Parse the email content
#                         email_message = email.message_from_bytes(response[1])
#                         subject, encoding = decode_header(email_message["Subject"])[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding or "utf-8")
#                         from_header, encoding = decode_header(email_message.get("From"))[0]
#                         if isinstance(from_header, bytes):
#                             from_header = from_header.decode(encoding or "utf-8")
                        
#                         print(f"Deleting email:")
#                         print(f"Message-ID: {message_id}")
#                         print(f"From: {from_header}")
#                         print(f"Subject: {subject}")
                        
#                         # Mark the email for deletion
#                         mail.store(num, '+FLAGS', '\\Deleted')
                
#                 # Permanently remove the email flagged for deletion
#                 mail.expunge()
#                 print("Email deleted permanently.")
#         else:
#             print(f"No email found with Message-ID: {message_id}")
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
    
#     finally:
#         # Close the mailbox and logout
#         mail.close()
#         mail.logout()

# # Usage
# username = "your_email@example.com"
# password = "your_password"
# imap_server = "imap.example.com"
# message_id = "<example-message-id@domain.com>"

# delete_email_by_id(username, password, imap_server, message_id)





# @app.delete("/Imap/Delete_email")
# async def delete_email(email_id: str = Query(description="enter the Message-ID of the email to delete")):
#     try:
#         with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as imap:
#             imap.login(IMAP_USER, IMAP_PASSWORD)
#             imap.select("INBOX")
            
#             # Search for the email with the given Message-ID
#             _, messages = imap.search(None, f'HEADER "Message-ID" "{email_id}"')
            
#             if not messages[0]:
#                 raise HTTPException(status_code=404, detail=f"Email with Message-ID {email_id} not found")
            
#             for num in messages[0].split():
#                 # Mark the email for deletion
#                 imap.store(num, "+FLAGS", "\\Deleted")
                
#                 # Fetch the email details for confirmation
#                 _, msg_data = imap.fetch(num, "(RFC822)")
#                 for response_part in msg_data:
#                     if isinstance(response_part, tuple):
#                         email_body = email.message_from_bytes(response_part[1])
#                         subject = email_body["subject"]
#                         sender = email_body["from"]
            
#             # Expunge to actually delete the marked email
#             imap.expunge()
            
#             return {
#                 "status": "success",
#                 "message": f"Email with Message-ID {email_id} has been deleted",
#                 "details": {
#                     "subject": subject,
#                     "sender": sender
#                 }
#             }

#     except imaplib.IMAP4.error as e:
#         raise HTTPException(status_code=500, detail=f"IMAP error: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.delete("/Imap/Delete_email")
# async def delete_email(email_id:str=Query(description="enter the deleted email id")):
#     # fetched_email=[]

#     try:
#         imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT) 
#         imap.login(IMAP_USER,IMAP_PASSWORD)

#         # select all messages from the sender
#         imap.select('INBOX')
#         result, data = imap.uid('search', None,f'FROM "{email_id}"')

#         # delete the emails
#         if data[0]:
#             for uid in data[0].split():
#                 imap.uid('store', uid, '+FLAGS', '\\Deleted')
#             imap.expunge()

#         # logout from your Gmail account
#             # imap.close()
#             imap.Logout()

#         return {   
#                 "status": "success",
#                 "message": f"Email with email id {email_id} has been deleted",
#              } 
#     except Exception as e:
#         return {'error': str(e)}      




# @app.get("/imap/fetch_thread_ids")
# def fetch_thread_ids(
#     from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
#     to_date: str = Query(..., description="Date in DD-MM-YYYY format and the to_date will not display so that enter next day"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of emails per page")
# ):
#     fetched_threads = []

#     try:
#         # Connect to Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox folder
#         imap.select("inbox")

#         # Convert input date format
#         start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

#         # Search for emails in the specified date range
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')
#         email_ids = messages[0].split()

#         # Pagination logic
#         total_emails = len(email_ids)
#         start_page = (page - 1) * page_size
#         end_page = min(start_page + page_size, total_emails)

#         # Iterate over email IDs in the current page
#         for i in email_ids[start_page:end_page]:
#             res, msg = imap.fetch(i, "(RFC822)")

#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])
#                     message_id = msg["Message-ID"]
                    
#                     # Append email thread ID details
#                     fetched_threads.append({
#                         "message_id": message_id,
#                         "subject": msg["Subject"],
#                         "from": msg["From"],
#                         "date": msg["Date"]
#                     })

#         # Logout from the server
#         imap.logout()

#         return {
#             "page": page,
#             "page_size": page_size,
#             "total_emails": total_emails,
#             "threads": fetched_threads
#         }

#     except Exception as e:
#         return {"error": str(e)}





# @app.get("/imap/fetch_all_emails")
# def fetch_all_emails():
#     fetched_emails = []

#     try:
#         # Connect to Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox folder
#         imap.select("inbox")

#         # Search for all emails
#         res, messages = imap.search(None, 'ALL')
#         email_ids = messages[0].split()

#         # Iterate over email IDs
#         for email_id in email_ids:
#             res, msg = imap.fetch(email_id, "(RFC822)")

#             for response in msg:
#                 if isinstance(response, tuple):
#                     unique_id = str(uuid.uuid4())
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email fields
#                     subject = msg["Subject"]
#                     if subject:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details
#                     fetched_emails.append({
#                         "id": unique_id,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#         return {
#             "total_emails": len(fetched_emails),
#             "emails": fetched_emails
#         }

#     except Exception as e:
#         return {'error': str(e)}























# import os
# import imaplib
# import email
# from email.header import decode_header
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import asyncio
# import concurrent.futures

# app = FastAPI()

# # Replace these with your actual credentials
# IMAP_HOST = "imap.gmail.com"
# IMAP_PORT = 993
# IMAP_USER = "your_email@gmail.com"
# IMAP_PASSWORD = "your_password"

# # Pydantic model for email fetching requests
# class ThreadIDRequest(BaseModel):
#     thread_ids: list[str]

# # Function to fetch emails by thread IDs
# def fetch_emails_by_thread_ids(thread_ids):
#     fetched_emails = []
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to your Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Iterate over the provided thread IDs
#         for thread_id in thread_ids:
#             # Search for the email with the specified thread ID
#             res, messages = imap.search(None, f'THREADID "{thread_id}"')

#             # Iterate over the email IDs returned for this thread
#             for num in messages[0].split():
#                 res, msg = imap.fetch(num, "(RFC822)")
#                 for response in msg:
#                     if isinstance(response, tuple):
#                         msg = email.message_from_bytes(response[1])

#                         # Decode the email subject
#                         subject = msg["Subject"]
#                         if subject is not None:
#                             subject, encoding = decode_header(subject)[0]
#                             if isinstance(subject, bytes):
#                                 subject = subject.decode(encoding if encoding else "utf-8")
#                         else:
#                             subject = "(No subject)"

#                         # Get sender, recipient, and date
#                         from_ = msg["From"]
#                         to = msg["To"]
#                         date = msg["Date"]

#                         # Append email details to the list
#                         fetched_emails.append({
#                             "from": from_,
#                             "subject": subject,
#                             "to": to,
#                             "date": date
#                         })

#         # Logout from the server
#         imap.logout()

#     except Exception as e:
#         fetched_emails.append({"error": str(e)})

#     return fetched_emails

# @app.post("/fetch-emails/")
# async def fetch_emails(request: ThreadIDRequest):
#     loop = asyncio.get_event_loop()

#     # Run the blocking function in a thread pool
#     with concurrent.futures.ThreadPoolExecutor() as pool:
#         emails = await loop.run_in_executor(pool, fetch_emails_by_thread_ids, request.thread_ids)

#     return {"emails": emails}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)














































































































































# @app.get("/imap/unread_emails")
# def fetch_unread_emails(
#     from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
#     to_date: str = Query(..., description="Date in DD-MM-YYYY format"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of emails per page")
# ):
#     fetched_emails = []

#     try:
#         # Connect to Gmail IMAP server
#         # print("Connecting to IMAP server...")
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox folder
#         imap.select("inbox")

#         # # Convert input date formats
#         start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

#         # print(f"Searching unread emails from {start_date} to {end_date}...")

#         # Search for unread emails within the specified date range
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}" UNSEEN)')
#         # res, messages = imap.search(None, f'(UNSEEN)')

#         # print(f"Search result: {res}, Messages: {messages}")
        
#         if res != 'OK' or not messages[0]:
#             return {"error": "No unread emails found for the given criteria."}

#         email_id = messages[0].split()
#         # print(f"Fetched Email IDs: {email_id}")

#         # Pagination logic
#         total_email = len(email_id)
#         start_page = (page - 1) * page_size
#         end_page = min(start_page + page_size, total_email)
#         # print(f"Total emails: {total_email}, Displaying emails from {start_page} to {end_page}")

#         # Iterate over email IDs in the current page
#         for num in email_id[start_page:end_page]:
#             res, msg = imap.fetch(num, "(UID RFC822)")
#             # print(f"Fetched message: {msg}")

#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email fields
#                     subject = msg["Subject"]
#                     if subject:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details
#                     fetched_emails.append({
#                         "id": str(uuid.uuid4()),  # Generate a unique UUID for each email
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#         return {
#             "page": page,
#             "page_size": page_size,
#             "total_email": total_email,
#             "emails": fetched_emails
#         }

#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





































































































































































































































































































































































































































































































































































































# @app.get("/imap/recived_email_filter_by_date_range_&_page")

# # Function to fetch emails from the inbox with a required date
# def fetch_inbox(from_date:str=Query(..., description="Fetching the date email in DD-MM-YYYY "),
#                 to_date:str=Query(...,description="Fetching the date email in DD-MM-YYYY format and the to_date will not display so that enter next day"),
#                 page: int = Query(1, description="Page number"),
#                 page_size: int = Query(10, description="Number of emails per page")
# ):
   
#     fetched_emails = []

#     # unique_id=str(uuid.uuid4())

#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Get the date formate
#         start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")
#         # start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # start_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # end_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # Get the date 24 hours ago
#         # date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
#         # date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
#         # Search for emails in inbox that are newer than 24 hours
#         # res, messages = imap.search(None, f'(SINCE "{date}")')
#         # res, messages = imap.search(None, f'(ON "{date}")')
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')
        
#         email_id=messages[0].split()

#         #pagination
#         total_email=len(email_id)
#         start_page=(page-1)*page_size
#         end_page=min(start_page+page_size,total_email)

#         # Iterate over the email IDs
#         for num in email_id[start_page:end_page]:
#             res, msg = imap.fetch(num, "(UID RFC822)")

#             # uid=None
#             for response in msg:
#                 if isinstance(response, tuple):
#                     unique_id= str(uuid.uuid4())
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From=msg["From"]
#                     To=msg["To"]
#                     date=msg["Date"]
#                     # unique_id=msg["unquie_id"]
   

                
#                     # Append email details to the list
#                     fetched_emails.append({
#                         "id":unique_id,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
                        
#                     })
                    
#         # Logout from the server
#         imap.logout()

#         return{
#             "page":page,
#             "page_size":page_size,
#             "total_email":total_email,
#             "email":fetched_emails
#         }
#     except Exception as e:
#         return{'error':str(e)}
   

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # For the filtering the primary, promotion and social
# @app.get('/')
# def fetch_email():
#     fetched_emails = []

    

#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # if  == "primary":
#         #     res, messages = mail.search(None, "UNFLAGGED")
#         # elif  == "promotions":
#         #     res, messages = mail.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_PROMOTIONS"')
#         # elif == "social":
#         #     res, messages = mail.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_SOCIAL"')
#         # else:
#         #     raise ValueError("Invalid category")

#     except Exception as e:
#         return{'error':str(e)}    
#     return 

# @app.get("/imap/received_email_by_category")
# def fetch_inbox(
#     from_date: str = Query(..., description="Date in DD-MM-YYYY format"),
#     to_date: str = Query(..., description="Date in DD-MM-YYYY format and the to_date will not display so that enter next day"),
#     category: str = Query("primary", description="Category: primary, social, promotions"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of emails per page")
# ):
#     fetched_emails = []
#     # unique_id = str(uuid.uuid4())

#     try:
#         # Connect to Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox folder
#         imap.select("inbox")

#         # Convert input date format
#         start_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%b-%Y")

        
#         if  category== "primary":
#             res, messages = imap.search(None, "UNFLAGGED")
#         elif category == "promotions":
#             res, messages = imap.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_PROMOTIONS"')
#         elif category== "social":
#             res, messages = imap.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_SOCIAL"')
#         else:
#             raise ValueError("Invalid category")
        
#         res, messages = imap.search(
#             None, f'X-GM-RAW "category:{category}"', f'(SINCE "{start_date}" BEFORE "{end_date}")'
#         )


#         # # Define IMAP search categories based on Gmail's labels
#         # category_label = {
#         #     "primary": "CATEGORY_PERSONAL",
#         #     "social": "CATEGORY_SOCIAL",
#         #     "promotions": "CATEGORY_PROMOTIONS"
#         # }.get(category.lower(), "CATEGORY_PERSONAL")  # Default to Primary if category not valid

#         # # Search for emails in the specified category and date range
#         # res, messages = imap.search(
#         #     None, f'X-GM-RAW "category:{category_label}"', f'(SINCE "{start_date}" BEFORE "{end_date}")'
#         # )

#         email_id = messages[0].split()

#         # Pagination logic
#         total_email = len(email_id)
#         start_page = (page - 1) * page_size
#         end_page = min(start_page + page_size, total_email)

#         # Iterate over email IDs in the current page
#         for num in email_id[start_page:end_page]:
#             res, msg = imap.fetch(num, "(UID RFC822)")

#             for response in msg:
#                 if isinstance(response, tuple):
#                     unique_id= str(uuid.uuid4())
#                     msg = email.message_from_bytes(response[1])

#                     # Decode email fields
#                     subject = msg["Subject"]
#                     if subject:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details
#                     fetched_emails.append({
#                         "id": unique_id,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#         return {
#             "page": page,
#             "page_size": page_size,
#             "total_email": total_email,
#             "category":category,
#             "emails": fetched_emails
#         }

#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

















































































































# class EmailConfig(BaseModel):
#     email: str
#     password: str
#     imap_server: str
#     imap_port: int = 993

# class EmailMessage(BaseModel):
#     subject: str
#     sender: str
#     date: str
#     category: str

# def fetch_emails(config: CreateEmailLinkedSchema, category: str) -> List[EmailSchema]:
# # def fetch_emails(config: EmailConfig, category: str) -> List[EmailMessage]:
#     try:
#         # Connect to the IMAP server
#         mail = imaplib.IMAP4_SSL(config.imap_server, config.imap_port)
#         mail.login(config.email, config.password)

#         # Select the inbox
#         mail.select("INBOX")

#         # Search for emails based on category
#         if category == "primary":
#             _, messages = mail.search(None, "UNFLAGGED")
#         elif category == "promotions":
#             _, messages = mail.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_PROMOTIONS"')
#         elif category == "social":
#             _, messages = mail.search(None, 'HEADER "X-Gmail-Labels" "CATEGORY_SOCIAL"')
#         else:
#             raise ValueError("Invalid category")

#         email_list = []
#         for num in messages[0].split():
#             _, msg = mail.fetch(num, "(RFC822)")
#             email_message = email.message_from_bytes(msg[0][1])
            
#             subject, encoding = decode_header(email_message["Subject"])[0]
#             if isinstance(subject, bytes):
#                 subject = subject.decode(encoding or "utf-8")
            
#             sender, encoding = decode_header(email_message["From"])[0]
#             if isinstance(sender, bytes):
#                 sender = sender.decode(encoding or "utf-8")
            
#             date = email_message["Date"]

#             email_list.append(EmailMessage(
#                 subject=subject,
#                 sender=sender,
#                 date=date,
#                 category=category
#             ))

#         mail.close()
#         mail.logout()

#         return email_list

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/fetch_emails/{category}")
# async def get_emails(category: str, config: CreateEmailLinkedSchema):
#     if category not in ["primary", "promotions", "social"]:
#         raise HTTPException(status_code=400, detail="Invalid category")
    
#     emails = fetch_emails(config, category)
#     return {"emails": emails}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

















































































































#  try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the "Sent Mail" folder
#         imap.select('"[Gmail]/Sent Mail"')

#         # Get the date format
#         start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")

#         # Search for emails in the date range
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')

#         email_ids = messages[0].split()

#         # Pagination
#         total_emails = len(email_ids)
#         start_page = (page - 1) * page_size
#         end_page = min(start_page + page_size, total_emails)

#         # Iterate over the email IDs for the selected page
#         for num in email_ids[start_page:end_page]:
#             # Fetch the UID and RFC822 message
#             res, msg_data = imap.fetch(num, "(UID RFC822)")

#             for response in msg_data:
#                 if isinstance(response, tuple):
#                     # Extract UID from the response
#                     uid = response[0].split()[2].decode()

#                     # Extract the email message
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details along with UID to the list
#                     fetched_emails.append({
#                         "id": uid,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })
                    




























#  for num in email_ids[start_page:end_page]:
#             # Fetch both the RFC822 message and the UID
#             res, msg_data = imap.fetch(num, "(UID RFC822)")

#             uid = None
#             for response in msg_data:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Get the UID from the response
#                     uid_response = msg_data[0].decode()
#                     uid = uid_response.split()[2]  # Extract the UID from the response

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details and UID to the list
#                     fetched_emails.append({
#                         "id": uid,  # Use the UID as the unique identifier
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })








# @app.get("/imap/filter_by_number")
# def fetch_inbox(n:int= Query(description="Number of emails to fetch")):
# # def fetch_inbox(n: int = Query(5, description="Number of emails to fetch")):
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the "Sent Mail" folder
#         res, messages = imap.select('"[Gmail]/Sent Mail"')

#         # Calculate the total number of sent messages
#         messages = int(messages[0])

#         email_list = []

#         # Iterate over the emails, starting from the most recent
#         for i in range(messages, messages - n, -1):
#             res, msg = imap.fetch(str(i), "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject, encoding = decode_header(msg["Subject"])[0]
#                     if isinstance(subject, bytes):
#                         subject = subject.decode(encoding if encoding else "utf-8")

#                     # Get sender, recipient, and subject details
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Add the email data to the list
#                     email_list.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

# #         # Logout from the server
# #         imap.logout()

# #         # Return the list of emails
# #         return email_list

# #     except Exception as e:
# #         return {"error": str(e)}

# # if __name__ == "__main__":
# #     fetch_inbox()


# @app.get("/imap/recived_email_filter_by_date_range_&_page")

# # Function to fetch emails from the inbox with a required date
# def fetch_inbox(from_date:str=Query(..., description="Fetching the date email in YYYY-MM-DD "),
#                 to_date:str=Query(...,description="Fetching the date email in YYYY-MM-DD format format and the to_date will not display so that enter next day"),
#                 page: int = Query(1, description="Page number"),
#                 page_size: int = Query(10, description="Number of emails per page")
# ):
   
#     fetched_emails = []

#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Get the date formate
#         start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # start_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # end_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # Get the date 24 hours ago
#         # date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
#         # date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
#         # Search for emails in inbox that are newer than 24 hours
#         # res, messages = imap.search(None, f'(SINCE "{date}")')
#         # res, messages = imap.search(None, f'(ON "{date}")')
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')
        
#         email_id=messages[0].split()

#         #pagination
#         total_email=len(email_id)
#         start_page=(page-1)*page_size
#         end_page=min(start_page+page_size,total_email)

#         # Iterate over the email IDs
#         for num in email_id[start_page:end_page]:
#             res, msg = imap.fetch(num, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]


                
#                     # Append email details to the list
#                     fetched_emails.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })
                    
#         # Logout from the server
#         imap.logout()

#         return{
#             "page":page,
#             "page_size":page_size,
#             "total_email":total_email,
#             "email":fetched_emails
#         }
#     except Exception as e:
#         return{'error':str(e)}
   

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# @app.get("/imap/filter_by_date_range")

# # Function to fetch emails from the inbox with a required date
# def fetch_inbox(from_date:str=Query(..., description="Fetching the date email in YYYY-MM-DD "),to_date:str=Query(...,description="Fetching the date email in YYYY-MM-DD format format and the to_date will not display so that enter next day")):
#     fetched_emails = []
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Get the date formate
#         start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # start_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # end_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # Get the date 24 hours ago
#         # date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
#         # date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
#         # Search for emails in inbox that are newer than 24 hours
#         # res, messages = imap.search(None, f'(SINCE "{date}")')
#         # res, messages = imap.search(None, f'(ON "{date}")')
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')

#         # Iterate over the email IDs
#         for num in messages[0].split():
#             res, msg = imap.fetch(num, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]


                
#                     # Append email details to the list
#                     fetched_emails.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })
                    
#         # Logout from the server
#         imap.logout()

#     except Exception as e:
#         fetched_emails.append({"error": str(e)})
    
#     return (fetched_emails)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



















# @app.get("/imap/filter_by_date_range")
# def fetch_inbox(
#     from_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
#     to_date: str = Query(..., description="Fetching the date email in YYYY-MM-DD format format and the to_date will not display so that enter next day"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of emails per page")
# ):
#     fetched_emails = []

#     # id=str(uuid.uuid4())

#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Get the date formate
#         start_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # start_date = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # end_date = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         # Get the date 24 hours ago
#         # date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
#         # date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
#         # Search for emails in inbox that are newer than 24 hours
#         # res, messages = imap.search(None, f'(SINCE "{date}")')
#         # res, messages = imap.search(None, f'(ON "{date}")')
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')

#         email_id=messages[0].split()

#         #Pagination 
#         total_emails=len(email_id)
#         start_page=(page-1)*page_size
#         end_page=min(start_page+page_size,total_emails)

#         # Iterate over the email IDs
#         for num in email_id[start_page:end_page]:
#             res, msg = imap.fetch(num, "(RFC822 ID)")
#             uid=None

#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     #Get the UID from the response
#                     uid_response = msg[0].decode()
#                     id = uid_response.split()[2]  # Extract UID from response

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]
#                     # id=msg["id"]


                
#                     # Append email details to the list
#                     fetched_emails.append({
#                         "id":id,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })
                    
#         # Logout from the server
#         imap.logout()

#         return{
#             "page":page,
#             "page_size":page_size,
#             "total_emails":total_emails,
#             "email":fetched_emails
#         }

#     except Exception as e:
#         return {"error": str(e)}
#         # fetched_emails.append({"error": str(e)})
    



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Convert the input dates into the format required by IMAP
#         start_date_formatted = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date_formatted = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")

#         # Search for emails within the date range
#         res, messages = imap.search(None, f'(SINCE "{start_date_formatted}" BEFORE "{end_date_formatted}")')
        
#         email_ids = messages[0].split()

#         # Pagination calculations
#         total_emails = len(email_ids)
#         start_page = (page - 1) * page_size
#         end_page = min(start_page + page_size, total_emails)

#         # Fetch emails for the current page
#         for num in email_ids[start_page:end_page]:
#             res, msg = imap.fetch(num, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details to the list
#                     fetched_emails.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#         # Include pagination metadata in the response
#         return {
#             "page": page,
#             "page_size": page_size,
#             "total_emails": total_emails,
#             "emails": fetched_emails
#         }

#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



























# @app.get("/imap/filter_by_month")
# def fetch_inbox(month: int = Query(..., description="Month to fetch emails from (1-12)"), 
#                 year: int = Query(..., description="Year to fetch emails from")):
#     fetched_emails = []
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Calculate the start and end date for the selected month
#         first_month = datetime(year, month, 1)
#         if month == 12:
#             first_next_month = datetime(year + 1, 1, 1)
#         else:
#             first_next_month = datetime(year, month + 1, 1)
#         last_month = first_next_month - timedelta(days=1)

#         # Format dates for IMAP search
#         start_date = first_month.strftime("%d-%b-%Y")
#         end_date = last_month.strftime("%d-%b-%Y")                             
                                   
#         # Search for emails within the date range
#         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')

#         # Iterate over the email IDs
#         for num in messages[0].split():
#             res, msg = imap.fetch(num, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details to the list
#                     fetched_emails.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#     except Exception as e:
#         fetched_emails.append({"error": str(e)})

#     return fetched_emails

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
























# # import the modules
# import imaplib                              
# import email
# from email.header import decode_header
# import webbrowser
# import os
 
# # establish connection with Gmail
# server ="imap.gmail.com"                     
# imap = imaplib.IMAP4_SSL(server)
 
# # instantiate the username and the password
# username ="username@gmail.com" 
# password ="********"
 
# # login into the gmail account
# imap.login(username, password)               
 
# # select the e-mails
# res, messages = imap.select('"[Gmail]/Sent Mail"')   
 
# # calculates the total number of sent messages
# messages = int(messages[0])
 
# # determine the number of e-mails to be fetched
# n = 3
 
# # iterating over the e-mails
# for i in range(messages, messages - n, -1):
#     res, msg = imap.fetch(str(i), "(RFC822)")     
#     for response in msg:
#         if isinstance(response, tuple):
#             msg = email.message_from_bytes(response[1])
             
#             # getting the sender's mail id
#             From = msg["From"]
 
#             # getting the subject of the sent mail
#             subject = msg["Subject"]
 
#             # printing the details
#             print("From : ", From)
#             print("subject : ", subject)
















































# # @app.get("/imap/filter_by_date_range")
# # def fetch_inbox(
# #     from_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
# #     to_date: str = Query(..., description="End date in YYYY-MM-DD format")
# # ):
# #     fetched_emails = []
# #     try:
# #         # Connect to the Gmail IMAP server
# #         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

# #         # Log in to the Gmail account
# #         imap.login(IMAP_USER, IMAP_PASSWORD)

# #         # Select the inbox
# #         imap.select("inbox")

# #         # Convert the input dates into the format required by IMAP
# #         start_date_formatted = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
# #         end_date_formatted = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")

# #         # Search for emails within the date range
# #         res, messages = imap.search(None, f'(SINCE "{start_date_formatted}" BEFORE "{end_date_formatted}")')

# #         # Iterate over the email IDs
# #         for num in messages[0].split():
# #             res, msg = imap.fetch(num, "(RFC822)")
# #             for response in msg:
# #                 if isinstance(response, tuple):
# #                     msg = email.message_from_bytes(response[1])

# #                     # Decode the email subject
# #                     subject = msg["Subject"]
# #                     if subject is not None:
# #                         subject, encoding = decode_header(subject)[0]
# #                         if isinstance(subject, bytes):
# #                             subject = subject.decode(encoding if encoding else "utf-8")
# #                     else:
# #                         subject = "(No subject)"

# #                     # Get sender, recipient, and date
# #                     From = msg["From"]
# #                     To = msg["To"]
# #                     date = msg["Date"]

# #                     # Append email details to the list
# #                     fetched_emails.append({
# #                         "from": From,
# #                         "subject": subject,
# #                         "to": To,
# #                         "date": date
# #                     })

# #         # Logout from the server
# #         imap.logout()

# #     except Exception as e:
# #         fetched_emails.append({"error": str(e)})

# #     return fetched_emails

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)







































































# #  # Convert the input date into the required format for IMAP
# #         date_formatted = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%b-%Y")

# #         # Search for emails in the inbox from the specified date
# #         res, messages = imap.search(None, f'(ON "{date_formatted}")')




# # @app.get("/imap/filter_by_month")
# # def fetch_inbox(month: int = Query(..., description="Month to fetch emails from (1-12)"), 
# #                 year: int = Query(..., description="Year to fetch emails from")):
# #     fetched_emails = []
# #     try:
# #         # Connect to the Gmail IMAP server
# #         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

# #         # Log in to the Gmail account
# #         imap.login(IMAP_USER, IMAP_PASSWORD)

# #         # Select the inbox
# #         imap.select("inbox")

# #         # Calculate the start and end date for the selected month
# #         first_month = datetime(year, month, 1)
# #         if month == 12:
# #             first_next_month = datetime(year + 1, 1, 1)
# #         else:
# #             first_next_month = datetime(year, month + 1, 1)
# #         last_month = first_next_month - timedelta(days=1)

# #         # Format dates for IMAP search
# #         start_date = first_month.strftime("%d-%b-%Y")
# #         end_date = last_month.strftime("%d-%b-%Y")

# #         # Search for emails within the date range
# #         res, messages = imap.search(None, f'(SINCE "{start_date}" BEFORE "{end_date}")')

# #         # Iterate over the email IDs
# #         for num in messages[0].split():
# #             res, msg = imap.fetch(num, "(RFC822)")
# #             for response in msg:
# #                 if isinstance(response, tuple):
# #                     msg = email.message_from_bytes(response[1])

# #                     # Decode the email subject
# #                     subject = msg["Subject"]
# #                     if subject is not None:
# #                         subject, encoding = decode_header(subject)[0]
# #                         if isinstance(subject, bytes):
# #                             subject = subject.decode(encoding if encoding else "utf-8")
# #                     else:
# #                         subject = "(No subject)"

# #                     # Get sender, recipient, and date
# #                     From = msg["From"]
# #                     To = msg["To"]
# #                     date = msg["Date"]

# #                     # Append email details to the list
# #                     fetched_emails.append({
# #                         "from": From,
# #                         "subject": subject,
# #                         "to": To,
# #                         "date": date
# #                     })

# #         # Logout from the server
# #         imap.logout()

# #     except Exception as e:
# #         fetched_emails.append({"error": str(e)})

# #     return fetched_emails

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)
















































































# # Function to fetch the most recent 5 emails from "Sent Mail" within the last 24 hours
# def fetch_inbox():
#     fetched_emails = []
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the "Sent Mail" folder
#         imap.select('"[Gmail]/Sent Mail"')

#         # Get the date 24 hours ago
#         date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

#         # Search for emails in "Sent Mail" that are newer than 24 hours
#         res, messages = imap.search(None, f'(SINCE "{date}")')

#         # Iterate over the email IDs
#         for num in messages[0].split():
#             res, msg = imap.fetch(num, "(RFC822)")
#             for response in msg:
#                 if isinstance(response, tuple):
#                     msg = email.message_from_bytes(response[1])

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details to the list
#                     fetched_emails.append({
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#     except Exception as e:
#         fetched_emails.append({"error": str(e)})

#     return fetched_emails


# import concurrent.futures
# import asyncio
# @app.get("/imap")
# async def fetch_inbox_and_sent():
#     loop = asyncio.get_event_loop()

#     # Run the blocking functions in a thread pool for both inbox and "Sent Mail"
#     with concurrent.futures.ThreadPoolExecutor() as pool:
#         inbox_emails = await loop.run_in_executor(pool, fetch_inbox)
#         sent_emails = await loop.run_in_executor(pool, fetch_inbox)

#     # Combine the results from both inbox and "Sent Mail"
#     return {
#         "inbox_emails": inbox_emails,
#         "sent_emails": sent_emails
#     }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)






















































# from fastapi import FastAPI, Query
# import imaplib
# import email
# from email.header import decode_header
# from datetime import datetime

# app = FastAPI()

# IMAP_HOST = 'imap.gmail.com'
# IMAP_PORT = 993
# IMAP_USER = 'your_email@gmail.com'
# IMAP_PASSWORD = 'your_password'

# @app.get("/imap/filter_by_date_range")
# def fetch_inbox(
#     from_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
#     to_date: str = Query(..., description="End date in YYYY-MM-DD format"),
#     page: int = Query(1, description="Page number"),
#     page_size: int = Query(10, description="Number of emails per page")
# ):
#     fetched_emails = []
#     try:
#         # Connect to the Gmail IMAP server
#         imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#         # Log in to the Gmail account
#         imap.login(IMAP_USER, IMAP_PASSWORD)

#         # Select the inbox
#         imap.select("inbox")

#         # Convert the input dates into the format required by IMAP
#         start_date_formatted = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y")
#         end_date_formatted = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y")

#         # Search for emails within the date range
#         res, messages = imap.search(None, f'(SINCE "{start_date_formatted}" BEFORE "{end_date_formatted}")')
        
#         email_ids = messages[0].split()

#         # Pagination calculations
#         total_emails = len(email_ids)
#         start_index = (page - 1) * page_size
#         end_index = min(start_index + page_size, total_emails)

#         # Fetch emails for the current page
#         for num in email_ids[start_index:end_index]:
#             # Fetch both the RFC822 message and the UID
#             res, msg_data = imap.fetch(num, "(RFC822 UID)")
#             uid = None

#             for response_part in msg_data:
#                 if isinstance(response_part, tuple):
#                     msg = email.message_from_bytes(response_part[1])

#                     # Get the UID from the response
#                     uid_response = msg_data[0].decode()
#                     uid = uid_response.split()[2]  # Extract UID from response

#                     # Decode the email subject
#                     subject = msg["Subject"]
#                     if subject is not None:
#                         subject, encoding = decode_header(subject)[0]
#                         if isinstance(subject, bytes):
#                             subject = subject.decode(encoding if encoding else "utf-8")
#                     else:
#                         subject = "(No subject)"

#                     # Get sender, recipient, and date
#                     From = msg["From"]
#                     To = msg["To"]
#                     date = msg["Date"]

#                     # Append email details and UID to the list
#                     fetched_emails.append({
#                         "uid": uid,
#                         "from": From,
#                         "subject": subject,
#                         "to": To,
#                         "date": date
#                     })

#         # Logout from the server
#         imap.logout()

#         # Include pagination metadata in the response
#         return {
#             "page": page,
#             "page_size": page_size,
#             "total_emails": total_emails,
#             "emails": fetched_emails
#         }

#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
















































# @app.get("/imap")
# def fetch_inbox():

#     # Connect to the Gmail IMAP server                    
#     imap = imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)

#     # login into the gmail account
#     imap.login(IMAP_USER, IMAP_PASSWORD)               

#     # Select the mailbox you want to check (inbox)
#     imap.select("inbox")

#     # select the e-mails
#     res, messages = imap.select('"[Gmail]/Sent Mail"')   

#     # calculates the total number of sent messages
#     messages = int(messages[0])

#     # determine the number of e-mails to be fetched
#     n = 1
    
#     # iterating over the e-mailss
#     for i in range(messages, messages - n, -1):
#         res, msg = imap.fetch(str(i), "(RFC822)")     
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg = email.message_from_bytes(response[1])

#                 # Decode the email subject
#                 subject, encoding = decode_header(msg["Subject"])[0]
#                 if isinstance(subject, bytes):
#                     # If it's a bytes object, decode to string
#                     subject = subject.decode(encoding if encoding else "utf-8") 

#                 # getting the sender's mail id
#                 From = msg["From"]

#                 # getting the subject of the sent mail
#                 subject = msg["Subject"]

#                 #getting the reciver's mail id
#                 To = msg["To"]

#                 # printing the details
#                 return {"from":From,
#                         "subject ": subject 
#                         ,"to":To
#                         #,"to":EmailMessage.msg
#                         # "to":EmailSchema.mail_id
#                         }
#                 # return{"subject ": subject}
#                 # print("="*100)
#     # Logout from the server
#     imap.logout()

# if __name__ == "__main__":
#     fetch_inbox()




# @app.get("/imap")
# async def fetch_inbox():
#     # Connect to the Gmail IMAP server                    
#     imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)

#     # login into the gmail account
#     imap.login(IMAP_USER, IMAP_PASSWORD)               


#     # Select the mailbox you want to check (inbox)
#     imap.select("inbox")

#     # Get the date and time
#     date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
  


#     # Search for emails in "Sent Mail" that are newer than 24 hours
#     res, messages = imap.search(None, f'(SINCE "{date}")')
#     # res, messages = imap.select('"[Gmail]/Sent Mail"')
#     # res, messages = imap.search(None,"All")
                                
#     # Convert messages to a list of email IDs
#     fetched_emails = []
#     # fetched_emails = int(messages[0])  
#     # determine the number of e-mails to be fetched   
#     # n=100
#     # fetched_emails= messages[0].split()

#     # Iterate over the email IDs
#     # for i in range(messages, messages - n, -1):
#     #     res, msg = imap.fetch(str(i), "(RFC822)") 
#     # for i in range(messages, messages - n, -1):
#     for num in messages[0].split():
#         res, msg = imap.fetch(num, "(RFC822)")
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg = email.message_from_bytes(response[1])

#                 # Decode the email subject
#                 subject = msg["Subject"]
#                 if subject is not None:
#                     subject, encoding = decode_header(subject)[0]
#                     if isinstance(subject, bytes):
#                         # If it's a bytes object, decode to string
#                         subject = subject.decode(encoding if encoding else "utf-8")
#                 else:
#                     subject = "(No subject)"

#                 # # Decode the email subject
#                 # subject, encoding = decode_header(msg["Subject"])[0]
#                 # if isinstance(subject, bytes):
#                 #     # If it's a bytes object, decode to string
#                 #     subject = subject.decode(encoding if encoding else "utf-8")

#                 # getting the sender's mail id
#                 From = msg["From"]

#                 # # getting the subject of the sent mail
#                 # subject = msg["Subject"]

#                 # getting the recipient's mail id
#                 To = msg["To"]

#                 # Get the date
#                 date = msg["Date"]

#                 # Store the fetched email details
#                 fetched_emails.append({
#                     "from": From,
#                     "subject": subject, 
#                     "to": To,
#                     "date":date
                   
#                 })

    
#     # Logout from the server
#     imap.logout()

#     # Return the fetched emails
#     return fetched_emails

# if __name__ == "__main__":
#     fetch_inbox()
#     # import uvicorn
#     # uvicorn.run(app, host="0.0.0.0", port=8000)













































































































# #Fetch all emails from Gmail inbox


# @app.get("/imap")
# def fetch_inbox():
#     # Connect to the Gmail IMAP server
#     imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    
#     # Login to the Gmail account
#     imap.login(IMAP_USER, IMAP_PASSWORD)
    
#     # Select the mailbox you want to check (inbox)
#     imap.select("INBOX")
    
#     # Search for all emails in the inbox
#     _, message_numbers = imap.search(None, "ALL")
    
#     email_data = []
    
#     # Iterate through all email IDs
#     for num in message_numbers[0].split():
#         _, msg_data = imap.fetch(num, "(RFC822)")
        
#         for response_part in msg_data:
#             if isinstance(response_part, tuple):
#                 msg = email.message_from_bytes(response_part[1])
                
#                 # Decode the email subject
#                 subject, encoding = decode_header(msg["Subject"])[0]
#                 if isinstance(subject, bytes):
#                      # If it's a bytes object, decode to string
#                     subject = subject.decode(encoding if encoding else "utf-8")
                
#                 # Get sender's email
#                 from_email = msg["From"]
                
#                 # Get receiver's email
#                 to_email = msg["To"]
                
#                 # Append email data to the list
#                 email_data.append({
#                     "from": from_email,
#                     "to": to_email,
#                     "subject": subject,
                    
#                 })
    
#     # Logout from the server
#     imap.logout()
    
#     return {"emails": email_data}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


























































































































































































# @app.get("/imap")
# def fetch_inbox():

#     # Connect to the Gmail IMAP server                    
#     imap = imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)

#     # login into the gmail account
#     imap.login(IMAP_USER, IMAP_PASSWORD)               

#     # Select the mailbox you want to check (inbox)
#     imap.select("inbox")

#     # select the e-mails
#     res, messages = imap.select('"[Gmail]/Sent Mail"')   

#     # calculates the total number of sent messages
#     messages = int(messages[0])

#     # determine the number of e-mails to be fetched
#     n = 1
    
#     # iterating over the e-mailss
#     for i in range(messages, messages - n, -1):
#         res, msg = imap.fetch(str(i), "(RFC822)")     
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg = email.message_from_bytes(response[1])

#                 # Decode the email subject
#                 subject, encoding = decode_header(msg["Subject"])[0]
#                 if isinstance(subject, bytes):
#                     # If it's a bytes object, decode to string
#                     subject = subject.decode(encoding if encoding else "utf-8") 

#                 # getting the sender's mail id
#                 From = msg["From"]

#                 # getting the subject of the sent mail
#                 subject = msg["Subject"]

#                 #getting the reciver's mail id
#                 To = msg["To"]

#                 # printing the details
#                 return {"from":From,
#                         "subject ": subject 
#                         ,"to":To
#                         #,"to":EmailMessage.msg
#                         # "to":EmailSchema.mail_id
#                         }
#                 # return{"subject ": subject}
#                 # print("="*100)
#     # Logout from the server
#     imap.logout()

# if __name__ == "__main__":
#     fetch_inbox()































# def fetch_inbox():
#     # Connect to the Gmail IMAP server
#     mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    
#     # Login to the Gmail account
#     mail.login(IMAP_USER, IMAP_PASSWORD)

#     # Select the mailbox you want to check (inbox)
#     mail.select("inbox")

#     # Search for all emails in the inbox
#     status, messages = mail.search(None, "ALL")

#     # Convert messages to a list of email IDs
#     email_ids = messages[0].split()

#     for email_id in email_ids:
#         # Fetch the email by ID
#         status, msg_data = mail.fetch(email_id, "(RFC822)")

#         for response_part in msg_data:
#             if isinstance(response_part, tuple):
#                 msg = email.message_from_bytes(response_part[1])

#                 # Decode the email subject
#                 subject, encoding = decode_header(msg["Subject"])[0]
#                 if isinstance(subject, bytes):
#                     # If it's a bytes object, decode to string
#                     subject = subject.decode(encoding if encoding else "utf-8")

#                 # Decode email sender
#                 from_ = msg.get("From")

#                 print("Subject:", subject)
#                 print("From:", from_)
#                 print("="*100)

#     # Logout from the server
#     mail.logout()

# if __name__ == "__main__":
#     fetch_inbox()




































































































































































# logging.basicConfig(level=logging.INFO)
# async def primary_inbox(db: AsyncSession):
#     client = aioimaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    
#     try:
#         await client.wait_hello_from_server()
#         logging.info("Connected to IMAP server.")
#         await client.login(IMAP_USER, IMAP_PASSWORD)
#         logging.info("Logged in to the email account.")

#         await client.select("INBOX")

#         search_criteria = 'X-GM-RAW "category:primary"'
#         response = await client.search(search_criteria)
        
#         if response.result == 'OK':                                                                                                                                                                                                                                         
#             logging.info(f"Emails found in Primary: {response.lines}")
#             for num in response.lines[0].split():
#                 _, msg_data = await client.fetch(num, '(RFC822)')
#                 msg = msg_data[0].payload
#                 logging.info(f"Email headers: {msg['header']}")
                
#                 if 'In-Reply-To' in msg['header'] or 'References' in msg['header']:
#                     reply_id = msg['header'].get('In-Reply-To') or msg['header'].get('References')
#                     unique_id = extract_unique_id_from_reply(reply_id)
#                     logging.info(f"Extracted unique_id: {unique_id}")
                    
#                     if unique_id:
#                         async with db.begin():
#                             result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
#                             email_data = result.scalars().first()
#                             logging.info(f"Database result: {email_data}")
                            
#                             if email_data and email_data.status in ["sent", "clicked"]:
#                                 email_data.status = "replied"
#                                 await db.commit()
#                                 await db.refresh(email_data)
#                                 logging.info(f"Updated email status to 'replied' for unique_id: {unique_id}")

#         else:
#             logging.warning("No emails found in the Primary category.")
    
#     except Exception as e:
#         logging.error(f"Error accessing Primary inbox: {e}")
#     finally:
#         await client.logout()

# def extract_unique_id_from_reply(reply_id: str) -> str:
#     # Check if In-Reply-To or References contains more than one ID and handle it
#     if not reply_id:
#         return None
    
#     # Some email clients may include multiple references, split and check each
#     ids = reply_id.split()
#     for id_ in ids:
#         if '@' in id_:
#             unique_id = id_.split('@')[0]
#             return unique_id
#     return None


























# async def primary_inbox():
#     client = aioimaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    
#     try:
#         await client.wait_hello_from_server()
#         logging.info("Connected to IMAP server.")

#         await client.login(IMAP_USER, IMAP_PASSWORD)
#         logging.info("Logged in to the email account.")

#         # Select the mailbox (INBOX by default)
#         await client.select("INBOX")

#         # Search for emails in the "Primary" category
#         # Gmail uses specific labels for this: 'CATEGORY_PRIMARY'
#         search_criteria = 'X-GM-RAW "category:primary"'
#         response = await client.search(search_criteria)
        
#         if response.result == 'OK':                                                                                                                                                                                                                                         
#             logging.info(f"Emails found in Primary: {response.lines}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
#             for num in response.lines[0].split():
#                 _, msg_data = await client.fetch(num, '(RFC822)')
#                 logging.info(f"Email {num} data: {msg_data[0].payload}")
        
#         else:
#             logging.warning("No emails found in the Primary category.")
    
#     except Exception as e:
#         logging.error(f"Error accessing Primary inbox: {e}")
#     finally:
#         await client.logout()

# # To run the asyncio event loop
# if __name__ == "__main__":
#     asyncio.run(primary_inbox())

















































































































































# async def check_for_replies():
#     while True:
#         try:
#             logging.info("Checking for replies...")
#             mail = imaplib.IMAP4_SSL('imap.gmail.com')
#             mail.login("mailerbycodetru@gmail.com", "swdj ioui sjdy yawg")
#             mail.select('inbox')

#             async with get_db() as db_session:  # Properly managing the database session
#                 result = await db_session.execute(select(EmailLinked).where(EmailLinked.status != "replied"))
#                 sent_emails = result.scalars().all()
#                 sent_email_addresses = {email.mail_id: email for email in sent_emails}

#                 status, messages = mail.search(None, 'UNSEEN')
#                 message_ids = messages[0].split()

#                 for msg_id in message_ids:
#                     status, msg_data = mail.fetch(msg_id, '(RFC822)')
#                     raw_email = msg_data[0][1]
#                     email_message = email.message_from_bytes(raw_email)
                   
#                     from_address = email.utils.parseaddr(email_message['From'])[1]
                   
#                     if from_address in sent_email_addresses:
#                         original_email = sent_email_addresses[from_address]
#                         original_email.status = "replied"
#                         await db_session.commit()
#                         await db_session.refresh(original_email)
#                         logging.info(f"Email {original_email.generated_id} status updated to 'replied'")

#             mail.close()
#             mail.logout()
#             logging.info("Finished checking for replies.")

#         except Exception as e:
#             logging.error(f"Failed to check for replies: {e}")

#         await asyncio.sleep(300)  # Sleep for 5 minutes

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)












# Background task to check for email replies
# Background task to check for email replies
# async def check_for_replies():
#     imap_host = "imap.gmail.com"
#     imap_user = "posinapraveen2002@gmail.com"
#     imap_password = "ihlz tjgz cwqm ekro"

#     while True:
#             # Connect to the IMAP server
#             imap_client = aioimaplib.IMAP4_SSL(imap_host)
#             await imap_client.wait_hello_from_server()
#             await imap_client.login(imap_user, imap_password)
#             await imap_client.select('INBOX')

































































































#             # Search for emails that are replies
#             search_criteria = 'SUBJECT "RE:"'
#             search_result = await imap_client.search([search_criteria])
            
#             if search_result.result == 'OK':
#                 for msg_id in search_result.lines[0].split():
#                     # Fetch the email and process it
#                     fetch_result = await imap_client.fetch(msg_id, 'RFC822')
#                     if fetch_result.result == 'OK':
#                         email_data = fetch_result.lines[1]  # Assuming the email content is in the second line
#                         unique_id = parse_unique_id_from_email(email_data)
#                         if unique_id:
#                             async with get_db() as db:
#                                 result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
#                                 email_record = result.scalars().first()
#                                 if email_record and email_record.status != 'replied':
#                                     email_record.status = 'replied'
#                                     await db.commit()
#                                     await db.refresh(email_record)
#                                     logging.info(f"Updated email status to 'replied' for {unique_id}")

#             await imap_client.logout()
#         except Exception as e:
#             logging.error(f"Error checking for replies: {e}")
        
#         # Sleep for a while before checking again
#         await asyncio.sleep(300)  # Check every 5 minutes

# def parse_unique_id_from_email(email_data):
#     # Implement your logic here to extract the unique ID from the email
#     # For example, you could extract it from the email subject or body
#     return "some_unique_id_extracted_from_email"



















###############################################______________failed_______________#######################################################################################################################################################################



# import logging
# import uuid
# from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status
# from fastapi.responses import RedirectResponse
# from email.message import EmailMessage
# import aiosmtplib
# import aioimaplib
# import asyncio
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from pydantic import BaseModel, EmailStr
# from database import get_db #engine
# from models import EmailLinked

# app = FastAPI()

# logging.basicConfig(level=logging.WARNING)

# # Pydantic schemas
# class CreateEmailLinkedSchema(BaseModel):
#     generated_id: str
#     status: str
#     user_id: str
#     mail_id: EmailStr
#     message: str
#     subject: str
#     actual_link: str

# class EmailSchema(BaseModel):
#     mail_id: EmailStr
#     subject: str

# @app.on_event("startup")
# async def on_startup():
#     from database import create_tables
#     await create_tables()
#     #asyncio.create_task(check_for_replies())  # Start the background task to check for replies

# async def send_email(email_data: EmailSchema, db: AsyncSession):
#     smtp_host = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_user = "posinapraveen2002@gmail.com"
#     smtp_password = "ihlz tjgz cwqm ekro"

#     msg = EmailMessage()
#     msg["From"] = smtp_user
#     msg["To"] = email_data.mail_id
#     msg["Subject"] = email_data.subject
#     msg.set_content("This is the email content.")

#     unique_id = str(uuid.uuid4())

#     html_message = f"""
#     <html>
#     <body>
#         <p>History, Purpose and Usage</p>
#         <a href='http://127.0.0.1:8000/click-link?link={unique_id}'>Click me</a>
#         <p>Best regards,<br>Your Company</p>
#         <img src='http://127.0.0.1:8000/track-email/{unique_id}' alt="" style="display:none;"/>
#     </body>
#     </html>
#     """

#     msg.add_alternative(html_message, subtype='html')

#     try:
#         await aiosmtplib.send(
#             msg,
#             hostname=smtp_host,
#             port=smtp_port,
#             start_tls=True,
#             username=smtp_user,
#             password=smtp_password
#         )
        
#         logging.info(f"Email sent to {email_data.mail_id}")

#         new_click = CreateEmailLinkedSchema(
#             generated_id=unique_id,
#             status="sent",
#             user_id='11',
#             mail_id=email_data.mail_id,
#             message=html_message,
#             subject=email_data.subject,
#             actual_link=f'https://www.codetru.com'
#         )
#         new_db_click = EmailLinked(**new_click.dict())
#         db.add(new_db_click)
#         await db.commit()
#         await db.refresh(new_db_click)
#         logging.info(f"Stored email data into database: {new_db_click}")
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email sending failed")

# @app.post("/send-email/")
# async def send_email_endpoint(email_data: EmailSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
#     background_tasks.add_task(send_email, email_data, db)
#     return {"message": "Email has been sent"}

# @app.get("/track-email/{unique_id}")
# async def track_email(unique_id: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status == "sent":
#                 email_data.status = "opened"
#                 await db.commit()
#                 await db.refresh(email_data)
#             return "Email opened"
#         return "Email not opened"
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @app.get("/click-link")
# async def click_link(link: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == link))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status in ["opened", "sent"]:
#                 email_data.status = "clicked"
#                 await db.commit()
#                 await db.refresh(email_data)
#         return RedirectResponse(url=email_data.actual_link)
#     except Exception as e:
#         logging.error(f"Error handling link click: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



# async def check_for_replies():
#     imap_host = "imap.outlook.com"
#     imap_user = "posinapraveen2002@gmail.com"
#     imap_password = "ihlz tjgz cwqm ekro"

#     client = aioimaplib.IMAP4_SSL(imap_host)


#     try:
#         await client.wait_hello_from_server()
#         await client.login(imap_user, imap_password)
#         await client.select("INBOX")

#         while True:
#             # Search for emails with the "REPLIED" flag or containing "In-Reply-To" headers
#             _, messages = await client.search('(UNSEEN)')

#             if messages:
#                 for msg_id in messages[0].split():
#                     _, msg_data = await client.fetch(msg_id, "(BODY[HEADER])")
#                     raw_email = msg_data[0][1].decode('utf-8')

#                     # Extract the In-Reply-To header and match with your unique_id
#                     if "In-Reply-To" in raw_email:
#                         in_reply_to = extract_message_id(raw_email)  # Implement this function to extract Message-ID
#                         await update_status_to_replied(in_reply_to)

#             await asyncio.sleep(60)  # Check for new replies every minute

#     except Exception as e:
#         logging.error(f"Failed to check for replies: {e}")
#     finally:
#         await client.logout()

# async def update_status_to_replied(message_id: str):
#     async with AsyncSession() as session:
#         try:
#             result = await session.execute(select(EmailLinked).where(EmailLinked.generated_id == message_id))
#             email_data = result.scalars().first()
#             #if email_data and email_data.status not in ["replied"]:
#             if email_data in["clicked","repiled","opened","sent"]:
#                 email_data.status = "replied"
#                 await session.commit()
#                 logging.info(f"Updated email status to replied for ID: {message_id}")
#         except Exception as e:
#             logging.error(f"Failed to update status to replied: {e}")

# def extract_message_id(raw_email: str) -> str:
#     # Function to extract 'In-Reply-To' or 'Message-ID' from email headers
#     import re
#     match = re.search(r"In-Reply-To:\s*<(.+?)>", raw_email)
#     return match.group(1) if match else None








####################################################_________________Failed_____________################################################################################################################################################################################################











# import logging
# import uuid
# from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, status
# from fastapi.responses import RedirectResponse
# from email.message import EmailMessage
# import aiosmtplib
# import aioimaplib
# import asyncio
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from pydantic import BaseModel, EmailStr
# from database import get_db
# from models import EmailLinked

# app = FastAPI()

# logging.basicConfig(level=logging.WARNING)

# # Pydantic schemas
# class CreateEmailLinkedSchema(BaseModel):
#     generated_id: str
#     status: str
#     user_id: str
#     mail_id: EmailStr
#     message: str
#     subject: str
#     actual_link: str

# class EmailSchema(BaseModel):
#     mail_id: EmailStr
#     subject: str

# @app.on_event("startup")
# async def on_startup():
#     from database import create_tables
#     await create_tables()
#     # Start the background task to check for replies
#     asyncio.create_task(check_for_replies())

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# async def send_email(email_data: EmailSchema, db: AsyncSession):
#     smtp_host = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_user = "posinapraveen2002@gmail.com"
#     smtp_password = "ihlz tjgz cwqm ekro"

#     msg = EmailMessage()
#     msg["From"] = smtp_user
#     msg["To"] = email_data.mail_id
#     msg["Subject"] = email_data.subject
#     msg.set_content("This is the email content.") 

#     unique_id = str(uuid.uuid4())
#     html_message = f"""
#     <html>
#     <body>
#         <p>History, Purpose and Usage</p>
#         <a href='http://127.0.0.1:8000/click-link?link={unique_id}'>Click me</a>
#         <p>Best regards,<br>Your Company</p>
#         <img src='http://127.0.0.1:8000/track-email/{unique_id}' alt="" style="display:none;"/>
#     </body>
#     </html>
#     """

#     msg.add_alternative(html_message, subtype='html')

#     try:
#         await aiosmtplib.send(
#             msg,
#             hostname=smtp_host,
#             port=smtp_port,
#             start_tls=True,
#             username=smtp_user,
#             password=smtp_password
#         )
        
#         logging.info(f"Email sent to {email_data.mail_id}")

#         new_click = CreateEmailLinkedSchema(
#             generated_id=unique_id,
#             status="sent",
#             user_id='11',
#             mail_id=email_data.mail_id,
#             message=html_message,
#             subject=email_data.subject,
#             actual_link=f'https://www.codetru.com'
#         )
#         new_db_click = EmailLinked(**new_click.dict())
#         db.add(new_db_click)
#         await db.commit()
#         await db.refresh(new_db_click)
#         logging.info(f"Stored email data into database: {new_db_click}")
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email sending failed")

# @app.post("/send-email/")
# async def send_email_endpoint(email_data: EmailSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
#     background_tasks.add_task(send_email, email_data, db)
#     return {"message": "Email has been sent"}

# @app.get("/track-email/{unique_id}")
# async def track_email(unique_id: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == unique_id))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status == "sent":
#                 email_data.status = "opened"
#                 await db.commit()
#                 await db.refresh(email_data)
#             return "Email opened"
#         return "Email not opened"
    
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @app.get("/click-link")
# async def click_link(link: str, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(EmailLinked).where(EmailLinked.generated_id == link))
#         email_data = result.scalars().first()
#         if email_data:
#             if email_data.status in ["opened", "sent"]:
#                 email_data.status = "clicked"
#                 await db.commit()
#                 await db.refresh(email_data)
#         return RedirectResponse(url=email_data.actual_link)
#     except Exception as e:
#         logging.error(f"Error handling link click: {e}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# async def check_for_replies():
#     imap_host = "imap.gmail.com"
#     imap_port = 993
#     imap_user = "your-email@gmail.com"
#     imap_password = "your-email-password"

#     client = aioimaplib.IMAP4_SSL(imap_host, port=imap_port)

#     try:
#         await client.wait_hello_from_server()  # Ensure connection is established
#         await client.login(imap_user, imap_password)
#         await client.select('INBOX')

#         while True:
#             try:
#                 response = await client.search('UNSEEN')  # Adjust the search criteria as needed
#                 if response:
#                     msg_ids = response.lines[0].split()
#                     for msg_id in msg_ids:
#                         fetch_result = await client.fetch(msg_id, '(RFC822)')
#                         message_data = fetch_result.lines[0]  # Correctly access the message content
                        
#                         # Parse the email message here to get the subject or other identifying info
#                         subject = parse_subject(message_data)  # You will need to implement parse_subject
                        
#                         # Properly use a new DB session
#                         async with get_db() as db:
#                             result = await db.execute(select(EmailLinked).where(EmailLinked.subject == subject))
#                             email_data = result.scalars().first()
#                             if email_data:
#                                 email_data.status = "replied"
#                                 await db.commit()
#                                 await db.refresh(email_data)
#                                 logging.info(f"Updated email status to 'replied' for ID {email_data.generated_id}")

#                 await asyncio.sleep(60 * 5)  # Check every 5 minutes

#             except Exception as e:
#                 logging.error(f"Failed during replies check: {e}")
#                 # Reconnect if needed
#                 try:
#                     await client.logout()
#                 except Exception:
#                     logging.error("Failed to log out. Reconnecting...")
#                 client = aioimaplib.IMAP4_SSL(imap_host, port=imap_port)
#                 await client.wait_hello_from_server()
#                 await client.login(imap_user, imap_password)
#                 await client.select('INBOX')

#     except Exception as e:
#         logging.error(f"Failed to initialize IMAP connection or during login: {e}")

#     finally:
#         try:
#             await client.logout()
#         except Exception as e:
#             logging.error(f"Error during IMAP client logout: {e}")

# def parse_subject(message_data):
#     # Parse the message_data to extract the subject
#     # This is a placeholder function; implement parsing logic here
#     import email
#     msg = email.message_from_bytes(message_data)
#     return msg['subject']

# # async def check_for_replies():
# #     imap_host = "imap.gmail.com"
# #     imap_port = 993
# #     imap_user = "posinapraveen2002@gmail.com"
# #     imap_password = "ihlz tjgz cwqm ekro"

# #     client = aioimaplib.IMAP4_SSL(imap_host, port=imap_port)

# #     try:
# #         await client.wait_hello_from_server()  # Ensure connection is established
# #         await client.login(imap_user, imap_password)
# #         await client.select('INBOX')

# #         while True:
# #             try:
# #                 response = await client.search('UNSEEN')  # Adjust the search criteria as needed
# #                 if response:
# #                     msg_ids = response.lines[0].split()
# #                     for msg_id in msg_ids:
# #                         fetch_result = await client.fetch(msg_id, '(RFC822)')
# #                         message_data = fetch_result.lines[0]  # Correctly access the message content
                        
# #                         # Parse the email message here to get the subject or other identifying info
# #                         subject = parse_subject(message_data)  # You will need to implement parse_subject
                        
# #                         # Assuming the subject contains the unique_id or another way to link the reply to the original email
# #                         db:AsyncSession=Depends(get_db)
# #                         result = await db.execute(select(EmailLinked).where(EmailLinked.subject == subject))
# #                         email_data = result.scalars().first()
# #                         if email_data:
# #                             email_data.status = "replied"
# #                             await db.commit()
# #                             await db.refresh(email_data)
# #                             logging.info(f"Updated email status to 'replied' for ID {email_data.generated_id}")

# #                 await asyncio.sleep(60 * 5)  # Check every 5 minutes

# #             except Exception as e:
# #                 logging.error(f"Failed during replies check: {e}")
# #                 # Reconnect if needed
# #                 try:
# #                     await client.logout()
# #                 except Exception:
# #                     logging.error("Failed to log out. Reconnecting...")
# #                 client = aioimaplib.IMAP4_SSL(imap_host, port=imap_port)
# #                 await client.wait_hello_from_server()
# #                 await client.login(imap_user, imap_password)
# #                 await client.select('INBOX')

# #     except Exception as e:
# #         logging.error(f"Failed to initialize IMAP connection or during login: {e}")

# #     finally:
# #         try:
# #             await client.logout()
# #         except Exception as e:
# #             logging.error(f"Error during IMAP client logout: {e}")

# # def parse_subject(message_data):
# #     # Parse the message_data to extract the subject
# #     # This is a placeholder function; implement parsing logic here
# #     import email
# #     msg = email.message_from_bytes(message_data)
# #     return msg['subject']
