# 🤜🏻 FilmonatorTM 🤛🏻

*"Remember to watch good movies"*

Filmonator to projekt zaliczeniowy stworzony przez Jakuba Godulę oraz Michała Łobazę na zajęcia z języków programowania wysokiego poziomu. Projekt ten to prosta aplikacja GUI, która pozwala na łączenie się zdalne z serwerem MySQL, utworzenie konta użytkownika oraz dodawanie do swojej bazy filmów, których cechy zwracane są przez określone zapytanie do API. 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
## 👇 Zadania do rozwiązania 👇 
<br>
Informacje dotyczące inicjalizowania bazy danych oraz potrzebnych bibliotek zostały podane wcześniej, jeżeli napotkałeś jakiś problem to zgłoś to do nas - twórców projektu.
Potrzebne będzie: połączenie VPN z siecią AGH, konto serwera poczty AGH, IDE obsługujące Pythona oraz Python, najlepiej w wersji najnowszej.

## Zadanie nr 1
Stwórz połączenie z bazą danych poprzez kod napisany w języku Python. 
<br>
Podpowiedź: aby sprawdzić czy połączyłeś się z bazą możesz zastosować klauzulę try: ze zwracanym wyjątkiem mysql.connecor.errrs.DatabaseError, gdyby coś poszło nie tak.
## Zadanie nr 2
Teraz utwórz zapytanie do bazy. Stwórz tablicę o nazwie 'jpwp' zawierającą pola: 'id_grupy' o cechach klucza głównego i typie int,  'ocena' o cesze nie pozwalającej być pustą i typie int o długości 10 bajtów, 'komentarz' o typie text z regułą sortowania utf8_polish_ci. Zweryfikuj czy tablica została dodana do bazy danych poprzez panel phpMyAdmin. Nie zapomnij o .commit()! Jeżeli udało Ci się wykonać zadanie, wykasuj zapytanie w kodzie.
## Zadanie nr 3
Utwórz kolejne zapytanie. Tym razem do wcześniej utworzonej tablicy spróbuj dodać kolumnę 'opinia', której typ to varchar o długości 50 bajtów. Nowa kolumna znajdować musi się za kolumną 'komentarz'. Zweryfikuj czy tablica została dodana do bazy danych poprzez panel phpMyAdmin.
## Zadanie nr 4
Napisz przy użyciu PyQt5 (modułu QtWidgets) interfejs podobny do tego na obrazkach. Po naciśnięciu na przycisk danego koloru tło powinno się zmienić na ten kolor. Okno ma mieć na początku czarne tło. 
(Podpowiedź: CSS Style Sheets)

![image](https://github.com/Mibazach/Projekt_JPWP_v2/assets/115176038/785bcc66-97fc-47df-8827-4bb7a6abf781)
![image](https://github.com/Mibazach/Projekt_JPWP_v2/assets/115176038/1770a3ee-0548-4707-9beb-f45fee58935a)
![image](https://github.com/Mibazach/Projekt_JPWP_v2/assets/115176038/6fef3362-89b5-4718-b6dd-a01ae92501a3)
