import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QShortcut
import sqlite3


# TO DO
# three widgets' interfaces
# password encryption in the authentication system
# choose a better colour palette
# connection to a real cloud database


def next_widget():
    auth_widgets.setCurrentIndex(auth_widgets.currentIndex() + 1)


def prev_widget():
    auth_widgets.setCurrentIndex(auth_widgets.currentIndex() - 1)


def go_to_main():
    app_widgets.show()
    auth_widgets.hide()


def go_to_home():
    auth_widgets.setCurrentIndex(3)


def go_to_search():
    auth_widgets.setCurrentIndex(4)


def go_to_profile():
    auth_widgets.setCurrentIndex(5)


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setGeometry(0, 0, 600, 500)
        auth_widgets.setWindowTitle("Welcome to Filmonator!")
        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 601, 501)
        self.widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.102, x2:1, "
                                  "y2:0.9375, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255));")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Filmonator", self.widget)
        self.label_title.move(130, 90)
        self.label_title.resize(360, 110)
        self.label_title.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0); font: "
                                       "72pt \"Pristina\";")

        self.label_username = QLabel("username", self.widget)
        self.label_username.move(66, 280)
        self.label_username.resize(100, 41)
        self.label_username.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_username = QLineEdit(self.widget)
        self.lineEdit_username.move(170, 280)
        self.lineEdit_username.resize(221, 41)
        self.lineEdit_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(255, 255, 255);")

        self.label_pass = QLabel("password", self.widget)
        self.label_pass.move(70, 340)
        self.label_pass.resize(121, 41)
        self.label_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                      "rgba(255, 255, 255, 0);")
        self.lineEdit_pass = QLineEdit(self.widget)
        self.lineEdit_pass.move(170, 340)
        self.lineEdit_pass.resize(221, 41)
        self.lineEdit_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                         "font: 11pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(255, 255, 255);")
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.login_button = QPushButton("log in", self.widget)
        self.login_button.move(300, 420)
        self.login_button.resize(93, 28)
        self.login_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, "
                                        "255); border-radius: 7px; border: 1px solid white; ")
        enter = QShortcut(Qt.Key_Return, self.login_button)
        enter.activated.connect(self.login_auth)
        self.login_button.clicked.connect(self.login_auth)
        self.no_account_button = QPushButton("no account? click here to create one", self.widget)
        self.no_account_button.move(10, 470)
        self.no_account_button.resize(180, 28)
        self.no_account_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, "
                                             "255); text-decoration: underline;")
        self.no_account_button.clicked.connect(next_widget)

        self.label_err = QLabel("", self.widget)
        self.label_err.move(170, 380)
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
            conn = sqlite3.connect("baza.db")
            cursor = conn.cursor()
            query = 'SELECT password FROM users WHERE username =\'' + username + "\'"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
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
        self.setGeometry(0, 0, 600, 500)

        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 601, 501)
        self.widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0.102, x2:1, "
                                  "y2:0.9375, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255));")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Create a new Filmonator account!", self.widget)
        self.label_title.move(130, 90)
        self.label_title.resize(600, 40)
        self.label_title.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                       "rgba(255, 255, 255, 0);")

        self.label_reg_username = QLabel("username", self.widget)
        self.label_reg_username.move(136, 190)
        self.label_reg_username.resize(100, 41)
        self.label_reg_username.setStyleSheet(
            "font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
            "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_username = QLineEdit(self.widget)
        self.lineEdit_reg_username.move(240, 190)
        self.lineEdit_reg_username.resize(221, 41)
        self.lineEdit_reg_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                                 "font: 11pt \"MS Shell Dlg 2\";\n"
                                                 "color: rgb(255, 255, 255);")

        self.label_reg_pass = QLabel("password", self.widget)
        self.label_reg_pass.move(140, 250)
        self.label_reg_pass.resize(121, 41)
        self.label_reg_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_pass = QLineEdit(self.widget)
        self.lineEdit_reg_pass.move(240, 250)
        self.lineEdit_reg_pass.resize(221, 41)
        self.lineEdit_reg_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(255, 255, 255);")
        self.lineEdit_reg_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.reg_button = QPushButton("register", self.widget)
        self.reg_button.move(305, 340)
        self.reg_button.resize(100, 30)
        self.reg_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(255, 255, 255); "
                                      "border-radius: 7px; border: 1px solid white; font: 10pt \"MS Shell Dlg 2\"")
        self.reg_button.clicked.connect(self.reg_auth)

        self.label_reg_err = QLabel("", self.widget)
        self.label_reg_err.move(240, 290)
        self.label_reg_err.resize(250, 28)
        self.label_reg_err.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: red; background-color: "
                                         "rgba(255, 255, 255, 0);")

        self.back_to_login_button = QPushButton("back to logging in", self.widget)
        self.back_to_login_button.move(10, 470)
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

        else:  # bazodanowe logowanie tu trzeba
            conn = sqlite3.connect("baza.db")
            cursor = conn.cursor()
            query = 'INSERT INTO users (username, password, create_time) VALUES (?, ?, CURRENT_TIMESTAMP)'
            cursor.execute(query, (username, password))
            conn.commit()
            conn.close()
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
        self.bar.setGeometry(-1, -1, 1000, 90)
        self.bar.setStyleSheet("background-color: red")
        self.bar_layout = QVBoxLayout()
        self.bar_layout.addWidget(self.bar, stretch=1)
        self.bar.setLayout(QVBoxLayout())
        self.label_bar_title = QLabel("Filmonator", self.bar)
        self.label_bar_title.resize(300, 91)
        self.label_bar_title.setStyleSheet("background-color: rgba(255, 255, 255, 0);font: 56pt \"Pristina\"; color: "
                                           "white")

        self.home_but = QPushButton("", self.bar)
        self.home_but.move(780, 10)
        self.home_but.resize(60, 60)
        home_ico = QIcon('resources/icons/home.png')
        self.home_but.setIcon(home_ico)
        icon_size = QSize(self.home_but.size().width()-5, self.home_but.size().height()-5)
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

        self.wall = QWidget()
        self.wall.setGeometry(-1, 91, 1000, 660)
        self.wall.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba("
                                "0, 0, 0, 255), stop:1 rgba(158, 158, 158, 255))")
        self.wall_layout = QVBoxLayout()
        self.wall_layout.addWidget(self.wall, stretch=9)
        self.wall.setLayout(QVBoxLayout())
        self.layout.addWidget(self.wall, stretch=9)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


app = QApplication(sys.argv)
auth_widgets = QtWidgets.QStackedWidget()
auth_widgets.setFixedWidth(600)
auth_widgets.setFixedHeight(500)
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
