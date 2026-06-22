import tkinter as tk
import sys
import platform
import time

def run_diagnostics():
    print("--- System Diagnostics ---")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")
    
    try:
        root = tk.Tk()
        tcl_version = root.tk.call('info', 'patchlevel')
        print(f"Tkinter / Tcl Version: {tcl_version}")
        root.destroy()
    except Exception as e:
        print(f"Tkinter Error: {e}")

    print("\n--- Stress Test (100 Moving Circles) ---")
    print("This will test if your macOS WindowServer can handle Tkinter updates.")
    print("If this crashes, the issue is your Python/Tkinter installation.")
    
    try:
        root = tk.Tk()
        root.title("Tkinter Stress Test")
        canvas = tk.Canvas(root, width=600, height=400, bg="white")
        canvas.pack()
        
        circles = []
        for i in range(100):
            x, y = 300, 200
            c = canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")
            circles.append({'id': c, 'dx': (i%10 - 5), 'dy': (i//10 - 5)})
            
        def update():
            try:
                for c in circles:
                    coords = canvas.coords(c['id'])
                    # Bounce logic
                    if coords[0] <= 0 or coords[2] >= 600: c['dx'] *= -1
                    if coords[1] <= 0 or coords[3] >= 400: c['dy'] *= -1
                    canvas.move(c['id'], c['dx'], c['dy'])
                root.after(30, update)
            except:
                pass
                
        # Auto-close after 5 seconds if it hasn't crashed
        root.after(5000, root.destroy)
        update()
        root.mainloop()
        print("Stress test COMPLETED without crash.")
    except Exception as e:
        print(f"Stress Test FAILED: {e}")

if __name__ == "__main__":
    run_diagnostics()
