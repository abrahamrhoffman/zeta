from ConfigParser import SafeConfigParser
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import pathlib
import base64
import shutil
import glob
import uuid
import os


class Database(object):


    #### Private Methods ####

    def __init__(self, bootstrap=False):
        self._init_cVars()
        if bootstrap: self._bootstrap()
        if not self._check_keys():
            print("Database keys not present in path. Check folder: {}"
                  .format(os.getcwd() + "/" + self._path))

    def _init_cVars(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self._db_folder = parser.get("database", "default_folder")
        self._path = self._db_folder
        self._admin_username = parser.get("database", "admin_username")
        self._admin_secret = parser.get("database", "admin_secret")
        self._secret = self._admin_secret
        self._admin_email = parser.get("database", "admin_email")
        self._admin_password = parser.get("database", "admin_password")
        self._initial_table_name = parser.get("database", "initial_table_name")
        self._dbPriv = (self._path + "/" + "." + self._path + ".priv")
        self._dbPub = (self._path + "/" + "." + self._path + ".pub")

    def _create_uuid(self):
        aUuid = str(uuid.uuid4()).replace("-", "")
        return aUuid

    def _check_keys(self):
        dbPriv = pathlib.Path(self._dbPriv)
        dbPub = pathlib.Path(self._dbPub)
        if dbPriv.is_file() and dbPub.is_file():
            return True
        else:
            return False

    def _create_keys(self):
        dbPriv = (self._dbPriv)
        dbPub = (self._dbPub)
        key = RSA.generate(2048)
        encrypted_key = key.exportKey(passphrase=self._secret, pkcs=8,
                                      protection="scryptAndAES128-CBC")
        with open(dbPriv, 'wb') as f:
            f.write(encrypted_key)
        with open(dbPub, 'wb') as f:
            f.write(key.publickey().exportKey())

    def _encrypt(self, aTableName):
        readPath = (self._path + "/" + aTableName + ".pq")
        writePath = (self._path + "/" + aTableName + ".enc")
        with open(writePath, 'wb') as out_file:
            recipient_key = RSA.import_key(open(self._dbPub).read())
            session_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            out_file.write(cipher_rsa.encrypt(session_key))
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = \
                cipher_aes.encrypt_and_digest(pa.memory_map(readPath).read())
            out_file.write(cipher_aes.nonce)
            out_file.write(tag)
            out_file.write(ciphertext)
        os.remove(readPath)

    def _decrypt(self, tableFile):
        encTableFile = tableFile.replace("pq", "enc")
        with open(encTableFile, 'r') as fobj:
            private_key = \
                RSA.import_key(open(self._dbPriv).read(),passphrase=self._secret)
            enc_session_key, nonce, tag, ciphertext = \
                [fobj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        with open(tableFile, "w+") as f:
            f.write(data)
        with open(tableFile, "r") as f:
            fileData = f.read()
        return fileData


    def _purge(self):
        # Purge database folder and recreate folders and keys!
        try: shutil.rmtree(self._path)
        except: pass
        try: os.makedirs(self._path)
        except: pass
        self._create_keys()

    def _bootstrap(self):
        # Recreate database folders and keys
        self._purge()
        # Create the initial users table
        pqFile = (self._initial_table_name + ".pq")
        # Define table
        tableFile = (self._path + "/" + pqFile)
        # Check user input first
        if not ("@") in self._admin_email:
            return ("Invalid Email address: {}".format(self._admin_email))

        # Create database table as file
        try:
            f = open(tableFile, "w+")
            f.close()
        except:
            print("Database creation failed. Check Path: {}"
                  .format(tableFile))

        # Create the initial user with details
        uid = self._create_uuid()
        username = [self._admin_username]
        email = [self._admin_email]
        password = [self._admin_password]
        password = base64.b64encode(password[0])

        # Create dataframe
        aDict = {"uid": uid,
                 "username": username,
                 "email": email,
                 "password": password,
                 "admin": True}
        aTable = pd.DataFrame(aDict)
        # Arrange columns
        cols = ["uid", "username", "email", "password", "admin"]
        aTable = aTable.loc[:, cols]

        # Fill database with initial information
        try: self.write(aTable, self._initial_table_name)
        except: print("Initial db creation failed. Check _bootstrap method.")


    #### Public Methods ####

    def tables(self):
        t = glob.glob(self._path + "/*")
        tables = [ele.split("/")[-1].split(".")[0] for ix, ele in enumerate(t)]
        return tables

    def create(self, aTableName, aDict, order=None):
        # Creating new tables requires a dict with keys as lists
        # Example ::
        #    my_list0 = [1,2,3]
        #    my_list1 = [3,4,5]
        #    my_dict = {"my_list0": my_list0,
        #               "my_list1", my_list1}
        #    # Instantiate database with folder and secret
        #    db = Database(folder="my_folder",
        #                  secret="my_secret")
        #    db.create("newTable", my_dict)
        #    # Order is a list of columns that you would like ordered
        #    # Example: order = ["my_list1", "my_list0"]
        #    db.create("newTable", my_dict, order=order)
        table = pd.DataFrame(aDict)
        if order:
            table = table.loc[:, order]
        self.write(table, aTableName)

    def read(self, aTableName):
        try:
            tableFile = (self._path + "/" + aTableName + ".pq")
            self._decrypt(tableFile)
            dataframe = pq.read_table(tableFile).to_pandas()
            os.remove(tableFile)
            return dataframe
        except:
            return ("File not present. Check path: {}"
                    .format(tableFile))

    def write(self, aDataFrame, aTableName):
        tableFile = (self._path + "/" + aTableName + ".pq")
        table = pa.Table.from_pandas(aDataFrame)
        pq.write_table(table, tableFile)
        self._encrypt(aTableName)
