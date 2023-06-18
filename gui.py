import sys
import mysql.connector.errors
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QShortcut,\
    QSizePolicy, QHBoxLayout, QGridLayout, QScrollArea, QTextEdit
import database_con
import hashlib
import api_functionality

# TO DO
# nothing label in profile_view

"""
Zakładam na razie takie dwie tabele z takimi kolumnami:

users: | user_id | login | password | create_time |
movies: | movie_id | title | year | type | poster | posted_by | 

"""

global current_logged_user
current_logged_user = None


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
        self.a = None
        self.setGeometry(0, 0, 800, 550)
        auth_widgets.setWindowTitle("Welcome to Filmonator!")
        auth_widgets.setWindowIcon(QIcon('resources/icons/app_icon.png'))
        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 801, 551)
        self.widget.setStyleSheet("#widget{background-image: url('resources/background.png');}")
        self.widget.setObjectName("widget")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Filmonator", self.widget)
        self.label_title.move(180, 90)
        self.label_title.resize(550, 200)
        self.label_title.setStyleSheet("color: rgb(0, 0, 0); background-color: rgba(255, 255, 255, 0); font: "
                                       "72pt \"Pristina\";")

        self.label_username = QLabel("username", self.widget)
        self.label_username.move(213, 268)
        self.label_username.resize(140, 60)
        self.label_username.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(0, 0, 0); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_username = QLineEdit(self.widget)
        self.lineEdit_username.move(340, 280)
        self.lineEdit_username.resize(221, 45)
        self.lineEdit_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(0, 0, 0);")

        self.label_pass = QLabel("password", self.widget)
        self.label_pass.move(215, 338)
        self.label_pass.resize(140, 41)
        self.label_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(0, 0, 0); background-color: "
                                      "rgba(255, 255, 255, 0);")
        self.lineEdit_pass = QLineEdit(self.widget)
        self.lineEdit_pass.move(340, 340)
        self.lineEdit_pass.resize(221, 41)
        self.lineEdit_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                         "font: 11pt \"MS Shell Dlg 2\";\n"
                                         "color: rgb(0, 0, 0);")
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.login_button = QPushButton("log in", self.widget)
        self.login_button.move(400, 420)
        self.login_button.resize(93, 28)
        self.login_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(0, 0, "
                                        "0); border-radius: 7px; border: 1px solid white; ")
        enter = QShortcut(Qt.Key_Return, self.login_button)
        enter.activated.connect(self.login_auth)
        self.login_button.clicked.connect(self.login_auth)
        self.no_account_button = QPushButton("no account? click here to create one", self.widget)
        self.no_account_button.move(55, 515)
        self.no_account_button.resize(280, 28)
        self.no_account_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(0, 0, "
                                             "0); text-decoration: underline;")
        self.no_account_button.clicked.connect(next_widget)

        self.label_err = QLabel("", self.widget)
        self.label_err.move(340, 383)
        self.label_err.resize(250, 28)
        self.label_err.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: red; background-color: "
                                     "rgba(255, 255, 255, 0);")
        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        shortcut.activated.connect(self.close_application)

    def login_auth(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_pass.text()
        if len(username) == 0 and len(password) == 0:
            self.label_err.setText("The fields are empty")
        elif len(username) == 0 or len(password) == 0:
            self.label_err.setText("One of the fields is empty")

        else:
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            uname = f'"{username}"'
            my_cursor.execute(f'SELECT password FROM users WHERE username = {uname}')
            result = my_cursor.fetchone()
            mydb.close()
            if result is not None:
                stored_password = result[0]
                if stored_password == hashlib.md5(password.encode()).hexdigest():
                    self.label_err.setText("")
                    global current_logged_user
                    current_logged_user = uname
                    go_to_main()
            self.label_err.setText("Invalid username or password")
            self.lineEdit_pass.setText("")

    def close_application(self):
        self.a = None
        auth_widgets.close()


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.a = None
        self.setGeometry(0, 0, 800, 550)

        self.widget = QWidget()
        self.widget.setGeometry(-1, -1, 801, 551)
        self.widget.setStyleSheet("#widget{background-image: url('resources/background.png');}")
        self.widget.setObjectName("widget")
        self.setCentralWidget(self.widget)

        self.label_title = QLabel("Create a new Filmonator account!", self.widget)
        self.label_title.move(180, 110)
        self.label_title.resize(600, 40)
        self.label_title.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: rgb(0, 0, 0); background-color: "
                                       "rgba(255, 255, 255, 0);")

        self.label_reg_username = QLabel("username", self.widget)
        self.label_reg_username.move(237, 200)
        self.label_reg_username.resize(121, 60)
        self.label_reg_username.setStyleSheet(
            "font: 16pt \"MS Shell Dlg 2\"; color: rgb(0, 0, 0); background-color: "
            "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_username = QLineEdit(self.widget)
        self.lineEdit_reg_username.move(370, 210)
        self.lineEdit_reg_username.resize(221, 41)
        self.lineEdit_reg_username.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
                                                 "font: 11pt \"MS Shell Dlg 2\";\n"
                                                 "color: rgb(0, 0, 0);")

        self.label_reg_pass = QLabel("password", self.widget)
        self.label_reg_pass.move(240, 260)
        self.label_reg_pass.resize(121, 60)
        self.label_reg_pass.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(0, 0, 0); background-color: "
                                          "rgba(255, 255, 255, 0);")
        self.lineEdit_reg_pass = QLineEdit(self.widget)
        self.lineEdit_reg_pass.move(370, 270)
        self.lineEdit_reg_pass.resize(221, 41)
        self.lineEdit_reg_pass.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 11pt \"MS Shell Dlg 2\";\n"
                                             "color: rgb(0, 0, 0);")
        self.lineEdit_reg_pass.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki

        self.reg_button = QPushButton("register", self.widget)
        self.reg_button.move(430, 360)
        self.reg_button.resize(100, 30)
        self.reg_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(0, 0, 0); "
                                      "border-radius: 7px; border: 1px solid white; font: 10pt \"MS Shell Dlg 2\"")
        self.reg_button.clicked.connect(self.reg_auth)

        self.label_reg_err = QLabel("", self.widget)
        self.label_reg_err.move(370, 310)
        self.label_reg_err.resize(250, 28)
        self.label_reg_err.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: red; background-color: "
                                         "rgba(255, 255, 255, 0);")

        self.back_to_login_button = QPushButton("back to logging in", self.widget)
        self.back_to_login_button.move(93, 515)
        self.back_to_login_button.resize(100, 28)
        self.back_to_login_button.setStyleSheet("background-color: rgb(255, 255, 255, 0); color: rgb(0, 0, "
                                                "0); text-decoration: underline;")
        self.back_to_login_button.clicked.connect(prev_widget)

        self.label_reg_success = QLabel("", self.widget)
        self.label_reg_success.move(370, 310)
        self.label_reg_success.resize(250, 28)
        self.label_reg_success.setStyleSheet("font: 10pt \"MS Shell Dlg 2\"; color: green; background-color: "
                                             "rgba(255, 255, 255, 0);")
        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        shortcut.activated.connect(self.back_to_login)

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

        else:
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            my_cursor.execute("SELECT username FROM users")
            list_of_users = my_cursor.fetchall()
            if (username,) in list_of_users:  # zwraca mi tuple (tupla skurwysyna)
                self.label_reg_err.setText("This username exists!")
            else:
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                print(password, type(password))
                query = 'INSERT INTO users (username, password, create_time) VALUES (%s, %s, CURRENT_TIMESTAMP)'
                my_cursor.execute(query, (username, password))
                mydb.commit()
                mydb.close()
                self.label_reg_err.clear()
                self.label_reg_success.setText("You registered successfully")
                self.lineEdit_reg_username.setText("")
                self.lineEdit_reg_pass.setText("")

    def back_to_login(self):
        self.a = None
        auth_widgets.setCurrentIndex(auth_widgets.currentIndex() - 1)


def close_application():
    app_widgets.close()


class MainApp(QMainWindow):
    def __init__(self):
        self.movie = None
        self.add_template = None
        self.search_result = None
        super(MainApp, self).__init__()
        app_widgets.setWindowIcon(QIcon('resources/icons/app_icon.png'))
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

        self.wall.setStyleSheet("background-color: black;")
        self.wall_layout = QVBoxLayout()
        self.wall_layout.addWidget(self.wall, stretch=9)
        self.wall.setLayout(QVBoxLayout())
        self.layout.addWidget(self.wall, stretch=9)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.home_view = QScrollArea()
        self.home_view.setWidgetResizable(True)
        self.home_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.label_nothing = QLabel("", self.home_view)
        self.label_nothing.move(130, 90)
        self.label_nothing.resize(360, 110)
        self.label_nothing.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: white; "
                                         "background-color: rgba(255, 255, 255, 0);")
        self.home_view_widget = QWidget()
        self.home_view_layout = QVBoxLayout(self.home_view_widget)
        self.home_view_layout.setContentsMargins(0, 0, 0, 0)
        self.home_view_layout.setSpacing(0)
        self.home_view.setWidget(self.home_view_widget)
        self.layout = QVBoxLayout(self.home_view)
        self.home_view.setLayout(self.layout)

        self.show_all_saved_movies()

        self.wall.addWidget(self.home_view)
        self.home_but.clicked.connect(self.show_home)

        self.search_view = QWidget()
        self.layout = QVBoxLayout(self.search_view)
        self.search_view.setLayout(self.layout)

        self.searchbar_label = QLabel("Search for a movie:", self.search_view)
        self.searchbar_label.setStyleSheet("font: 24pt \"MS Shell Dlg 2\"; color: white; "
                                           "background-color: rgba(255, 255, 255, 0);")
        self.searchbar_label.move(330, 100)
        self.searchbar_label.adjustSize()
        self.lineEdit_searchbar = QLineEdit(self.search_view)
        self.lineEdit_searchbar.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: white; "
                                              "background-color: rgba(255, 255, 255, 0);")
        self.lineEdit_searchbar.setAlignment(Qt.AlignCenter)
        self.lineEdit_searchbar.resize(600, 100)
        self.lineEdit_searchbar.move(200, 160)
        self.search_button = QPushButton(self.search_view)
        self.search_button.move(700, 160)
        self.search_button.resize(100, 100)
        self.search_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        search_ico = QIcon('resources/icons/search.png')
        self.search_button.setIcon(search_ico)
        search_button_size = QSize(100, 100)
        self.search_button.setIconSize(search_button_size)
        self.enter = QShortcut(Qt.Key_Return, self.search_button)
        self.enter.activated.connect(lambda: self.update_search_result())
        self.search_button.clicked.connect(lambda: self.update_search_result())

        self.nf_label = QLabel("", self.search_view)
        self.nf_label.move(400, 280)
        self.nf_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\"; color: red; "
                                    "background-color: rgba(255, 255, 255, 0);")
        self.nf_label.adjustSize()

        self.wall.addWidget(self.search_view)
        self.search_but.clicked.connect(self.show_search_view)

        self.profile_view = QScrollArea()
        self.profile_view.setWidgetResizable(True)
        self.profile_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.label_nothing_in_prof = QLabel("", self.profile_view)
        self.label_nothing_in_prof.move(130, 90)
        self.label_nothing_in_prof.resize(360, 110)
        self.label_nothing_in_prof.setStyleSheet("font: 20pt \"MS Shell Dlg 2\"; color: white; "
                                                 "background-color: rgba(255, 255, 255, 0);")
        self.profile_view_widget = QWidget()
        self.profile_view_layout = QVBoxLayout(self.profile_view_widget)
        self.profile_view_layout.setContentsMargins(0, 0, 0, 0)
        self.profile_view_layout.setSpacing(0)
        self.profile_view.setWidget(self.profile_view_widget)
        self.profile_layout = QVBoxLayout(self.profile_view)
        self.profile_view.setLayout(self.profile_layout)

        self.show_all_user_current_user_movies()

        self.wall.addWidget(self.profile_view)
        self.profile_but.clicked.connect(self.show_profile)

        self.mas_view = QWidget()
        self.mas_label = QLabel("Adding", self.mas_view)
        self.mas_label.move(460, 0)
        self.mas_label.resize(81, 121)
        self.mas_label.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                     "background-color: rgba(255, 255, 255, 0);")
        self.mas_label_2 = QLabel("to your library", self.mas_view)
        self.mas_label_2.move(417, 140)
        self.mas_label_2.resize(171, 121)
        self.mas_label_2.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                       "background-color: rgba(255, 255, 255, 0);")
        self.mas_title_label = QLabel("", self.mas_view)
        self.mas_title_label.move(10, 70)
        self.mas_title_label.resize(981, 121)
        self.mas_title_label.setStyleSheet("font: 28pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                           "background-color: rgba(255, 255, 255, 0);")
        self.mas_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mas_label_3 = QLabel("Your rating:", self.mas_view)
        self.mas_label_3.move(60, 230)
        self.mas_label_3.resize(160, 121)
        self.mas_label_3.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                       "background-color: rgba(255, 255, 255, 0);")
        self.mas_label_3 = QLabel("Your review:", self.mas_view)
        self.mas_label_3.move(60, 310)
        self.mas_label_3.resize(160, 121)
        self.mas_label_3.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                       "background-color: rgba(255, 255, 255, 0);")
        self.mas_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.mas_view)
        self.mas_slider.setMinimum(0)
        self.mas_slider.setMaximum(10)
        self.mas_slider.setSingleStep(1)
        self.mas_slider.move(220, 270)
        self.mas_slider.resize(640, 41)
        self.mas_slider.setStyleSheet("color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0);")
        self.mas_slider_value_label = QLabel(str(self.mas_slider.value()), self.mas_view)
        self.mas_slider_value_label.move(880, 250)
        self.mas_slider_value_label.resize(71, 71)
        self.mas_slider_value_label.setStyleSheet("font: 36pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                                  "background-color: rgba(255, 255, 255, 0);")
        self.mas_slider.valueChanged.connect(self.update_label_value)
        self.mas_textedit = QTextEdit(self.mas_view)
        self.mas_textedit.move(230, 350)
        self.mas_textedit.resize(630, 170)
        self.mas_textedit.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); background-color: "
                                        "rgba(255, 255, 255, 0);")
        self.character_limit = 200
        self.mas_textedit.textChanged.connect(self.limit_characters)
        self.mas_submit_but = QPushButton(self.mas_view)
        self.mas_submit_but.setText("Submit")
        self.mas_submit_but.move(660, 560)
        self.mas_submit_but.resize(220, 60)
        self.mas_submit_but.setStyleSheet("font: 24pt \"MS Shell Dlg 2\"; color: rgb(255, 255, 255); "
                                          "background-color: rgba(255, 255, 255, 0); border-radius: 7px; border: 2px "
                                          "solid white; ")

        self.mas_submit_but.clicked.connect(lambda: self.handle_submit_button_click(self.movie, str(self.mas_slider.value())+'/10', str(self.mas_textedit.toPlainText())))

        self.mas_label_submitted = QLabel("", self.mas_view)
        self.mas_label_submitted.move(300, 560)
        self.mas_label_submitted.resize(300, 61)
        self.mas_label_submitted.setStyleSheet("font: 16pt \"MS Shell Dlg 2\"; color: green; "
                                               "background-color: rgba(255, 255, 255, 0);")
        self.wall.addWidget(self.mas_view)

        shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        shortcut.activated.connect(close_application)

    def limit_characters(self):
        cursor = self.mas_textedit.textCursor()
        text = self.mas_textedit.toPlainText()

        if len(text) > self.character_limit:
            cursor.deletePreviousChar()
            self.mas_textedit.setTextCursor(cursor)

    def update_label_value(self, value):
        self.mas_slider_value_label.setText(str(value))

    def show_home(self):
        self.label_nothing.setText("")
        self.clear_movies()
        self.wall.setCurrentWidget(self.home_view)
        self.show_all_saved_movies()

    def show_profile(self):
        self.label_nothing_in_prof.setText("")
        self.clear_movies_in_prof()
        self.wall.setCurrentWidget(self.profile_view)
        self.show_all_user_current_user_movies()

    def update_search_result(self):
        self.search_result = api_functionality.find_movies(self.lineEdit_searchbar.text())
        self.display_search_result()

    def display_search_result(self):
        if self.search_result:
            self.nf_label.setText("")
            self.nf_label.adjustSize()
            self.clear_buttons()
            spacer_widget = QWidget()
            spacer_widget.setFixedHeight(250)
            spacer_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            self.layout.addWidget(spacer_widget)
            self.layout.setAlignment(Qt.AlignCenter)
            for movie in self.search_result:
                print(movie)
                title = movie['Title']
                year = movie['Year']
                if len(title) > 25:
                    short_title = title[0:30] + "..."
                else:
                    short_title = title
                button_text = f"{short_title} ({year})"
                button = QPushButton(button_text)
                button.setToolTip(title)
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button.setMaximumWidth(400)
                button.setMaximumHeight(50)
                button.setFixedWidth(400)
                button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: white; "
                                     "background-color: rgba(255, 255, 255, 0); border: 1px solid white;")
                button_container = QWidget()
                button_container_layout = QHBoxLayout()
                button_container.setLayout(button_container_layout)
                button_container_layout.addWidget(button)
                button_container_layout.setContentsMargins(0, 0, 0, 0)
                add_button = QPushButton()
                add_button.setIcon(QIcon("resources/icons/plus.png"))
                add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                add_button.setFixedWidth(50)
                add_button.setFixedHeight(30)
                add_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: none;")
                add_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color: white; "
                                         "background-color: rgba(255, 255, 255, 0); border: 2px solid white;")
                add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button_container_layout.addWidget(add_button)
                self.layout.setSpacing(7)
                self.layout.addWidget(button_container)
                button.clicked.connect(lambda checked, moviee=movie: self.handle_button_click(moviee))
                add_button.clicked.connect(lambda checked, moviee=movie: self.handle_add_button_click(moviee))
        else:
            self.nf_label.setText("Nothing found.")
            self.nf_label.adjustSize()
            self.clear_buttons()

    def handle_submit_button_click(self, movie, rating, review):
        self.mas_slider.setValue(0)
        self.mas_textedit.setText("")
        print('wejscie do handle')
        self.mas_label_submitted.setText("Successfully submitted!")
        print('aa')
        api_functionality.add_movie_to_db(current_logged_user, movie, rating, review)
        print("AAAA!!")

    def handle_add_button_click(self, movie):
        self.mas_title_label.setText(movie['Title'])
        self.mas_label_submitted.setText("")
        self.wall.setCurrentWidget(self.mas_view)
        self.movie = movie
        # self.add_template = MovieTemplate(movie['Title'], movie['Year'], current_logged_user,
        #                                  '0', "aaa", movie['Poster'])
        # self.home_view_layout.addWidget()

    def handle_button_click(self, movie):
        self.clear_movies()
        self.show_all_movie_by_title(movie['Title'])
        self.wall.setCurrentWidget(self.home_view)

    def clear_buttons(self):
        while self.layout.count() > 0:
            item = self.layout.itemAt(0)
            if isinstance(item.widget(), QPushButton):
                button = item.widget()
                self.layout.removeWidget(button)
                button.deleteLater()
            else:
                self.layout.removeItem(item)

    def clear_movies(self):
        while self.home_view_layout.count():
            item = self.home_view_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def clear_movies_in_prof(self):
        while self.profile_view_layout.count():
            item = self.profile_view_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_search_view(self):
        self.wall.setCurrentWidget(self.search_view)
        self.lineEdit_searchbar.setFocus()

    def show_all_saved_movies(self):
        self.label_nothing.setText("")
        try:
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            my_cursor.execute('SELECT * FROM movies')
            list_of_movies = my_cursor.fetchall()
            print(list_of_movies, type(list_of_movies))
            for movie in list_of_movies:
                title = movie[1]
                year = movie[2]
                poster_path = movie[4]
                author = movie[5]
                rating = movie[7]
                review = movie[8]
                self.home_view_layout.addWidget(MovieTemplate(title, year, author, rating, review, poster_path, False))
        except mysql.connector.errors.DatabaseError:
            print('Coś poszło nie tak z wyświetlaniem...')

    def show_all_movie_by_title(self, title):
        try:
            title = f"'{title}'"
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            my_cursor.execute(f'SELECT * FROM movies WHERE title = {title}')
            list_of_movies = my_cursor.fetchall()
            mydb.close()
            if len(list_of_movies) == 0:
                self.label_nothing.setText("No user added that movie to their profile! ...yet.")
                self.label_nothing.adjustSize()
                print('No user added that movie to their profile! ...yet.')
                return
            self.label_nothing.setText("")
            print(list_of_movies, type(list_of_movies))
            for movie in list_of_movies:
                title = movie[1]
                year = movie[2]
                poster_path = movie[4]
                author = movie[5]
                rating = movie[7]
                review = movie[8]
                self.home_view_layout.addWidget(MovieTemplate(title, year, author, rating, review, poster_path, False))
        except mysql.connector.errors.DatabaseError:
            print('Coś poszło nie tak z wyświetlaniem...')

    def show_all_user_current_user_movies(self):
        try:
            mydb = database_con.data_base_connect()
            my_cursor = mydb.cursor()
            my_cursor.execute(f'SELECT * FROM movies WHERE posted_by = {current_logged_user}')
            list_of_movies = my_cursor.fetchall()
            mydb.close()
            if len(list_of_movies) == 0:
                self.label_nothing_in_prof.setText("Nothing to see here... yet.")
                self.label_nothing_in_prof.adjustSize()
                print('Nothing to see here... yet.')
                return
            print(list_of_movies, type(list_of_movies))
            for movie in list_of_movies:
                title = movie[1]
                year = movie[2]
                poster_path = movie[4]
                author = movie[5]
                rating = movie[7]
                review = movie[8]
                self.profile_view_layout.addWidget(MovieTemplate(title, year, author, rating,
                                                                 review, poster_path, True))
        except mysql.connector.errors.DatabaseError:
            print('Coś poszło nie tak z wyświetlaniem...')

    # def delete_this_movie(self, movie):
    #     try:
    #         mydb = database_con.data_base_connect()
    #         my_cursor = mydb.cursor()
    #         title = movie[1]
    #         query = f'DELETE FROM movies WHERE title = %s AND username = %s'
    #         my_cursor.execute(query, (title, current_logged_user))
    #         mydb.close()
    #     except mysql.connector.errors.DatabaseError:
    #         print('Coś poszło nie tak z usuwaniem...')


def delete_this_movie(title):
    try:
        username = current_logged_user.strip('"')
        #username = current_logged_user
        mydb = database_con.data_base_connect()
        my_cursor = mydb.cursor()
        query = "DELETE FROM movies WHERE title = '"+str(title)+"' AND posted_by = '"+str(username)+"'"
        print(query)
        my_cursor.execute(query)
        print(query)
        print("Review of "+title+" by "+username+" deleted.")
        mydb.commit()
        mydb.close()
        main_scr.show_profile()
    except mysql.connector.errors.DatabaseError:
        print('Coś poszło nie tak z usuwaniem...')


class MovieTemplate(QWidget):
    def __init__(self, title, year, author, rating, review, poster_path, delete_bool, parent=None):
        super().__init__(parent)
        self.title = title
        self.year = year
        self.author = author
        self.rating = rating
        self.review = review
        self.poster_path = poster_path
        self.delete_bool = delete_bool
        self.init()

    def init(self):
        main_layout = QHBoxLayout(self)
        poster_label = QLabel(self)
        response = requests.get(self.poster_path)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        poster_label.setPixmap(pixmap)
        poster_label.setMaximumSize(300, 447)

        container_widget = QWidget(self)
        container_widget.setFixedHeight(447)

        container_layout = QGridLayout(container_widget)

        title_label = QLabel(f"\'{self.title}\' ({self.year})")
        if not self.delete_bool:
            container_layout.addWidget(title_label, 0, 0)
        title_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\"; color: white; "
                                  "background-color: rgba(255, 255, 255, 0); border: 1px solid white;")
        if self.delete_bool:
            title_layout = QHBoxLayout()
            title_layout.addWidget(title_label)
            del_button = QPushButton()
            container_layout.addWidget(del_button, 0, 0)
            profile_ico = QIcon('resources/icons/trash.png')
            icon_size = QSize(80, 50)
            del_button.setIcon(profile_ico)
            del_button.setIconSize(icon_size)
            del_button.setStyleSheet("font: 18pt \"MS Shell Dlg 2\"; color: white; "
                                     "background-color: rgba(255, 255, 255, 0); border: 1px solid white;")
            title_layout.addWidget(del_button)
            container_layout.addLayout(title_layout, 0, 0)
            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            del_button.setSizePolicy(size_policy)
            del_button.clicked.connect(lambda: delete_this_movie(self.title))

        rating_label = QLabel(f"Rating: {self.rating}")
        container_layout.addWidget(rating_label, 1, 0)
        rating_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\"; color: white; "
                                   "background-color: rgba(255, 255, 255, 0); border: 1px solid white;")

        author_label = QLabel(f"Author: {self.author}")
        container_layout.addWidget(author_label, 2, 0)
        author_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\"; color: white; "
                                   "background-color: rgba(255, 255, 255, 0); border: 1px solid white;")

        review_label = QLabel(f"Review: \"{self.review}\"")
        container_layout.addWidget(review_label, 3, 0)
        review_label.setWordWrap(True)
        review_label.setAlignment(Qt.AlignJustify)
        review_label.setStyleSheet("font: 14pt \"MS Shell Dlg 2\"; color: white; "
                                   "background-color: rgba(255, 255, 255, 0); border: 1px solid white; "
                                   "word-wrap: break-word; padding-left: 10px; padding-right: 10px; "
                                   "padding-top: 10px; padding-bottom: 10px")

        main_layout.addWidget(poster_label)
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)


app = QApplication(sys.argv)
auth_widgets = QtWidgets.QStackedWidget()
auth_widgets.setFixedWidth(800)
auth_widgets.setFixedHeight(550)
auth_widgets.show()

log_scr = LoginWindow()
auth_widgets.addWidget(log_scr)
reg_scr = RegisterWindow()
auth_widgets.addWidget(reg_scr)
auth_widgets.setWindowFlag(Qt.FramelessWindowHint)

app_widgets = QtWidgets.QStackedWidget()
app_widgets.setFixedWidth(1000)
app_widgets.setFixedHeight(750)
auth_widgets.show()
app_widgets.setWindowFlag(Qt.FramelessWindowHint)

main_scr = MainApp()
app_widgets.addWidget(main_scr)

sys.exit(app.exec_())
