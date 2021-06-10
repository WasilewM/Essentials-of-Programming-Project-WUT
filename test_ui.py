from ui import UserInterface


def test_ui_init(monkeypatch):
    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    ui = UserInterface()
    assert len(ui.database().flights()) == 0
    assert len(ui.database().planes()) == 0
    assert len(ui.database().passengers()) == 0
    assert len(ui.database().tickets()) == 0

    assert ui.default_files()['flights'] == 'flights_database.csv'
    assert ui.default_files()['passengers'] == 'passengers_database.csv'
    assert ui.default_files()['planes'] == 'planes_database.csv'
    assert ui.default_files()['tickets'] == 'tickets_database.csv'


def test_ui_get_main_menu_options(monkeypatch):
    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    correct = """Choose option - type number 0-15
0. Add data from predefined files
1. Add new flight
2. Add new plane
3. Add new ticket
4. Add new passenger
5. Show existing flights
6. Show existing planes
7. Show existing tickets
8. Show existing passengers
9. Print boarding pass
10. Change passenger seat
11. Ask for assistant
12. Thank assistant for help
13. Check departure gate
14. Check flight parameters
15. Exit
If you want to close the program instantly please enter Ctrl + D"""
    ui = UserInterface()
    assert ui.get_main_menu_options() == correct


def test_ui_collect_data_to_create_flight_valid(monkeypatch):
    def return_one(arg):
        return 1

    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    monkeypatch.setattr('ui.UserInterface.get_user_input_int', return_one)
    ui = UserInterface()
    assert ui.collect_data_to_create_flight() == 1


def test_create_boarding_pass(monkeypatch):
    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    ui = UserInterface()
    data = {
        'ticket id': 1,
        'first name': 'Lara',
        'last name': 'Croft',
        'plane number': 1,
        'seat class': 'business',
        'seat number': 1,
        'gate number': 1
    }
    boarding_pass = ui.create_table(data)
    correct = """------------------------------
| ticket id    |           1 |
------------------------------
| first name   |        Lara |
------------------------------
| last name    |       Croft |
------------------------------
| plane number |           1 |
------------------------------
| seat class   |    business |
------------------------------
| seat number  |           1 |
------------------------------
| gate number  |           1 |
------------------------------
"""
    assert correct == boarding_pass


def test_check_departure_gate(monkeypatch):
    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    ui = UserInterface()
    data = {'departure gate': 1}
    result = ui.create_table(data)
    correct = """----------------------------------
| departure gate |             1 |
----------------------------------
"""

    assert result == correct


def test_check_flights_param(monkeypatch):
    def not_run(arg):
        pass

    monkeypatch.setattr('ui.UserInterface._run', not_run)
    ui = UserInterface()
    ui.load_default_files()

    data = {
        'flight number': 1,
        'plane type': 'wide-body',
        'number of business class seats': 50,
        'number of economy class seats': 200,
        'carrier name': 'LOT'
    }
    table = ui.create_table(data)

    correct = """------------------------------------------------------------------
| flight number                  |                             1 |
------------------------------------------------------------------
| plane type                     |                     wide-body |
------------------------------------------------------------------
| number of business class seats |                            50 |
------------------------------------------------------------------
| number of economy class seats  |                           200 |
------------------------------------------------------------------
| carrier name                   |                           LOT |
------------------------------------------------------------------
"""

    assert table == correct
