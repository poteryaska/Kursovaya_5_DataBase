from src.config import config
from src.classes import DBManager
def main():
    params = config()
    HH = DBManager('HH', params)
    HH.create_database()



if __name__ == '__main__':
    main()