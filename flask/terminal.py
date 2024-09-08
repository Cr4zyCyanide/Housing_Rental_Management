from sql import *
import hashlib

db = Database(
    host="127.0.0.1",
    user="ynx",
    passwd="2333",
    db_name="rental_mng")

# pwd_hash_layer1 = hashlib.sha256("123456".encode("utf-8")).hexdigest()
# l2 = hashlib.sha3_512(("salt" + pwd_hash_layer1).encode("utf-8")).hexdigest()
#
# print(pwd_hash_layer1, l2)

print(db.getAllRentalInfo('yang'))
