from bclib import edge
from config import config

app = edge.from_options(config)

sqlite_connection = app.db_manager.open_sqllite_connection('sqlite_todo')
cursor = sqlite_connection.connection.cursor()
cursor.execute('''CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    completed BOOLEAN,
    title TEXT,
    date DATE
);
''')
sqlite_connection.connection.commit()
