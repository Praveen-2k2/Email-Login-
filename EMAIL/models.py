

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

