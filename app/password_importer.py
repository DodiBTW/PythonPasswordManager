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
    def import_passwords_from_csv(self, file_path, user_id):
        if not os.path.exists(file_path):
            logging.error("File does not exist")
            return
        if file_path.endswith('.csv'):
            file = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            file = pd.read_excel(file_path)
        else:
            logging.error("File type not supported")
            return
        for x, row in file.iterrows():
            print(f"Lecture de la ligne {x}")
            username = row['username']
            password = row['password']
            if 'site' in row:
                site = row['site']
            else:
                site = None
            password = self.encrypt_password(password)
            if self.password_handler.password_exists(user_id, site):
                self.password_handler.add_password(user_id, password, site)
            else:
                self.password_handler.modify_password(user_id, password, site)
    def import_password_from_json(self, file_path):
        if not os.path.exists(file_path):
            logging.error("File does not exist")
            return
        if not file_path.endswith('.json'):
            logging.error("File type not supported")
            return
        with open(file_path, 'r') as file:
            data = json.load(file)
        for x, row in enumerate(data):
            print(f"Lecture de la ligne {x}")
            username = row['username']
            password = row['password']
            if 'site' in row:
                site = row['site']
            else:
                site = None
            password = self.encrypt_password(password)
            self.db_handler.register(username, password, site)
    def encrypt_password(self, password):
        return Fernet(self.key).encrypt(password.encode()).decode()
    def decrypt_password(self, password):
        return Fernet(self.key).decrypt(password.encode()).decode()