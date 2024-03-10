from bclib import edge
from config import config
from datetime import datetime


app = edge.from_options(config)


@app.restful_action(app.get("api/todos"))
def get_all(context: edge.RESTfulContext):
    sqlite_connection = context.dispatcher.db_manager.open_sqllite_connection('sqlite_todo')
    with sqlite_connection:
        cursor = sqlite_connection.connection.cursor()
        cursor.execute("SELECT * FROM todos")

        data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

        return data
    

@app.restful_action(app.get("api/todos/:id"))
def get_one(context: edge.RESTfulContext):
    todo_id = int(context.url_segments.id)
    sqlite_connection = context.dispatcher.db_manager.open_sqllite_connection('sqlite_todo')
    with sqlite_connection:
        cursor = sqlite_connection.connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = :id", {'id': todo_id})

        data = dict(zip([column[0] for column in cursor.description], cursor.fetchone()))

        return data
    
@app.restful_action(app.post("api/todos"))
def add(context: edge.RESTfulContext):
    title = context.body['title']
    sqlite_connection = context.dispatcher.db_manager.open_sqllite_connection('sqlite_todo')
    with sqlite_connection:
        cursor = sqlite_connection.connection.cursor()
        date = datetime.today().strftime('%Y-%m-%d')
        cursor.execute('''INSERT INTO todos (title, completed, date)
                        VALUES (:title, 0, :date)''', {'title': title, 'date': date})
        sqlite_connection.connection.commit()

        return {'success': True, 'id': cursor.lastrowid}
    

@app.restful_action(app.put("api/todos/:id"))
def update(context: edge.RESTfulContext):
    todo_id = int(context.url_segments.id)
    data = {'title': context.body.get('title'), 'completed': context.body.get('completed')}
    data = {key: value for key, value in data.items() if value is not None}
    sqlite_connection = context.dispatcher.db_manager.open_sqllite_connection('sqlite_todo')
    with sqlite_connection:
        query = 'UPDATE todos SET '
        query += (', '.join([column + '= :' + column for column in data.keys()]))
        query +=' WHERE id = :id'

        cursor = sqlite_connection.connection.cursor()
        cursor.execute(query, data | {'id': todo_id})
        sqlite_connection.connection.commit()

    return {'success': True}


@app.restful_action(app.delete("api/todos/:id"))
def delete(context: edge.RESTfulContext):
    todo_id = int(context.url_segments.id)
    sqlite_connection = context.dispatcher.db_manager.open_sqllite_connection('sqlite_todo')
    with sqlite_connection:
        cursor = sqlite_connection.connection.cursor()
        cursor.execute("DELETE FROM todos WHERE id = :id", {'id': todo_id})
        sqlite_connection.connection.commit()

        return {'success': True}



app.listening()
