from peewee import *


db = SqliteDatabase('records_db.sqlite')


def main():
    db.connect()
    db.create_tables([Record])
    populate_db()
    
    running = True
    while running:
        menu_options = {1: select_all, 2: search, 3: add_record, 4: update_record, 5: delete_record}
        selection = menu()
        
        if selection == 6:  # 6 is quit
            running = False
        else:
            response = menu_options[selection]()   # execute selected function
            
            # response is (response string, returned rows)
            if response[1] != None:
                print(response[0])
                for record in response[1]:
                    print('\t' + str(record))
            else:
                print(response[0])
            print()
    
def menu():
    while True:
        print('1. View all records')
        print('2. Search records by name')
        print('3. Add a record')
        print('4. Update a record')
        print('5. Delete a record')
        print('6. Quit')
        response = input('Make a selection:  ')
        
        if response.isdigit():
            selection = int(response)
            if selection > 0 and selection < 7:
                return selection
        
        print('Invalid selection\n')
    

def add_record(name_str=None, country_str=None, catches_int=None):
    if name_str == None:
        name_str = input('Enter record holder\'s name:  ')
    if country_str == None:
        country_str = input('Enter record holder\'s country:  ')
    if catches_int == None:
        catches_int = input('Enter number of chainsaws caught:  ')
    
    try:
        new_record = Record(name=name_str, country=country_str, catches=catches_int)
        new_record.save()
        return 'Added new record:', [new_record]
    except IntegrityError as e:
        print(e)
        return 'Failed to add record', None
    

def update_record(name_str=None, catches_int=None):
    if name_str == None:
        name_str = input('Enter record holder\'s name:  ')
    if catches_int == None:
        catches_int = input('Enter number of chainsaws caught:  ')
    
    try:
        rows_changed = Record.update(catches=catches_int).where(Record.name == name_str).execute()
        return 'Updated record:', rows_changed
    except IntegrityError as e:
        print(e)
        return 'Failed to update record', None
    

def delete_record(name_str=None):
    if name_str == None:
        name_str = input('Enter record holder\'s name:  ')
    
    try:
        rows_deleted = Record.delete().where(Record.name == name_str).execute()
        return 'Deleted record:', rows_deleted
    except IntegrityError as e:
        print(e)
        return 'Failed to delete record', None
    

# returns all records where 'name' matches search_name
def search(name_str=None):
    if name_str == None:
        name_str = input('Enter record holder\'s name:  ')
    
    # Record.name is unique, so only one result, if any, is expected
    matching_record = Record.get_or_none(Record.name == name_str)
    
    if matching_record != None:
        return 'Found matching record:', [matching_record]
    else:
        return 'Found no matching records', None


# returns all records, sorted by number of catches
def select_all():
    rows_selected = Record.select().order_by(Record.catches)
    
    if len(rows_selected) > 0:
        return 'All records:', rows_selected
    else:
        return 'No records found', None
    

# fills db with example data
def populate_db():
    if search(name_str='Janne Mustonen') == None:
        add_record(name_str='Janne Mustonen', country_str='Finland', catches_int=98)
    if search(name_str='Ian Stewart') == None:
        add_record(name_str='Ian Stewart', country_str='Canada', catches_int=94)
    if search(name_str='Aaron Gregg') == None:
        add_record(name_str='Aaron Gregg', country_str='Canada', catches_int=88)
    if search(name_str='Chad Taylor') == None:
        add_record(name_str='Chad Taylor', country_str='USA', catches_int=78)


# model class for records to be stored in database
class Record(Model):
    name = CharField(unique=True)   # only one record per 
    country = CharField()
    catches = IntegerField()
    
    class Meta:
        database = db
    
    def __str__(self):
        return f'Name: {self.name} Country: {self.country} Number of Catches: {self.catches}'


if __name__ == '__main__':
    main()
