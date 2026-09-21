import os
import sys
import threading
import ctkinter_  # Imports your class-based GUI
import edp        # Imports your background process logic

def get_asset_path(relative_path):
    """ Finds the absolute path to bundled files at runtime """
    try:
        # PyInstaller extracts files to a temporary folder named _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def start_background_logic():
    """ Runs the background process loops/logic """
    # Replace 'run_background_loop' with the actual function name inside your edp.py
    if hasattr(edp, 'start'):
        edp.start()

if __name__ == "__main__":
    # 1. Locate your public key dynamically
    key_path = get_asset_path("public_key.pem")
    
    # 2. Start the edp.py background process in a separate thread
    bg_thread = threading.Thread(target=start_background_logic, daemon=True)
    bg_thread.start()
    
    # 3. Launch your CustomTkinter GUI class
    # (Adjust this to match exactly how you initialize your specific class)
    app = ctkinter_.App()
    app.mainloop()
