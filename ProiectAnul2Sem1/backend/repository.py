import sqlite3, hashlib, sys, random, os
from datetime import datetime, timedelta

database = "C:/www/G610-WebProgramming1-MC/ProiectAnul2Sem1/backend/db.db"


def connect_to_database(database_file_path):
    conn = sqlite3.connect(database_file_path)
    return conn


def get_users(conn):
    query = f"select * from users"
    cursor = conn.cursor()
    users = list(cursor.execute(query))
    if users:
        return users
    else:
        return None


def get_user(conn, id):
    query = f"select * from users WHERE id = '{id}'"
    cursor = conn.cursor()
    user = list(cursor.execute(query))
    if user:
        return user[0]
    else:
        return None


def create_user(conn, body, password):
    query = """insert into users(id_group, firstname, lastname, email, password, job_title, created, updated, active)
    values (?,?,?,?,?,?,?,?,?)"""
    user_data = (
        body.get("id_group"),
        body.get("firstname"),
        body.get("lastname"),
        body.get("email"),
        password,
        body.get("job_title"),
        datetime.utcnow().timestamp(),
        datetime.utcnow().timestamp(),
        1,
    )
    cursor = conn.cursor()
    cursor.execute(query, user_data)
    conn.commit()

    id_user = cursor.lastrowid
    user = get_user(conn, id_user)

    return user


def update_user(conn, body, password):
    data = {}
    for key in body:
        if (key != "id" and key != "password"):
            data[key] = body[key]

    if len(data) > 0:
        data['updated'] = datetime.utcnow().timestamp()
        query = "UPDATE `users` SET "
        for key in data:
            query += f"`{key}` = '{data[key]}',"

        query = query[:-1]
        query += f" WHERE id = '{body['id']}'"

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    id_user = body['id']
    user = get_user(conn, id_user)

    return user


def delete_user(conn, id):
    query = f"DELETE FROM users WHERE id = '{id}'"

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    return True


def authenticate(conn, email, password):
    query = f"select u.id, u.firstname, u.lastname from users u where email='{email}' AND password = '{password}'"
    cursor = conn.cursor()
    user = cursor.execute(query).fetchone()

    if user:
        token = generate_token(conn, user[0])

        response = {
            'id': user[0],
            'firstname': user[1],
            'lastname': user[2],
            'token': token
        }
        return response
    else:
        return {}


def generate_token(conn, id_user):
    query = f"select token from user_tokens where id_user='{id_user}'"
    cursor = conn.cursor()
    user = cursor.execute(query).fetchone()

    if user:
        return user[0]
    else:
        password = str(id_user) + str(random.randint(10, 10000000000000000000))
        token = hashlib.sha1(password.encode()).hexdigest()
        print(password, token)

        expires = datetime.today() + timedelta(days=2)
        query = """insert into user_tokens(id_user, token, created, expires)
            values (?,?,?,?)"""
        token_data = (
            id_user,
            token,
            datetime.utcnow().timestamp(),
            expires.timestamp()
        )
        cursor = conn.cursor()
        cursor.execute(query, token_data)
        conn.commit()

        return token


def get_vms(conn):
    query = f"select * from virtual_machines"
    cursor = conn.cursor()
    vms = list(cursor.execute(query))
    if vms:
        return vms
    else:
        return None


def get_vm(conn, id):
    query = f"select * from virtual_machines WHERE id = '{id}'"
    cursor = conn.cursor()
    vm = cursor.execute(query).fetchone()
    if vm:
        return vm
    else:
        return None


def create_vm(conn, body):
    query = """insert into virtual_machines(id_group, id_cluster, title, ip, active)
    values (?,?,?,?,?)"""
    vm_data = (
        body.get("id_group"),
        body.get("id_cluster"),
        body.get("title"),
        body.get("ip"),
        1,
    )
    cursor = conn.cursor()
    cursor.execute(query, vm_data)
    conn.commit()

    id_vm = cursor.lastrowid
    vm = get_vm(conn, id_vm)

    return vm


def update_vm(conn, body):
    data = {}
    for key in body:
        if (key != "id"):
            data[key] = body[key]

    if len(data) > 0:
        query = "UPDATE `virtual_machines` SET "
        for key in data:
            query += f"`{key}` = '{data[key]}',"

        query = query[:-1]
        query += f" WHERE id = '{body['id']}'"

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    id_vm = body['id']
    vm = get_vm(conn, id_vm)

    return vm


def delete_vm(conn, id):
    query = f"DELETE FROM virtual_machines WHERE id = '{id}'"

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    return True


def get_user_logs(conn, body):
    query = f"select * from user_logs"
    cursor = conn.cursor()
    users = list(cursor.execute(query))
    if users:
        return users
    else:
        return None


def upload_file(conn, body):
    query = f"select * from user_logs"
    cursor = conn.cursor()
    users = list(cursor.execute(query))
    if users:
        return users
    else:
        return None


def get_files(conn):
    query = f"select * from user_files"
    cursor = conn.cursor()
    files = list(cursor.execute(query))
    if files:
        return files
    else:
        return None

def get_file(conn, id):
    query = f"select * from user_files WHERE id = '{id}'"
    cursor = conn.cursor()
    file = list(cursor.execute(query))
    if file:
        return file[0]
    else:
        return None


def create_file(conn, body):
    query = """insert into user_files(id_user, title, file, created)
    values (?,?,?,?)"""
    file_data = (
        body.get("id_user"),
        body.get("title"),
        body.get("file"),
        datetime.utcnow().timestamp()
    )
    cursor = conn.cursor()
    cursor.execute(query, file_data)
    conn.commit()

    id_file = cursor.lastrowid
    file = get_file(conn, id_file)

    return file


def delete_file(conn, body):
    query = f"DELETE FROM user_files WHERE id = '{id}'"

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    return True


def get_sync_jobs(conn):
    query = f"select * from sync_jobs"
    cursor = conn.cursor()
    items = list(cursor.execute(query))
    if items:
        return items
    else:
        return None

def get_sync(conn, id):
    query = f"select * from sync_jobs WHERE id='{id}'"
    cursor = conn.cursor()
    item = cursor.execute(query).fetchone()

    if item:
        return item
    else:
        return None


def update_sync(conn, body):
    password = str(body.get("id_user")) + str(random.randint(10, 10000000000000000000))
    hash = hashlib.sha1(password.encode()).hexdigest()

    query = """insert into sync_jobs(id_user, status, hash, created)
        values (?,?,?,?)"""
    vm_data = (
        body.get("id_user"),
        "started",
        hash,
        datetime.utcnow().timestamp()
    )
    cursor = conn.cursor()
    cursor.execute(query, vm_data)
    conn.commit()

    id_sync = cursor.lastrowid
    sync = get_sync(conn, id_sync)

    return sync

def verify_authentication(conn, body):
    token = body.headers['Token']

    if token != "null" and token != "":
        query = f"SELECT u.id, u.firstname, u.lastname, u.email, u.job_title, ut.token FROM user_tokens ut JOIN users u ON ut.id_user = u.id WHERE ut.token='{token}' AND u.active=1"
        cursor = conn.cursor()
        user = cursor.execute(query).fetchone()

        return user
    else:
        return False


def user_log(conn, user, action):
    if len(user) == 4:
        id_user = user['id']
    else:
        id_user = user[0]

    query = """insert into user_logs(id_user, log_type, created, duration)
        values (?,?,?,?)"""
    data = (
        id_user,
        action,
        datetime.utcnow().timestamp(),
        1,
    )

    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()

    return None
