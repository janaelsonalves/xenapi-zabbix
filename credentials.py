import base64
import getpass
import json

credentials_file = "credentials.txt"

class Credentials:


    @staticmethod
    def encode():
        user = getpass.getpass('User:')
        password = getpass.getpass('Password:')
        user_e = base64.b64encode(user.encode("utf-8"))
        password_e = base64.b64encode(password.encode("utf-8"))
        
        with open(credentials_file, "w") as outfile:
            outfile.write(str(user_e))
            outfile.write("\n")
            outfile.write(str(password_e))


    @staticmethod
    def decode(value):
        return base64.b64decode(value)

def open_file(filename, mode):
    return open(filename, mode)

def save_data(file, data):
    file.write(json.dumps(data))

def get_data(file):
    return json.load(file)

if __name__ == "__main__":
    
    # user = getpass.getpass('User:')
    # password = getpass.getpass('Password:')
    # user_encoded = base64.b64encode(user.encode("utf-8"))
    # password_encoded = base64.b64encode(password.encode("utf-8"))

    # user_decoded = user_encoded.decode("utf-8")
    # password_decoded = password_encoded.decode("utf-8")

    # data = {
    #     "credentials": {
    #         "username": user_decoded,
    #         "password": password_decoded
    #     }
    # }

    # with open("data.json", "w") as f:
    #     f.write(json.dumps(data))

    # print(user_encoded, password_encoded)
    # print(data)

    f = open_file("data.json", "r")

    response = get_data(f)

    print (response["credentials"].get("username"))

    username = response["credentials"].get("username")

    other_encode = str.encode(username)

    print (other_encode)

    user_new = base64.decodebytes(other_encode)

    print (user_new.decode("utf-8"))


#     >>> string = 'data to be encoded'
# >>> data = base64.b64encode(string.encode())
# >>> print(data)
# b'ZGF0YSB0byBiZSBlbmNvZGVk'


    