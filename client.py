import pickle
import re


class Client_Validation_Exception(Exception):
    pass


class InvalidNameError(Client_Validation_Exception):
    pass


class InvalidNumberError(Client_Validation_Exception):
    pass


class InvalidEmailError(Client_Validation_Exception):
    pass


class InvalidPasswordError(Client_Validation_Exception):
    pass


class Validate_Input_Data:
    @staticmethod
    def validate_name(ipname):
        inpname = "".join((ipname).split())
        if not re.search("^[a-zA-Z][a-zA-Z]*$", inpname):
            return False
        return True

    @staticmethod
    def validate_phone(ipnumber):
        if not re.search("[0-9]{10}", ipnumber):
            return False
        return True

    @staticmethod
    def validate_email(ipemail):
        pattern = r"^[a-zA-Z0-9._%+-]+@outlook\.com$"
        if re.match(pattern, ipemail):
            return True
        return False

    @staticmethod
    def validate_pass(ippass):
        if len(ippass) > 7:
            if not re.search("[a-z]", ippass):
                return False
            if not re.search("[A-Z]", ippass):
                return False
            if not re.search("[0-9]", ippass):
                return False
            return True
        return False

    @staticmethod
    def Client_Validation(ipname, ipnumber, ipemail, ippass):
        if not Validate_Input_Data.validate_name(ipname):
            raise InvalidNameError("Invalid name")

        if not Validate_Input_Data.validate_phone(ipnumber):
            raise InvalidNumberError("Invalid phone number")

        if not Validate_Input_Data.validate_email(ipemail):
            raise InvalidEmailError("Invalid email")

        if not Validate_Input_Data.validate_pass(ippass):
            raise InvalidPasswordError("Invalid password")

        return True


class Client_DB_Support:
    @staticmethod
    def store_client(client):
        client_db_file = "client_data_file.pickle"
        infile = open(client_db_file, "ab")
        pickle.dump(client, infile)
        infile.close()

    @staticmethod
    def get_all_clients():
        client_db_file = "client_data_file.pickle"
        clients = []
        try:
            file = open(client_db_file, "rb")
            while True:
                try:
                    client = pickle.load(file)
                    clients.append(client)
                except EOFError:
                    file.close()
                    break
        except FileNotFoundError:
            print(f"File '{client_db_file}' not found.")
        return clients

    @staticmethod
    def check_client_credential(ipemail, ippassword):
        clients = Client_DB_Support.get_all_clients()
        for client in clients:
            if client._email == ipemail:
                if client._password == ippassword:
                    return True
        return False


class Client:
    @staticmethod
    def create_client(name, phone, email, password):
        Validate_Input_Data.Client_Validation(name, phone, email, password)
        Client(name, phone, email, password)

    def __init__(self, name, phone, email, password):
        self._name = name
        self._phone = phone
        self._email = email
        self._password = password
        Client_DB_Support.store_client(self)
