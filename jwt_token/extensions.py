from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# this object can use in multiple files
db = SQLAlchemy()  # for database object    
jwt = JWTManager() # for jwt object