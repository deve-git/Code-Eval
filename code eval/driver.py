from db_wrapper import DBWrapper
from prettytable import from_db_cursor


class Driver:
    db_wrapper = DBWrapper(
        "CREATE TABLE IF NOT EXISTS games (id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, publisher TEXT NOT "
        "NULL, year TEXT NOT NULL);")

    # Banner for cool 1337 points
    @staticmethod
    def banner():
        return r'''
=================================================
||    ____   ___  __  __ __  __  ____ ____     ||
||    || )) // \\ ||\ || ||\ || ||    || \\    ||
||    ||=)  ||=|| ||\\|| ||\\|| ||==  ||_//    ||
||    ||_)) || || || \|| || \|| ||___ || \\    ||
||                                             ||
=================================================
'''

    @staticmethod
    def generic_select():
        print("Options:")
        print("1 : add new game to your database")
        print("2 : search some games in your database")
        print("3 : delete a game from your database")
        print("4 : edit a game in your database")
        print("5 : list all games in your database")
        print("0 : exit")
        print("Type option number(0-5) and press [Enter]")
        opt = Driver.get_option_safe([str(i) for i in range(6)])
        link_array = [
            exit,
            Driver.add_game_step,
            Driver.search_game_step,
            Driver.delete_game_step,
            Driver.edit_game_step,
            Driver.list_game_step
        ]
        return link_array[int(opt)]

    @staticmethod
    def greetings_screen():
        print(Driver.banner())
        print("Hello, user!")
        print("Where does your journey continue?")
        return Driver.generic_select

    @staticmethod
    def get_option_safe(opts):
        selected = None
        while selected is None:
            opt = input().strip()
            if opt in opts:
                selected = opt
            else:
                print("Incorrect option number, try again")
        return selected

    @staticmethod
    def add_game_step():
        name = ""
        while name == "":
            name = input("Input game name:")

        publisher = ""
        while publisher == "":
            publisher = input("Input game publisher:")

        year = ""
        while year == "":
            year = input("Input game year:")

        Driver.db_wrapper.custom("INSERT INTO games (name,publisher,year) VALUES (?,?,?);", (name, publisher, year))
        return Driver.generic_select

    @staticmethod
    def search_game_step():
        name = input("Input game name (leave blank to not include in search):")
        publisher = input("Input game publisher (leave blank to not include in search):")
        year = input("Input game year (leave blank to not include in search):")

        query = "SELECT * FROM games WHERE "
        params = []
        if name != "":
            query = query + " name = ? AND"
            params.append(name)
        if publisher != "":
            query = query + " publisher = ? AND"
            params.append(publisher)
        if year != "":
            query = query + " year = ? AND"
            params.append(year)

        query = query[:-3] + ";"
        params = tuple(params)
        print(query, params)
        result = Driver.db_wrapper.select(query, params)
        my_table = from_db_cursor(result)
        print(my_table)

        return Driver.generic_select

    @staticmethod
    def delete_game_step():
        idt = ""
        while idt == "":
            idt = input("Input game id:")
        Driver.db_wrapper.custom("DELETE FROM games WHERE id = ?", (int(idt),))
        return Driver.generic_select

    @staticmethod
    def edit_game_step():
        idt = ""
        while idt == "":
            idt = input("Input game id:")

        result = Driver.db_wrapper.select("SELECT * FROM games WHERE id = ?;", (int(idt),))
        my_table = from_db_cursor(result)
        print(my_table)

        name = input("Input new game name (leave blank leave unchanged):")
        publisher = input("Input new game publisher (leave blank leave unchanged):")
        year = input("Input new game year (leave blank leave unchanged):")

        if name != "":
            Driver.db_wrapper.custom("UPDATE games SET name = ? WHERE id = ?", (name, int(idt)))
        if publisher != "":
            Driver.db_wrapper.custom("UPDATE games SET publisher = ? WHERE id = ?", (publisher, int(idt)))
        if year != "":
            Driver.db_wrapper.custom("UPDATE games SET year = ? WHERE id = ?", (year, int(idt)))

        return Driver.generic_select

    @staticmethod
    def list_game_step():

        result = Driver.db_wrapper.select("SELECT * FROM games;")
        my_table = from_db_cursor(result)
        print(my_table)

        return Driver.generic_select
