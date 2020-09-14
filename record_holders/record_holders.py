from peewee import *


db = SqliteDatabase('records_db.sqlite')


def main():
    db.connect()
    db.create_tables([Record])
    populate_db()
    

def add_record(name_str, country_str, catches_int):
    new_record = Record(name=name_str, country=country_str, catches=catches_int)
    new_record.save()
    

def update_record(name_str, catches_int):
    rows_changed = Record.update(catches=catches_int).where(Record.name == name_str).execute()
    return rows_changed
    
    
def delete_record(name_str):
    rows_deleted = Record.delete().where(Record.name == name_str).execute()
    return rows_deleted
    

# returns all records where 'name' matches search_name
def search(name_str):
    rows_selected = Record.select().where(Record.name == name_str)
    return rows_selected
    

# fills db with example data
def populate_db():
    add_record('Janne Mustonen', 'Finland', 98)
    add_record('Ian Stewart', 'Canada', 94)
    add_record('Aaron Gregg', 'Canada', 88)
    add_record('Chad Taylor', 'USA', 78)


# model class for records to be stored in database
class Record(Model):
    name = CharField()
    country = CharField()
    catches = IntegerField()
    
    class Meta:
        database = db
    
    def __str__(self):
        return f'Name: {self.name} Country: {self.country} Number of Catches: {self.catches}'


if __name__ == '__main__':
    main()
