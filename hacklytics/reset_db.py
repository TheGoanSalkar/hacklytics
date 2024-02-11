from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.config['SECRET_KEY'] = '32659db159db1a52cd39b981b2f56a22'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///init_db.sql'
db = SQLAlchemy(app)


with app.app_context():
    db.reflect()
    # Iterate over each table and delete all records
    for table_name in db.metadata.tables.keys():
        table = db.metadata.tables[table_name]
        db.session.execute(table.delete())
    db.session.commit()

with app.app_context():
    db.reflect()
    for table_name in db.metadata.tables:
        print(table_name)

print('done')

with app.app_context():
        # Reflect the current database tables
        db.reflect()
        
        # Iterate over each table and print its entries
        for table_name in db.metadata.tables.keys():
            table = db.metadata.tables[table_name]
            print(f"Entries in {table_name}:")
            
            # Querying all records in the table
            entries = db.session.query(table).all()
            for entry in entries:
                print(entry)
            print("\n")  # Add a newline for better separation between tables
