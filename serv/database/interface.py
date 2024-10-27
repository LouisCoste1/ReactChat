import sqlite3
import os

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    model_dir = "database/db_models"

    # be careful, will execute every file in model_dir directory
    for file in os.listdir(model_dir):
        # Check if it's a file and not a directory
        if not os.path.isfile(os.path.join(model_dir, file)):
            # Meaning it's a directory, so pass
            continue
        
        # Execute the SQL script
        sql_file = os.path.join(model_dir, file)
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        
        try:
            c.executescript(sql_script)
            conn.commit()
            print("Initialized database")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    conn.close()
