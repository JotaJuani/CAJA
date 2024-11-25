from tkinter import Tk
import vista
from vista import Ventanita
from modelo import ModeloPoo


class Controller:
    def __init__(self, root):
        self.root_controler = root

        self.objeto_vista = vista.Ventanita(self.root_controler)


if __name__ == "__main__":
    root = Tk()
    application = Controller(root)

    root.mainloop()
