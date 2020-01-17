from app import create_app
from app.models import db

db.create_all(app = create_app())

if __name__ == '__main__':
    app.run(debug=True)