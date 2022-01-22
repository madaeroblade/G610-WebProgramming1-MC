from flask import Flask, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS

from repository import *

UPLOAD_FOLDER = 'C:/www/G610-WebProgramming1-MC/ProiectAnul2Sem1/backend/files'

app = Flask("UsersAPI")
CORS(app)


@app.route("/api/v1/users", methods=["GET", "POST", "PUT", "DELETE"])
def users_crud():
    conn = connect_to_database(database)
    registeredUser = verify_authentication(conn, request)

    if registeredUser:
        try:
            # returns the users list
            if request.method == "GET":
                users = get_users(conn)
                response = {
                    "users": users
                }

                user_log(conn, registeredUser, 'get_users')
                conn.close()
                return response, 200

            # creates a new user
            if request.method == "PUT":
                formData = request.form
                password = hashlib.sha1(formData['password'].encode()).hexdigest()
                user = create_user(conn, formData, password)

                response = {
                    "user": user,
                }

                user_log(conn, registeredUser, 'add_user')
                conn.close()
                return response, 200

            if request.method == "POST":
                formData = request.form
                password = "null"

                if formData.get('password') is not None:
                    password = hashlib.sha1(formData['password'].encode()).hexdigest()

                user = update_user(conn, formData, password)

                response = {
                    "user": user,
                }
                
                user_log(conn, registeredUser, 'edit_user')
                conn.close()
                return response, 200

            if request.method == "DELETE":
                id_user = request.form['id']
                delete_user(conn, id_user)

                response = {}
                user_log(conn, registeredUser, 'delete_user')
                conn.close()
                return response, 200

            conn.close()
            return {"error": "Invalid request"}, 500
        except Exception as e:
            conn.close()
            error = {
                "error": f"--there was an error: {e}"
            }
            return error, 500
    else:
        conn.close()
        error = {
            "error": "--Invaid authentication token."
        }
        return error, 401


@app.route("/api/v1/user/files", methods=["GET", "PUT"])
def files_crud():
    conn = connect_to_database(database)
    registeredUser = verify_authentication(conn, request)
    if registeredUser:
        try:
            # returns the files list
            if request.method == "GET":
                files = get_files(conn)
                response = {
                    "files": files
                }

                user_log(conn, registeredUser, 'get_files')
                conn.close()
                return response, 200

            # creates a new file
            if request.method == "PUT":
                if 'file' not in request.files:
                    return {
                        'error': f"--there was an error"
                    }, 401

                file = request.files['file']
                if file.filename == '':
                    return {
                               'error': f"--there was an error"
                           }, 401

                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))

                    fileData = {
                        "id_user": registeredUser[0],
                        "title": request.form.get('title'),
                        "file": filename
                    }

                    fileInfo = create_file(conn, fileData)
                    response = {
                        "file": fileInfo,
                    }
                if response:
                    user_log(conn, registeredUser, 'add_file')
                    return response, 200

            conn.close()
            return {"error": "Invalid request"}, 500
        except Exception as e:
            conn.close()
            error = {
                "error": f"--there was an error: {e}"
            }
            return error, 500
    else:
        conn.close()
        error = {
            "error": "--Invaid authentication token."
        }
        return error, 401

@app.route("/api/v1/sync", methods=["GET", "PUT"])
def sync_crud():
    conn = connect_to_database(database)
    registeredUser = verify_authentication(conn, request)
    if registeredUser:
        try:
            # returns the sync items list
            if request.method == "GET":
                items = get_sync_jobs(conn)
                response = {
                    "items": items
                }

                user_log(conn, registeredUser, 'get_sync_items')
                conn.close()
                return response, 200

            # sync some items
            if request.method == "PUT":
                formData = request.form
                sync = update_sync(conn, formData)

                response = {
                    "sync": sync,
                }

                user_log(conn, registeredUser, 'sync_items')
                conn.close()
                return response, 200

            conn.close()
            return {"error": "Invalid request"}, 500
        except Exception as e:
            conn.close()
            error = {
                "error": f"--there was an error: {e}"
            }
            return error, 500
    else:
        conn.close()
        error = {
            "error": "--Invaid authentication token."
        }
        return error, 401

@app.route("/api/v1/login", methods=["POST"])
def login():
    try:
        formData = request.form

        print(formData)
        email = formData['email']
        password = hashlib.sha1(formData['password'].encode()).hexdigest()

        conn = connect_to_database(database)
        user = authenticate(conn, email, password)

        if len(user) == 0:
            error = {
                "error": "--Failed to sign in. Email or password are wrong."
            }
            return error, 401

        user_log(conn, user, 'login')
        return user, 200
    except Exception as e:
        error = {
            "error": f"--Failed to sign in. Cause: {e}"
        }
        return error, 500


@app.route("/api/v1/vm", methods=["GET", "POST", "PUT", "DELETE"])
def vms_crud():
    conn = connect_to_database(database)
    registeredUser = verify_authentication(conn, request)
    if registeredUser:
        try:
            # returns the users list
            if request.method == "GET":
                vms = get_vms(conn)
                response = {
                    "vms": vms
                }

                user_log(conn, registeredUser, 'get_vms')
                conn.close()
                return response, 200

            # creates a new user
            if request.method == "PUT":
                formData = request.form
                vm = create_vm(conn, formData)

                response = {
                    "vm": vm,
                }

                user_log(conn, registeredUser, 'add_vm')
                conn.close()
                return response, 200

            if request.method == "POST":
                formData = request.form

                vm = update_vm(conn, formData)

                response = {
                    "vm": vm,
                }

                user_log(conn, registeredUser, 'edit_vm')
                conn.close()
                return response, 200

            if request.method == "DELETE":
                id_vm = request.form['id']
                delete_vm(conn, id_vm)

                response = {}

                user_log(conn, registeredUser, 'delete_vm')
                conn.close()
                return response, 200

            conn.close()
            return {"error": "Invalid request"}, 500
        except Exception as e:
            conn.close()
            error = {
                "error": f"--there was an error: {e}"
            }
            return error, 500
    else:
        conn.close()
        error = {
            "error": "--Invaid authentication token."
        }
        return error, 401

if __name__ == "__main__":
    app.run(debug=True, port=3010)
