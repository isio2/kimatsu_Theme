import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


#ソルト
def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt


#ハッシュ
def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password


#新規登録
def insert_user(user_name, password):
    sql = 'INSERT INTO staff_sample VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count


#利用者ログイン
def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM staff_sample WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

            if  flg == False:
                sql = 'SELECT hashed_password, salt FROM admin_sample WHERE name = %s'
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


# 一覧
def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT title, author, publisher, pages FROM books_sample'

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


# 図書登録
def insert_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO books_sample VALUES (default,%s, %s, %s, %s)"

    cursor.execute(sql,(title, author, publisher, pages))

    connection.commit()
    cursor.close()
    connection.close()


# 図書削除
def delete_book(id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'DELETE FROM books_sample WHERE id = %s'

    cursor.execute(sql, (id))

    connection.commit()
    cursor.close()
    connection.close()


# 図書編集
def edit_book(title, author, publisher, pages):
    connection = get_connection()
    cursor = connection.cursor()
    sql ="UPDATE books_sample SET title = ?, author = ?, publisher = ?, pages = ?, WHERE id = ?";

    cursor.execute(sql,(title,author, publisher,pages))

    connection.commit()
    cursor.close()
    connection.close()


#利用者登録
def insert_user(user_name, password):
    sql = 'INSERT INTO staff_sample VALUES(default, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count


#管理者ログイン
def admin_login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM admin_sample WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            # SQLの結果からソルトを取得
            salt = user[1]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)

            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg