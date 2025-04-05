import base64
import gzip
import sqlite3
from os import getcwd

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key(password: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"\x6a\x55\x53\x6a\x42\x2b\x35\x71\x51\x50\x72\x50\x2f\x34\x61\x66\x4d\x52\x34\x67\x71\x43\x79\x7a\x5a\x70\x51\x64\x65\x5a\x35\x6a\x70\x52\x67\x33\x63\x35\x39\x4f\x56\x63\x47\x53\x5a\x62\x42\x6a\x41\x42\x68\x4a\x51\x54\x51\x57\x41\x6b\x43\x50\x6b\x70\x32\x42\x48\x31\x6f\x52\x2b\x63\x65\x4f\x55\x45\x7a\x79",
        iterations=1024,
        backend=default_backend(),
    )
    key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
    return key


def encryption(b, password):
    f = generate_key(password)
    safe = f.encrypt(b)
    return safe


def decryption(safe, password):
    f = generate_key(password)
    b = f.decrypt(safe)
    return b


def open_db(name, password):
    f = gzip.open(getcwd() + "/" + name + "_crypted.sql.gz", "rb")
    safe = f.read()
    f.close()
    content = decryption(safe, password)
    content = content.decode("utf-8")
    con = sqlite3.connect(":memory:")
    con.executescript(content)
    return con


def save_db(con, name, password):
    fp = gzip.open(getcwd() + "/" + name + "_crypted.sql.gz", "wb")
    b = b""
    for line in con.iterdump():
        b += bytes("%s\n", "utf8") % bytes(line, "utf8")
    b = encryption(b, password)
    fp.write(b)
    fp.close()
