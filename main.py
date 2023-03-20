import psycopg2

# Функция, создающая структуру БД (таблицы)

def create_db(conn):

        cur.execute("""
            CREATE TABLE clients(
	        clients_id SERIAL PRIMARY KEY,
	        first_name VARCHAR(60) NOT NULL,
	        last_name VARCHAR(60) NOT NULL,
	        email VARCHAR(60) NOT NULL UNIQUE
	        );
            """)

        cur.execute("""
            CREATE TABLE phone_clients(
            phone_clients_id SERIAL PRIMARY KEY,
            phone VARCHAR(11) NOT NULL UNIQUE,
            clients_id INTEGER REFERENCES clients(clients_id)
            );
            """)
        conn.commit()

# Функция, позволяющая добавить нового клиента.

def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email)
        VALUES (%s, %s, %s);
        """, (first_name, last_name, email))
    conn.commit()
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())

# Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(conn, clients_id, phone):
    cur.execute("""
        INSERT INTO phone_clients(clients_id, phone)
        VALUES (%s, %s);
        """, (clients_id, phone))
    conn.commit()
    cur.execute("""
        SELECT * FROM phone_clients;
        """)
    print(cur.fetchall())

# Функция, позволяющая изменить данные о клиенте.

def change_client(conn, clients_id, first_name=None, last_name=None, email=None):
    cur.execute("""
        UPDATE clients SET first_name=%s, last_name=%s, email=%s 
        WHERE clients_id=%s;
        """, (clients_id, first_name, last_name, email))
    conn.commit()
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())

# Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(conn, clients_id, phone):
    cur.execute("""
        DELETE FROM phone_clients 
        WHERE clients_id=%s and phone=%s;
        """, (clients_id, phone))
    conn.commit()
    cur.execute("""
        SELECT * FROM phone_clients;
        """)
    print(cur.fetchall())

# Функция, позволяющая удалить существующего клиента.

def delete_client(conn, clients_id):
    cur.execute("""
        DELETE FROM phone_clients 
        WHERE clients_id=%s
        """, (clients_id, ))
    conn.commit()
    cur.execute("""
        DELETE FROM clients 
        WHERE clients_id=%s;
        """, (clients_id, ))
    conn.commit()
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute("""
            SELECT c.clients_id, c.first_name, c.last_name, c.email, p.phone FROM clients c
            JOIN phone_clients p ON c.clients_id = p.clients_id
            WHERE c.first_name LIKE %s and c.last_name LIKE %s 
            and c.email LIKE %s;
            """, (first_name, last_name, email))
    else:
        cur.execute("""
            SELECT c.clients_id, c.first_name, c.last_name, c.email, p.phone FROM clients c
            LEFT JOIN phone_clients p ON c.clients_id = p.clients_id
            WHERE c.first_name LIKE %s and c.last_name LIKE %s 
            and c.email LIKE %s and p.phone LIKE %s;
            """, (first_name, last_name, email, phone))
    conn.commit()
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="base_clients", user="postgres", password="admin") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE phone_clients;
            DROP TABLE clients;
            """)
            create_db(conn)
            add_client(conn, 'Иван', 'Иванов', 'IVANOF@ya.ru')
            add_client(conn, 'Антон', 'Антонов', 'ANTONOFF@ya.ru')
            add_phone(conn, 1, '89144112218')
            add_phone(conn, 2, '89148122114')
            change_client(conn, 'Сергей', 'Сергеев', 'SERG@ya.ru', 1)
            delete_phone(conn, 1, '89144112218')
            delete_client(conn, 1)
            find_client(conn, None, None, None, '89148122114')
            find_client(conn, 'Антон')
    conn.close()