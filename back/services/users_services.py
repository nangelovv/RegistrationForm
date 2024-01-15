from sqlalchemy import update, and_, exists
from jwt import encode, decode, get_unverified_header
from data.users_models import *
from common.secret import SECRET_KEY, EMAIL_KEY, API_KEY
from common.responses import *
from mailjet_rest import Client
import os, random, string
import uuid, json


def try_login(email: str, password: str, session):

    try:
        user_data = session.query(Users).filter(Users.email == email).first()
        
        if not user_data:
            return False
        session.close()

        return user_data if (user_data.email == email and user_data.password == password) else False
    except:
        BadRequest()


def create_token(data: Users) -> str:
    """
    Creates a token for a user
    """

    _PAYLOAD_DATA = {"id": data.user_id, "email": data.email}
    return encode(payload=_PAYLOAD_DATA, key=SECRET_KEY)


def register(data: RegistrationData, session):
    """
    Registers a new user

    1. Checks if email exists
    2. Create new user row in database

    Args:
        data (str): RegistrationData object

    Returns:
        HTTP response
    """

    try:
        
        # Checks if email exists
        if session.query(Users).filter(Users.email == data.email).first():
            return Conflict("Email already taken.")
        
        id = str(uuid.uuid4())
        auth_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        
        # Create new user row in database
        session.add(Users(
            user_id = id,
            email = data.email,
            first_name = data.first_name,
            last_name = data.last_name,
            password = data.password,
            auth_code = auth_code,
            is_verified = 0
            ))
        session.commit()
        session.close()

        # Send verification email
        api_key = os.environ['API_KEY']
        api_secret = os.environ['EMAIL_KEY']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "nk.angelovv@gmail.com",
                "Name": "Registration"
            },
            "To": [
                {
                "Email": data.email,
                "Name": f"{data.first_name} {data.last_name}"
                }
            ],
            "Subject": "Thank you for registering!",
            "TextPart": f"One last step to complete your registration. Please enter the following code in the site: {auth_code}",
            }
        ]
        }
        mailjet.send.create(data=data)
        return Created()
    except:
        return BadRequest()


def _is_authenticated(token: str) -> str | bool:
    """
    Checks if correct user token is provided
    """

    try:
        header_data = get_unverified_header(token)
        decoded_token = decode(token, key=SECRET_KEY, algorithms=[header_data['alg'], ])
        return decoded_token['id']
    except:
        return False


def change_email(txt: str, token: str, session):
    """
    Updates the email in database for current user
    """

    id = _is_authenticated(token)
    if not id:
        return BadRequest("Ooops, something went wrong...")

    try:
        if session.query(Users).filter(Users.email == txt).first():
            return Conflict("Email already taken.")

        stmt = (
            update(Users)
            .where(Users.user_id == id)
            .values(email = txt)
        )

        session.execute(stmt)
        session.commit()
        session.close()
        return NoContent()
    except:
        return BadRequest()


def change_password(txt: str, token: str, session):
    """
    Updates the password in database for current user
    """

    id = _is_authenticated(token)
    if not id:
        return BadRequest("Ooops, something went wrong...")

    try:
        stmt = (
            update(Users)
            .where(Users.user_id == id)
            .values(password = txt)
        )

        session.execute(stmt)
        session.commit()
        session.close()
        return NoContent()
    except:
        return BadRequest()


def verify(code: str, token: str, session):

    id = _is_authenticated(token)
    if not id:
        return BadRequest("Ooops, something went wrong...")

    try:
        result = session.query(Users).filter(Users.user_id == id, Users.auth_code == code).first()

        if not result:
            return BadRequest("Invalid code.")

        stmt = (
            update(Users)
            .where(Users.user_id == id)
            .values(is_verified = 1)
        )

        session.execute(stmt)
        session.commit()
        session.close()
        return NoContent()
    except:
        return BadRequest()


def delete(token, session):
    id = _is_authenticated(token)

    if not id:
        return BadRequest("Ooops, something went wrong...")
    try:
        session.query(Users).filter(Users.user_id == id).delete()
        session.commit()
        session.close()
        return Accepted()
    except:
        return BadRequest()