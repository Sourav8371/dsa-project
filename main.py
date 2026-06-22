import tkinter as tk
from simulation import SimulationApp

def main():
    root = tk.Tk()
    
    # Configure the main window
    root.geometry("900x700")
    root.resizable(False, False)
    
    # Initialize the visualization app
    # This automatically kicks off the DSA layout and update loops
    app = SimulationApp(root, width=860, height=580)
    
    # Start the standard GUI block
    root.mainloop()

if __name__ == "__main__":
    main()
