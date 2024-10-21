from pydantic import BaseModel, EmailStr


# Pydantic schemas
class CreateEmailLinkedSchema(BaseModel):
    generated_id: str
    status: str
    user_id: str
    mail_id: EmailStr
    message: str
    subject: str
    actual_link: str

class EmailSchema(BaseModel):
    mail_id: EmailStr
    subject: str