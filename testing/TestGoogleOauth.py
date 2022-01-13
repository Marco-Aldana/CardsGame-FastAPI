import os
import pathlib

import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from fastapi import Query, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from project import app, create_access_token

from project.database.constants import CLIENT_ID
from project.repository.user_repository import UserRepository

GOOGLE_CLIENT_ID = CLIENT_ID
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "../project/database/GoogleOauth2.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:8000/google-callback"
)


@app.get("/login")
def login():
    authorization_url, state = flow.authorization_url()
    return RedirectResponse(authorization_url)


@app.get('/google-callback')
def google_callback(code: str = Query(...)):
    flow.fetch_token(code=code)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    user = UserRepository.get_user_by_email_repository(id_info.get("email"))
    if user:
        return {
            'info': id_info,
            'user info': user.__data__,
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username or password not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )
