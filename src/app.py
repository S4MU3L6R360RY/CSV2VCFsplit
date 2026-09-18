import tkinter as tk

from src.ui import CSVToVCFApp


def main():
    root = tk.Tk()

    CSVToVCFApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
