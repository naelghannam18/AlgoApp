import sqlite3 as sq
import os
import hashlib
import uuid

DATABASE_NAME = 'LOGS.db'

def createDatabse():
    if os.path.isfile(DATABASE_NAME):
        pass
    else:
        conn = sq.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("""
                     CREATE TABLE CAESER_CIPHER(
                     ID INTEGER PRIMARY KEY,
                     OPTION_TYPE TEXT,
                     CIPHER TEXT,
                     KEY INTEGER,
                     MESSAGE TEXT,
                     TIMESTAMP TEXT
                  )""")
        c.execute("""
                     CREATE TABLE RAILFENCE(
                     ID INTEGER PRIMARY KEY,
                     OPTION_TYPE TEXT,
                     PASSWORD TEXT,
                     CIPHER TEXT,
                     MESSAGE TEXT,
                     TIMESTAMP TEXT
                  )""")
        c.execute("""
                     CREATE TABLE CREDENTIALS(
                     ID INTEGER PRIMARY KEY,    
                     USERNAME TEXT,
                     SALT BLOB,
                     PASSWORD BLOB,
                     EMAIL TEXT,
                     RGB_PATTERN TEXT,
                     PICTURE_ORDER TEXT             
                   )""")
        conn.commit()
        conn.close()

def add_Caeser_cipher(alType, cipher, key, message, timestamp):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO CAESER_CIPHER (OPTION_TYPE, CIPHER, KEY, MESSAGE, TIMESTAMP) VALUES (?,?,?,?,?)",
                 (alType, cipher, key, message, timestamp,))
    conn.commit()
    conn.close()

def add_RailFence(type, password, cipher, message, timestamp):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO RAILFENCE (OPTION_TYPE, PASSWORD, CIPHER, MESSAGE, TIMESTAMP) VALUES (?,?,?,?,?)",
              (type, password, cipher, message, timestamp))
    conn.commit()
    conn.close()

def get_CaeserCipherLog():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CAESER_CIPHER")
    logs = c.fetchall()
    conn.close()
    return logs

def get_RailFenceLog():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM RAILFENCE")
    logs = c.fetchall()
    conn.close()
    return logs

def clear_all_logs():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM CAESER_CIPHER")
    c.execute("DELETE FROM RAILFENCE")
    conn.commit()
    conn.close()

def get_CaeserCipherLogPerID(id):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CAESER_CIPHER WHERE ID = (?)", (id),)
    log = c.fetchone()
    return log

def get_RailFenceLogPerID(id):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM RAILFENCE WHERE ID = (?)", (id,))
    log = c.fetchone()
    return log

def createUser(username, password, email, RGB, PictureOrder):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    encodedPass = str(password).encode()
    salt = uuid.uuid4().bytes
    hashedpass = hashlib.sha512(encodedPass+salt).digest()
    c.execute("INSERT INTO CREDENTIALS (USERNAME, SALT, PASSWORD, EMAIL, RGB_PATTERN, PICTURE_ORDER) VALUES (?,?,?,?,?,?)"
              ,(username,salt, hashedpass, email, RGB, PictureOrder,))
    conn.commit()
    conn.close()

def defaultUserExists():
    conn=sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CREDENTIALS")
    values = c.fetchall()
    return len(values) != 0

def validate(username, password):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CREDENTIALS WHERE USERNAME = (?)", (username,))
    v = c.fetchall()
    if len(v) == 0:
        return False
    else:
        salt = v[0][2]
        encodedPassword = str(password).encode()
        hashedPassword = hashlib.sha512(encodedPassword+salt).digest()
        return v[0][3] == hashedPassword

def removeUser():
    conn=sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM CREDENTIALS")
    conn.commit()
    conn.close()

def getUser():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CREDENTIALS WHERE ID = 1")
    v = c.fetchall()
    return v