import tkinter as tk


class LevelConfigUI(tk.Tk):
    def __init__(self):
        self._lcui_run = True

        def _lcui_stop():
            self._lcui_run = False

        super().__init__()
        form = tk.Frame(self)
        self.title("level configure - pySaperGame v1.1 alpha")
        self.geometry("800x400")
        tk.Label(form, text="Field width:").grid(row=0, column=0)
        tk.Label(form, text="Field height:").grid(row=1, column=0)
        tk.Label(form, text="Mines count:").grid(row=2, column=0)
        self.w = tk.Entry(form)
        self.h = tk.Entry(form)
        self.c = tk.Entry(form)
        self.s = tk.Button(self, text="ok", command=_lcui_stop)
        self.w.grid(row=0, column=1)
        self.h.grid(row=1, column=1)
        self.c.grid(row=2, column=1)
        form.pack(side=tk.TOP)
        self.s.pack()

    def run(self):
        while self._lcui_run:
            self.update()
        return (self.w.get(), self.h.get()), self.c.get()


class PopupUI(tk.Tk):
    def __init__(self, msg, name, *buttons):
        super().__init__()
        self.title(name)
        self.geometry('500x150')
        label = tk.Label(self, text=msg)
        label.pack(anchor=tk.CENTER)
        for button in buttons:
            button_obj = tk.Button(self, text=button[0],
                                   command=lambda popup=self: button[
                                       1](popup))
            button_obj.pack(side=tk.BOTTOM)
        try:
            self.mainloop()
        except tk.TclError:
            pass


class GameUi(tk.Tk):
    def __init__(self, width, height, field, size, constants):
        super().__init__()
        self.constants = constants
        self.nk = []
        grid_width = len(field[0])
        grid_height = len(field)
        self.title('сапер')
        self.size = size
        self.geometry(f"{width}x{height}")
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.field = tk.Frame(self, width=grid_width * size,
                              height=grid_height * size,
                              borderwidth=1)

    def generate_field_by_matrix(self, matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                current_el = matrix[i][j]
                self.field.grid_columnconfigure(j, minsize=self.size)
                self.field.grid_rowconfigure(i, minsize=self.size)
                current = tk.Button(self.field, text=current_el[0])
                current.grid(row=i, column=j, sticky="nsew")
                self.nk.append([i, j, current])

    def update_field_by_matrix(self, matrix):
        for el in self.nk:
            el[2].configure(text=matrix[el[0]][el[1]][0])

    def show_all_mines(self, f, mine_symbol):
        for cell in self.nk:
            i = cell[0]
            j = cell[1]
            if f[i][j][1] == self.constants.mineTypes["exists"]:
                cell[2].configure(text=f[i][j][0] + mine_symbol)

    def bind_field(self, field, method1, method2, method3, on_lose):
        def on_lose_2(ui, fieldd):
            self.show_all_mines(fieldd, "*")
            on_lose()

        for el in self.nk:
            el[2].bind("<Button-1>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method1(event, f, x,
                                               y, lambda
                                                   ui=self: on_lose_2(
                               ui, field)))
            el[2].bind("<Button-2>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method2(event, f, x,
                                               y))
            el[2].bind("<Button-3>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method3(event, f, x,
                                               y))


class FullUI(GameUi):
    def destroy_game(self):
        self.destroy()
        exit('Game was exited')

    def __init__(self, width, height, field, size, constants,
                 change_level, restart, cheat_safe_open,
                 get_level_data):
        super().__init__(width, height, field, size, constants)
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        level_menu = tk.Menu(main_menu, tearoff=0)
        level_menu.add_command(label="easy",
                               command=lambda: change_level(
                                   get_level_data(
                                       constants.levels["easy"],
                                       constants)))
        level_menu.add_command(label="medium",
                               command=lambda: change_level(
                                   get_level_data(
                                       constants.levels["medium"],
                                       constants)))
        level_menu.add_command(label="hard",
                               command=lambda: change_level(
                                   get_level_data(
                                       constants.levels["hard"],
                                       constants)))
        level_menu.add_command(label="custom",
                               command=lambda: change_level(
                                   get_level_data(
                                       constants.levels["custom"],
                                       constants)))
        cheats_menu = tk.Menu(main_menu, tearoff=0)
        cheats_menu.add_command(label="safe open",
                                command=cheat_safe_open)
        file_menu = tk.Menu(main_menu, tearoff=0)
        file_menu.add_command(label="restart", command=restart)
        file_menu.add_command(label="exit",
                              command=self.destroy_game)
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="level", menu=level_menu)
        main_menu.add_cascade(label="cheats", menu=cheats_menu)
        self.field.pack(side=tk.TOP, expand=True)


if __name__ == '__main__':
    import api

    ui = FullUI(1000, 1000, [
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]]],
                40,
                api.Constants,
                print,
                lambda: print("restart"),
                lambda: print("cheat"),
                lambda l, c: print(l))
    ui.generate_field_by_matrix([
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]],
        [[' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0], [' ', 0, 0, 0], [' ', 0, 0, 0],
         [' ', 0, 0, 0]]])
    while True:
        ui.update()
