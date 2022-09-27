import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client_base(
        Id SERIAL PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Surname VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL);
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client_phone(
        Id SERIAL PRIMARY KEY,
        Client_id INTEGER NOT NULL REFERENCES Client_base(Id),
        Phone VARCHAR(50) UNIQUE);
        """)
    conn.commit()


def add_client(conn, client_name, client_surname, client_email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Client_base(Name, Surname, email)
        VALUES(%s, %s, %s);
        """, (client_name, client_surname, client_email))


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Client_phone(Client_id, Phone)
        VALUES(%s,%s);
        """, (client_id, phone))


def change_client(conn, client_id, new_client_name, new_client_surname, new_client_email, new_client_phone):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE Client_base
        SET Name = %s, Surname = %s, email = %s WHERE Id = %s;
        """, (new_client_name, new_client_surname, new_client_email, client_id))
        cur.execute("""
        UPDATE Client_phone
        SET Phone = %s WHERE Client_id = %s;
        """, (new_client_phone, client_id))


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Client_phone WHERE Client_id = %s AND Phone = %s;
        """, (client_id, phone))


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Client_phone
        WHERE Client_id = %s;
        """, (client_id,))
        cur.execute("""
        DELETE FROM Client_base
        WHERE Id = %s;
        """, (client_id,))
    conn.commit()


def find_client(conn, Name=None, Surname=None, email=None, Phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT *
        FROM Client_base AS cb
        LEFT JOIN Client_phone AS cp ON cb.Id = cp.Client_id
        WHERE (Name = %(Name)s OR %(Name)s IS NULL)
        AND (Surname = %(Surname)s OR %(Surname)s IS NULL)
        AND (email = %(email)s OR %(email)s IS NULL)
        AND (Phone = %(Phone)s OR %(Phone)s IS NULL);
        """, {"Name": Name, "Surname": Surname, "email": email, "Phone": Phone})
        print(cur.fetchall())


conn = psycopg2.connect(database='Home_work_DB-4', user='postgres', password='29072017svadba')
with conn.cursor() as cur:
    create_db(conn)
    add_client(conn, 'Аланка', 'Хулиганка', 'pochtahuliganki@gmail.com')
    add_client(conn, 'Ксюша', 'Капуша', 'pochtakapushy@gmail.com')
    add_client(conn, 'Аминка', 'Витаминка', 'pochtavitaminki@mail.ru')
    add_phone(conn, 3, '8(123)456-78-90')
    add_phone(conn, 2, '8(098)765-43-21')
    add_phone(conn, 3, '8(955)977-66-21')
    change_client(conn, 2, 'Ксюшенция', 'Капушенция', 'pochtakapushy@gmail.com', '8(089)765-43-21')
    delete_phone(conn, 3, '8(955)977-66-21')
    delete_client(conn, 1)
    find_client(conn, 'Ксюшенция')
conn.close()
