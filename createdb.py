from app import db

def create(a_db):
    return a_db.create_all()

if __name__ == "__main__":
    create(db)
