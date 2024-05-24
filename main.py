import time

from game import generate_field, MainUi, PopupUI, generate_mines, \
    calculate_bombs_around_count, open_cell, tick, accorde, \
    flag_cell, Constants

f = generate_field(10, 10)
ui = MainUi(1000, 1100, f, 40, Constants)
ui.generate_field_by_matrix(f)
work = True


def close_and_restart(popup):
    global work
    work = False
    time.sleep(1)
    start()
    popup.destroy()


def exit_button(popup):
    global ui
    ui.destroy()
    popup.destroy()


def lose_popup():
    msg = PopupUI("you lose!", "сапер",
                  ["restart", close_and_restart],
                  ["exit", exit_button])


def win_popup():
    msg = PopupUI("you won!", "сапер",
                  ["restart", close_and_restart],
                  ["exit", exit_button])


def start():
    global f
    f = generate_field(10, 10)
    ui.generate_field_by_matrix(f)
    f = generate_mines(f, 20)
    f = calculate_bombs_around_count(f)
    ui.update_field_by_matrix(f)
    ui.bind_field(f, open_cell, accorde, flag_cell, lose_popup)


start()
while work:
    tick(f, ui)
