import random
import tkinter


class Constants:
    cellTypes = {"closed": 0, "open": 1}
    mineTypes = {"exists": 1, "safe": 0}
    selectionTypes = {"empty": " ", "flag": "!", "?": "?"}
    levels = {"easy": 0, "medium": 1, "hard": 2, "custom": 3}


def generate_mines(field, count):
    temp_field = field
    current_count = 0
    while True:
        for i in range(len(temp_field)):
            for j in range(len(temp_field[i])):
                if random.randint(0, count) == 1:
                    if current_count == count:
                        return temp_field
                    temp_field[i][j][1] = Constants.mineTypes[
                        "exists"]
                    current_count += 1


def generate_field(width, length):
    field = []
    for line in range(width):
        field.append([])
        for column in range(length):
            field[line].append([Constants.selectionTypes["empty"],
                                Constants.mineTypes["safe"], 0,
                                Constants.cellTypes["closed"]])
    return field


def calculate_bombs_around_count(field):
    temp_field = field
    for i in range(len(temp_field)):
        for j in range(len(temp_field[i])):
            if temp_field[i][j][1] == Constants.mineTypes["safe"]:
                current_result = 0
                if i > 0:
                    if j > 0:
                        if temp_field[i - 1][j - 1][1] == \
                                Constants.mineTypes["exists"]:
                            current_result += 1
                    if temp_field[i - 1][j][1] == \
                            Constants.mineTypes["exists"]:
                        current_result += 1
                    if j < len(temp_field[i - 1]) - 1:
                        if temp_field[i - 1][j + 1][1] == \
                                Constants.mineTypes["exists"]:
                            current_result += 1
                if i < len(temp_field) - 1:
                    if temp_field[i + 1][j][1] == \
                            Constants.mineTypes["exists"]:
                        current_result += 1
                    if j < len(temp_field[i + 1]) - 1:
                        if temp_field[i + 1][j + 1][1] == \
                                Constants.mineTypes["exists"]:
                            current_result += 1
                    if j > 0:
                        if temp_field[i + 1][j - 1][1] == \
                                Constants.mineTypes["exists"]:
                            current_result += 1
                if j < len(temp_field) - 1:
                    if temp_field[i][j + 1][1] == \
                            Constants.mineTypes["exists"]:
                        current_result += 1
                if j > 0:
                    if temp_field[i][j - 1][1] == \
                            Constants.mineTypes["exists"]:
                        current_result += 1
                temp_field[i][j][2] = current_result
    return temp_field


def open_cascade(field, i, j):
    if i > 0:
        if j > 0:
            if field[i - 1][j - 1][0] != field[i - 1][j - 1][2]:
                open_cell(None, field, i - 1, j - 1, lambda: True)
        if field[i - 1][j][0] != field[i - 1][j][2]:
            open_cell(None, field, i - 1, j, lambda: True)
        if j < len(field[i - 1]) - 1:
            if field[i - 1][j + 1][0] != field[i - 1][j + 1][2]:
                open_cell(None, field, i - 1, j + 1, lambda: True)
    if i < len(field) - 1:
        if field[i + 1][j][0] != field[i + 1][j][2]:
            open_cell(None, field, i + 1, j, lambda: True)
        if j < len(field[i + 1]) - 1:
            if field[i + 1][j + 1][0] != field[i + 1][j + 1][2]:
                open_cell(None, field, i + 1, j + 1, lambda: True)
        if j > 0:
            if field[i + 1][j - 1][0] != field[i + 1][j - 1][2]:
                open_cell(None, field, i + 1, j - 1, lambda: True)
    if j < len(field) - 1:
        if field[i][j + 1][0] != field[i][j + 1][2]:
            open_cell(None, field, i, j + 1, lambda: True)
    if j > 0:
        if field[i][j - 1][0] != field[i][j - 1][2]:
            open_cell(None, field, i, j - 1, lambda: True)


def open_cell(event, field, row, col, on_lose):
    print("open!")
    temp_field = field
    if temp_field[row][col][1] == Constants.mineTypes["exists"]:
        on_lose()
    else:
        temp_field[row][col][3] = Constants.cellTypes["open"]
        temp_field[row][col][0] = temp_field[row][col][2]
        if temp_field[row][col][2] == 0:
            open_cascade(field, row, col)
    return temp_field


def flag_cell(event, field, row, col):
    print("flag!")
    temp_field = field
    if temp_field[row][col][3] != Constants.cellTypes["open"]:
        if temp_field[row][col][0] == Constants.selectionTypes[
            "flag"]:
            temp_field[row][col][0] = Constants.selectionTypes["?"]
        elif temp_field[row][col][0] == Constants.selectionTypes[
            "?"]:
            temp_field[row][col][0] = Constants.selectionTypes[
                "empty"]
        else:
            temp_field[row][col][0] = Constants.selectionTypes[
                "flag"]
    return temp_field


def accorde(event, field, row, col):
    print("Unsupported")


def check_win(field):
    isWin = True
    for i in range(len(field)):
        for j in range(len(field[i])):
            if not (field[i][j][3] == Constants.cellTypes[
                "open"] or (field[i][j][1] == Constants.mineTypes[
                "exists"] and field[i][j][0] ==
                            Constants.selectionTypes["flag"])):
                isWin = False
    return isWin


def tick(field, ui):
    check_win(field)
    ui.update_field_by_matrix(field)
    ui.update()
