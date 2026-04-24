from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



# Initialize extensions
db = MongoEngine()
bcrypt = Bcrypt()
oauth = OAuth()
cache = Cache()
limiter = Limiter(get_remote_address)