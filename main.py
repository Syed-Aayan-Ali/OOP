import tkinter as tk
from gui import CarRentalGUI

def main():
    root = tk.Tk()
    app = CarRentalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
