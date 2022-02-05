import mariadb as db
import dbcreds as c
import traceback as taa

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except Exception as e:
        print(e)
        print("Something went wrong!")
    return conn, cursor  

# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e)
        print("cursor close error: what happened?")

    try:
        conn.close()
    except Exception as e:
        print(e)
        print("connection close error")

def get_recipes_db():
    recipes = None
    conn, cursor = connect_db()

    try:
        cursor.execute("select title, content, created_at, image_url from recipes")
        recipes = cursor.fetchall()
    except db.OperationalError:
        return False, "something went wrong with the DB, please try again in 5 minutes"
    except db.ProgrammingError:
        return False, "Error running DB Query, please file bug report"
    except Exception as e:
        return False, e

    disconnect_db(conn, cursor)

    return recipes

def attempt_login_db(username, password):
    user = None

    conn, cursor = connect_db()

    try:
        cursor.execute("select id, created_at from users where username =? and password =?", [username, password])
        user = cursor.fetchone()
    except Exception as e:
        error_msg = t.print_exc
        return False, error_msg

    disconnect_db(conn, cursor)

    if user == None:
        return False, "Login unsuccessful, please check your credentials and try again!"
    else:
        return user

def get_recipe_star_db(recipes_id):
    recipes = None

    conn, cursor = connect_db()

    try:
        cursor.execute("select created_at, users_id from recipe_star where recipes_id =?", [recipes_id])
        recipes = cursor.fetchall()
    except Exception as e:
        error_msg = t.print_exc
        return False, error_msg

    disconnect_db(conn, cursor)

    if recipes == None:
        return False
    else:
        return recipes
    
def post_users_db(username, password):
    user = None

    conn, cursor = connect_db()

    try:
        cursor.execute("insert into users (username, password) values(?,?)", [username, password])
        conn.commit()

        cursor.execute("select username, created_at, id from users where username =? and password =?", [username, password])
        user = cursor.fetchone()
    except db.OperationalError:
        print(
            "something went wrong with the DB, please try again in 5 minutes")
    except db.ProgrammingError:
        print("Error running DB Query, please file bug report")
    except:
        print("Something went wrong!")

    disconnect_db(conn, cursor)

    if user == None:
        return False, "error message from dbinteractions"
    else:
        return True, user

print(get_recipes_db())