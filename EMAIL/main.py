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
    smtp_user = "Your-Email"
    smtp_password = "Your-Password"

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
IMAP_USER = 'Your-Email'
IMAP_PASSWORD = 'Your-Password' 




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








@app.delete("/Imap/Delete_email_subject")
async def delete_email(subject: str = Query(description="enter the subject of emails you want to delete")):
    try:
        with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) as imap:
            imap.login(IMAP_USER, IMAP_PASSWORD)
            imap.select("INBOX")
            
            # Search for emails with the given subject
            res, messages = imap.search(None, f'SUBJECT "{subject}"')
            
            if not messages[0]:
                return {"status": "info", "message": f"No emails found with subject: {subject}"}
            
            deleted_count = 0
            for i in messages[0].split():
                # Fetch the email details
                res, msg_data = imap.fetch(i, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        email_body = email.message_from_bytes(response_part[1])
                        email_subject = decode_header(email_body["subject"])[0][0]
                        if isinstance(email_subject, bytes):
                            email_subject = email_subject.decode()
                        
                        # Double-check if the subject matches (case-insensitive)
                        if subject.lower() in email_subject.lower():
                            # Mark the email for deletion
                            imap.store(i, "+FLAGS", "\\Deleted")
                            deleted_count += 1
            
            # Expunge to actually delete the marked emails
            imap.expunge()
            imap.logout()
            
            return {
                "status": "success",
                "message": f"Deleted {deleted_count} email(s) with subject containing: {subject}",
            }


    except Exception as e:
        return {'error': str(e)}
    
  





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






    


@app.delete("/Imap/Delete_email_through_email_id_&_sibject")
async def delete_email(email_id: str = Query(description="enter the email_id that you want to delete"),
                       subject: str = Query(description="enter the subject of the email tat you want to delete ")
                       ):
    try:
        imap= imaplib.IMAP4_SSL(IMAP_HOST,IMAP_PORT)
        imap.login(IMAP_USER,IMAP_PASSWORD)

        imap.select('Inbox')

        res, messages=imap.search((None,f'FROM"{email_id}"'),(None,f'SUBJECT"{subject}"'))

        if not messages[0]:
            return {"status": "info", "message": f"No emails found with subject: {subject}"}
            
        
        deleted_count = 0
        for i in messages[0].split():
            # Fetch the email details
            res, msg_data = imap.fetch(i, "(RFC822)")
            for response_part in msg_data:

                if isinstance(response_part, tuple):
                    email_body = email.message_from_bytes(response_part[1])

                    email_subject = decode_header(email_body["subject"])[0][0]
                    if isinstance(email_subject, bytes):
                        email_subject = email_subject.decode()
                            
                         # Double-check if the subject matches (case-insensitive)
                        if subject.lower() in email_subject.lower():
                            # Mark the email for deletion
                            imap.store(i, "+FLAGS", "\\Deleted")
                            deleted_count += 1
                
                # Expunge to actually delete the marked emails
            imap.expunge()
            imap.logout()
            
            return {
                "status": "success",
                "message": f"Deleted {deleted_count} email_id: {email_id} with subject containing: {subject}",
                }
        


    except Exception as e:
        return {"error ": str(e)}    


