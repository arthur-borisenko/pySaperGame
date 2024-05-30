import time

from game import generate_field, FullUI, PopupUI, generate_mines, \
    calculate_bombs_around_count, open_cell, tick, accorde, \
    flag_cell, Constants, LevelConfigUI

safe = False


def close_and_restart(popup):
    restart()
    popup.destroy()


def exit_button(popup):
    global ui
    ui.destroy_game()
    popup.destroy()


def lose_popup():
    #msg = PopupUI("you lose!", "сапер",
    #              ["restart", close_and_restart],
    #              ["exit", exit_button])
    global work
    print("you lose")
    ui.show_all_mines(f,Constants.mineTypes["exists"])
    work=False
    ui.mainloop()



def win_popup():
    #msg = PopupUI("you won!", "сапер",
    #              ["restart", close_and_restart],
     #             ["exit", exit_button])
    print("you won")
    exit_button(PopupUI)
_lvl = [[10, 10], 20]


def _restart(level_data):
    global f, work
    work = False
    time.sleep(3)
    f = generate_field(level_data[0][0], level_data[0][1])
    f = generate_mines(f, level_data[1])
    f = calculate_bombs_around_count(f)


def restart():
    _restart(_lvl)


def change_level(level_data):
    _lvl = level_data
    _restart(_lvl)


def pass_func():
    pass


def safe_open():
    global safe
    safe = True


def open_cell_override(e, f, i, j, lose):
    global safe
    on_lose = pass_func if safe else lose
    open_cell(e, f, i, j, on_lose)
    safe = False

def get_level_data(l,c):
    if l == c.levels["easy"]:
        return ((10,10),20)
    elif l == c.levels["medium"]:
        return ((20,30),50)
    elif l == c.levels["hard"]:
        return ((20,50),100)
    else:
        return LevelConfigUI().run()

f = generate_field(10, 10)
ui = FullUI(1000, 1100, f, 30, Constants, change_level, restart,safe_open,get_level_data)
ui.generate_field_by_matrix(f)
f = generate_mines(f, 20)
f = calculate_bombs_around_count(f)
work = True
ui.bind_field(f, open_cell_override, accorde, flag_cell, lose_popup)

while True:
    if work:
        tick(f, ui)
