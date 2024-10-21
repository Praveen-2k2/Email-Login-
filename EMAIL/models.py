# from sqlalchemy import Column, Integer, String, Boolean
# from database import Base

# class Email(Base):
#     __tablename__ = "EMAIL"
#     id = Column(Integer, primary_key=True, index=True)  
#     recipient=Column(String,index=True)


# from sqlalchemy import Column, String, Boolean
# from database import Base
# import uuid


# class EmailModel(Base):
#     __tablename__ = "emails"

#     tracking_id = Column(String, primary_key=True, index=True)
#     status = Column(Boolean, default=False)
#     user_id = Column(String)
#     mail_id = Column(String)
#     message = Column(String)
#     subject = Column(String)
#     actual_link = Column(String)

# from sqlalchemy import Column, Integer, Boolean
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from database import Base

# class email_schema(Base):
#     __tablename__ = "links"

#     id = Column(Integer, primary_key=True, index=True)
#     is_opened = Column(Boolean, default=False)

# async def update_link_status(session: AsyncSession, link_id: int, status: bool):
#     result = await session.execute(select(email_schema).where(email_schema.id == link_id))
#     link = result.scalars().first()
#     if link:
#         link.is_opened = status
#         await session.commit()

#####################________________________TRACKING MAIL LINK______________________________________##########################################################
# from sqlalchemy import Column, String, Boolean, Integer, Text
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class EmailsClicked(Base):
#     __tablename__ = 'emails_clicked'

#     id = Column(Integer, primary_key=True, index=True)
#     generated_id = Column(String, unique=True, index=True, nullable=False)
#     status = Column(Boolean, default=False)
#     recipient=Column(String,index=True)
#     body=Column(String,index=True)
#     user_id = Column(String, nullable=False)
#     mail_id = Column(String, nullable=False)
#     message = Column(Text, nullable=False)
#     subject = Column(String, nullable=False)
#     actual_link = Column(String, nullable=False)

    

#################################################################____________tracking link and email status_____________######################################################################################

# from sqlalchemy import Column, String
# # from sqlalchemy.orm import relationship
# from database import Base

# # Define the EmailLinked model
# class EmailLinked(Base):
#     __tablename__ = "email_click_1"

#     generated_id = Column(String, primary_key=True, index=True)
#     status = Column(String, nullable=False,default="sent")
#     # link_status = Column(String, nullable=False,default="link not opened")
#     user_id = Column(String, nullable=False)
#     mail_id = Column(String, nullable=False)
#     message = Column(String, nullable=False)
#     subject = Column(String, nullable=False)
#     actual_link = Column(String, nullable=False)








####################################################################################################################################################################################################
















from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship
from database import Base

# Define the EmailLinked model
class EmailLinked(Base):
    __tablename__ = "email_status"

    generated_id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False,default="sent")
    # link_status = Column(String, nullable=False,default="link not opened")
    user_id = Column(String, nullable=False)
    mail_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    actual_link = Column(String, nullable=False)

