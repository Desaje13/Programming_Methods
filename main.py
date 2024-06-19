# Класс "Пользователь"
class User:
    def __init__(self, proxy):
        self.proxy = proxy

    login_data = None

    def login(self, login, password):
        self.login_data = (login, password)

    def access(self):
        self.proxy.check_login(self)


# Класс "Прокси"
class Proxy:
    def __init__(self, server, db):
        self.server = server
        self.Data_Base = db

    def check_login(self, user):
        if user.login_data in self.Data_Base.logins:
            print("correct login")
            self.server.return_urls()
            print("Type 'login' to relogin: ")
        else:
            print("wrong login details")
            # print(user.login_data)
            self.server.return_first_url()
            print("Type 'login' to relogin: ")


# Класс "Сервер"
class Server:
    urls = ["https://bricscouncil.hse.ru/announcements/910744358.html",
            "https://lang.hse.ru/announcements/915163499.html",
            "https://oriental.hse.ru/chinesestudies/announcements/919965132.html",
            "https://anr.hse.ru/announcements/917512733.html",
            "https://www.hse.ru/ma/therapy/announcements/896070860.html",
            "https://gsb.hse.ru/ma/announcements/915919477.html",
            "https://medieval.hse.ru/announcements/919733457.html",
            "https://bioelectric.hse.ru/neuroschool2024/",
            "https://demogr.hse.ru/announcements/917090358.html",
            "https://ikm.hse.ru/mpc/announcements/920793032.html"]

    def return_urls(self):
        print("you received all urls")
        for url in self.urls:
            print(url)

    def return_first_url(self):
        print("you received only first url, please login to see all")
        print(self.urls[0])


# Класс, где хранятся данные на основе паттерна singleton
class Login_Database():
    logins = []

    def __init__(self):
        with open("DB.csv", "r") as db:
            for line in db:
                line = line.split(";")
                login = line[1]
                password = line[2]
                password = password.replace("\n", "")
                self.logins.append((login, password))


serv = Server()
DB = Login_Database()
# print(DB.logins)
prox = Proxy(serv, DB)
user = User(prox)

# print("Press any key to continue...")
while True:
    if (user.login_data is None):
        print("Please login to view all information")
        user_login = input("login:")
        user_password = input("Password:")
        user.login(user_login, user_password)
        user.access()

    message = input()
    # print(user.login)
    if message == "exit":
        break

    if message == "login":
        user_login = input("login:")
        user_password = input("Password:")
        user.login(user_login, user_password)
        user.access()
