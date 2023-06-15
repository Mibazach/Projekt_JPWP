import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QShortcut
import sqlite3
import database_con

# TO DO
# three widgets' interfaces
# password encryption in the authentication system
# choose a better colour palette
# connection to a real cloud database


"""
Zakładam na razie takie dwie tabele z takimi kolumnami:

user: | user_id | login | password | create_time |
movie: | movie_id | title | year | type | poster | posted_by | 

"""


def next_widget():
    auth_widgets.setCurrentIndex(auth_widgets.currentIndex() + 1)


def prev_widget():
    auth_widgets.setCurrentIndex(auth_widgets.currentIndex() - 1)


def go_to_main():
    app_widgets.show()
    auth_widgets.hide()


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setGeometry(0, 0, 800, 550)
        auth_widgets.setWindowTitle("Welcome to Filmonator!")
        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 801, 551)
        self.widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.102, x2:1, "
                                  "y2:0.9375, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255));")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Filmonator", self.widget)
        self.label_title.move(180, 90)
        self.label_title.resize(550, 200)
        self.label_title.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0); font: "
                                       "72pt \"Pristina\";")

        self.label_username = QLabel("username", self.widget)
        self.label_username.move(213, 268)
        self.label_username.resize(140, 60)
        self.label_username.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_username = QLineEdit(self.widget)
        self.lineEdit_username.move(340, 280)
        self.lineEdit_username.resize(221, 45)
        self.lineEdit_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(255, 255, 255);")

        self.label_pass = QLabel("password", self.widget)
        self.label_pass.move(215, 338)
        self.label_pass.resize(140, 41)
        self.label_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                      "rgba(255, 255, 255, 0);")
        self.lineEdit_pass = QLineEdit(self.widget)
        self.lineEdit_pass.move(340, 340)
        self.lineEdit_pass.resize(221, 41)
        self.lineEdit_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                         "font: 11pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(255, 255, 255);")
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.login_button = QPushButton("log in", self.widget)
        self.login_button.move(400, 420)
        self.login_button.resize(93, 28)
        self.login_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, "
                                        "255); border-radius: 7px; border: 1px solid white; ")
        enter = QShortcut(Qt.Key_Return, self.login_button)
        enter.activated.connect(self.login_auth)
        self.login_button.clicked.connect(self.login_auth)
        self.no_account_button = QPushButton("no account? click here to create one", self.widget)
        self.no_account_button.move(-20, 515)
        self.no_account_button.resize(280, 28)
        self.no_account_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, "
                                             "255); text-decoration: underline;")
        self.no_account_button.clicked.connect(next_widget)

        self.label_err = QLabel("", self.widget)
        self.label_err.move(340, 383)
        self.label_err.resize(250, 28)
        self.label_err.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: red; background-color: "
                                     "rgba(255, 255, 255, 0);")

    def login_auth(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_pass.text()
        if len(username) == 0 and len(password) == 0:
            self.label_err.setText("The fields are empty")
        elif len(username) == 0 or len(password) == 0:
            self.label_err.setText("One of the fields is empty")

        else:  # bazodanowe logowanie tu trzeba
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            uname = f'"{username}"'
            my_cursor.execute(f'SELECT password FROM users WHERE username = {uname}')
            result = my_cursor.fetchone()
            mydb.close()
            if result is not None:
                stored_password = result[0]
                if stored_password == password:
                    self.label_err.setText("")
                    go_to_main()
            self.label_err.setText("Invalid username or password")
            self.lineEdit_pass.setText("")


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.setGeometry(0, 0, 800, 550)

        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 801, 551)
        self.widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.102, x2:1, "
                                  "y2:0.9375, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255));")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Create a new Filmonator account!", self.widget)
        self.label_title.move(180, 110)
        self.label_title.resize(600, 40)
        self.label_title.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                       "rgba(255, 255, 255, 0);")

        self.label_reg_username = QLabel("username", self.widget)
        self.label_reg_username.move(237, 200)
        self.label_reg_username.resize(121, 60)
        self.label_reg_username.setStyleSheet(
            "font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
            "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_username = QLineEdit(self.widget)
        self.lineEdit_reg_username.move(370, 210)
        self.lineEdit_reg_username.resize(221, 41)
        self.lineEdit_reg_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                                 "font: 11pt \"MS Shell Dlg 2\";\n"
                                                 "color: rgb(255, 255, 255);")

        self.label_reg_pass = QLabel("password", self.widget)
        self.label_reg_pass.move(240, 260)
        self.label_reg_pass.resize(121, 60)
        self.label_reg_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_pass = QLineEdit(self.widget)
        self.lineEdit_reg_pass.move(370, 270)
        self.lineEdit_reg_pass.resize(221, 41)
        self.lineEdit_reg_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(255, 255, 255);")
        self.lineEdit_reg_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.reg_button = QPushButton("register", self.widget)
        self.reg_button.move(430, 360)
        self.reg_button.resize(100, 30)
        self.reg_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, 255); "
                                      "border-radius: 7px; border: 1px solid white; font: 10pt \"MS Shell Dlg 2\"")
        self.reg_button.clicked.connect(self.reg_auth)

        self.label_reg_err = QLabel("", self.widget)
        self.label_reg_err.move(370, 310)
        self.label_reg_err.resize(250, 28)
        self.label_reg_err.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: red; background-color: "
                                         "rgba(255, 255, 255, 0);")

        self.back_to_login_button = QPushButton("back to logging in", self.widget)
        self.back_to_login_button.move(18, 515)
        self.back_to_login_button.resize(100, 28)
        self.back_to_login_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, "
                                                "255); text-decoration: underline;")
        self.back_to_login_button.clicked.connect(prev_widget)

        self.label_reg_success = QLabel("", self.widget)
        self.label_reg_success.move(240, 290)
        self.label_reg_success.resize(250, 28)
        self.label_reg_success.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: green; background-color: "
                                             "rgba(255, 255, 255, 0);")

    def reg_auth(self):
        username = self.lineEdit_reg_username.text()
        password = self.lineEdit_reg_pass.text()
        if len(username) == 0 and len(password) == 0:
            self.label_reg_err.setText("The fields are empty")
        elif len(username) == 0 or len(password) == 0:
            self.label_reg_err.setText("One of the fields is empty")
        elif len(username) > 50:
            self.label_reg_err.setText("Username length must be < 50 chars")
        elif len(password) > 50:
            self.label_reg_err.setText("Password length must be < 50 chars")

        else:  # bazodanowe logowanie tu trzeba
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            my_cursor.execute("SELECT username FROM users")
            list_of_users = my_cursor.fetchall()
            if (username,) in list_of_users:  # zwraca mi tuple (tupla skurwysyna)
                self.label_reg_err.setText("This username exists!")
            else:
                query = "INSERT INTO users (username, password, create_time) VALUES (%s, %s, CURRENT_TIMESTAMP)"
                my_cursor.execute(query, (username, password))
                mydb.commit()
                mydb.close()
                self.label_reg_err.clear()
                self.label_reg_success.setText("You registered successfully")


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        app_widgets.setWindowTitle("Filmonator")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget = QWidget()

        self.bar = QWidget()
        self.bar.setGeometry(-1, -1, 1000, 100)
        self.bar.setStyleSheet("background-color: black")
        self.bar_layout = QVBoxLayout()
        self.bar_layout.addWidget(self.bar, stretch=1)
        self.bar.setLayout(QVBoxLayout())
        self.label_bar_title = QLabel("Filmonator", self.bar)
        self.label_bar_title.resize(350, 107)
        self.label_bar_title.setStyleSheet("background-color: rgba(255, 255, 255, 0);font: 50pt \"Pristina\"; color: "
                                           "white")

        self.home_but = QPushButton("", self.bar)
        self.home_but.move(780, 10)
        self.home_but.resize(60, 60)
        home_ico = QIcon('resources/icons/home.png')
        self.home_but.setIcon(home_ico)
        icon_size = QSize(self.home_but.size().width() - 5, self.home_but.size().height() - 5)
        self.home_but.setIconSize(icon_size)

        self.search_but = QPushButton("", self.bar)
        self.search_but.move(850, 10)
        self.search_but.resize(60, 60)
        search_ico = QIcon('resources/icons/search.png')
        self.search_but.setIcon(search_ico)
        self.search_but.setIconSize(icon_size)

        self.profile_but = QPushButton("", self.bar)
        self.profile_but.move(920, 10)
        self.profile_but.resize(60, 60)
        profile_ico = QIcon('resources/icons/profile.png')
        self.profile_but.setIcon(profile_ico)
        self.profile_but.setIconSize(icon_size)

        self.layout.addWidget(self.bar, stretch=1)

        self.wall = QtWidgets.QStackedWidget()
        self.wall.setGeometry(-1, 91, 1000, 650)
        self.wall.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba("
                                "0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255))")
        self.wall_layout = QVBoxLayout()
        self.wall_layout.addWidget(self.wall, stretch=9)
        self.wall.setLayout(QVBoxLayout())
        self.layout.addWidget(self.wall, stretch=9)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.home_view = QWidget()
        self.home_view_label = QLabel("Home view", self.home_view)
        self.home_view_label.setStyleSheet("font: 50pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                           "background-color: rgba(255, 255, 255, 0);")
        self.home_view_label.move(100, 100)
        self.wall.addWidget(self.home_view)
        self.home_but.clicked.connect(lambda: self.wall.setCurrentWidget(self.home_view))
        #
        #

        self.search_view = QWidget()
        self.search_view_label = QLabel("Search view", self.search_view)
        self.search_view_label.setStyleSheet("font: 50pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                             "background-color: rgba(255, 255, 255, 0);")
        self.search_view_label.move(200, 200)
        self.wall.addWidget(self.search_view)
        self.search_but.clicked.connect(lambda: self.wall.setCurrentWidget(self.search_view))
        #
        #

        self.profile_view = QWidget()
        self.profile_view_label = QLabel("Profile view", self.profile_view)
        self.profile_view_label.setStyleSheet("font: 50pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                              "background-color: rgba(255, 255, 255, 0);")
        self.profile_view_label.move(300, 300)
        self.wall.addWidget(self.profile_view)
        self.profile_but.clicked.connect(lambda: self.wall.setCurrentWidget(self.profile_view))


app = QApplication(sys.argv)
auth_widgets = QtWidgets.QStackedWidget()
auth_widgets.setFixedWidth(800)
auth_widgets.setFixedHeight(550)
auth_widgets.show()

log_scr = LoginWindow()
auth_widgets.addWidget(log_scr)
reg_scr = RegisterWindow()
auth_widgets.addWidget(reg_scr)

app_widgets = QtWidgets.QStackedWidget()
app_widgets.setFixedWidth(1000)
app_widgets.setFixedHeight(750)
auth_widgets.show()

main_scr = MainApp()
app_widgets.addWidget(main_scr)

sys.exit(app.exec_())
