import tkinter as tk


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


class MainUi(tk.Tk):
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
        self.field.pack(side=tk.TOP, expand=True)

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
                cell[2].configure(text=mine_symbol)

    def bind_field(self, field, method1, method2, method3, on_lose):
        for el in self.nk:
            el[2].bind("<Button-1>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method1(event, f, x,
                                               y, on_lose))
            el[2].bind("<Button-2>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method2(event, f, x,
                                               y))
            el[2].bind("<Button-3>",
                       lambda event, f=field, x=el[0],
                              y=el[1]: method3(event, f, x,
                                               y))
