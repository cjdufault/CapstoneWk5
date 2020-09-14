from peewee import *


db = SqliteDatabase('records_db.sqlite')


def main():
    


class Record:
    def __init__(self, name, country, catches):
        self.name = name
        self.country = country
        self.catches = catches
    
    def __str__(self):
        return f'Name: {self.name} Country: {self.country} Number of Catches: {self.catches}'


if __name__ == '__main__':
    main()
