from flask import Blueprint

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')
task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

from .user import *
from .task import *
from .auth import *
