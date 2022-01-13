from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from .database.constants import CLIENT_SECRET
from .routers import user_router, card_router
from .database.models import User, Card, Deck
from .database.connection import connect, create_database

# API set---------------------------------------------------------------------------------------------------------------
from .routers.common import create_access_token, oauth2_sch

app = FastAPI(
    title="Gods Among Us",
    description="This is a cards game about mythology",
    version='0.0.2a'
)

api_v1 = APIRouter(prefix='/api/v1')
api_v1.include_router(user_router)
api_v1.include_router(card_router)


# GENERAL endpoints-----------------------------------------------------------------------------------------------------

@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username or password not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )


@api_v1.get('/')
async def index():
    return {'Welcome ': 'Summoner'}


app.include_router(api_v1)


# Events----------------------------------------------------------------------------------------------------------------
@app.on_event('startup')
def startup():
    create_database()
    with connect:
        connect.create_tables([User, Card, Deck])


@app.on_event('shutdown')
def shutdown():
    if not connect.is_closed():
        connect.close()
