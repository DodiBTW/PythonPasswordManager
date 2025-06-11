import pandas as pd
import numpy as np
import os
import sys
import json
import re
import logging
from app import db
from app.db.passwords_handler import PasswordsHandler
from cryptography.fernet import Fernet

class PasswordImporter:
    def __init__(self, key):
        self.password_handler = PasswordsHandler(key)
        self.key = key
    def import_passwords_from_csv(self, file, user_id):
        for x, row in file.iterrows():
            site = row['site']
            username = row['username']
            password = row['password']
            password = self.encrypt_password(password)
            self.password_handler.add_password(user_id ,username,site , password)
    def import_password_from_json(self, file, user_id):
        for x, row in enumerate(file):
            print(f"Lecture de la ligne {x}")
            username = row['username']
            password = row['password']
            if 'site' in row:
                site = row['site']
            else:
                site = None
            password = self.encrypt_password(password)
            self.password_handler.add_password(user_id ,username,site , password)
    def encrypt_password(self, password):
        return Fernet(self.key).encrypt(password.encode()).decode()
    def decrypt_password(self, password):
        return Fernet(self.key).decrypt(password.encode()).decode()