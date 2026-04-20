import threading
import tkinter as tk
from ipp.exercises.project.WaterServiceManagerFile import WaterServiceManager


class WaterAppGUI():
    '''
    GUI application for displaying and sorting live water data.

    Provides buttons to sort water data by different attributes
    such as flow rate, water level, temperature, and site name.
    '''
    def __init__(self, root):
        '''
        Initializes the GUI, connects to the WaterServiceManager,
        and builds the application window with sorting buttons.

        Args:
            root (tk.Tk): The main Tkinter window instance.
        '''              
        # store window inside class
        self.root = root
        # set window title text
        self.root.title("Live Water Data Viewer")
        
        # Build buttons first so the window appears immediately
        self._buildButtons()

        # Start water service manager in a background thread
        threading.Thread(target=self._startManager, daemon=True).start()
        
    def _buildButtons(self):
        '''
        Creates all GUI widgets (buttons + status label)
        and places them in the Tkinter window.
        '''
        # Show button on screen + spacing
        tk.Label(self.root, text="Sort Water Data").pack(pady=8)

        tk.Button(self.root, text="Sort by Flow Rate (cfs)",
                  command=lambda: self.manager.sortWaterData("flowRate_cfs")).pack(pady=4)
        tk.Button(self.root, text="Sort by Water Level (ft)",
                  command=lambda: self.manager.sortWaterData("waterLevel_ft")).pack(pady=4)
        tk.Button(self.root, text="Sort by Temperature (°C)",
                  command=lambda: self.manager.sortWaterData("waterTemperature_c")).pack(pady=4)
        tk.Button(self.root, text="Sort by Site Name (A–Z)",
                  command=lambda: self.manager.sortWaterData("location.siteName")).pack(pady=4)
        
        self.status_label = tk.Label(
            self.root,
            text="Wait a bit for the first data update...",
            fg="gray"
            )
        self.status_label.pack(pady=10)
        
    def notifyDataReceived(self):
        '''
        Updates the GUI when the first valid water data is received
        from the background service manager.
        Updates the status label text and color.
        '''
        self.status_label.config(text="✅ Data received! Ready to sort.", fg="green")

    def _startManager(self):
        '''
        Creates and starts the WaterServiceManager in a background thread,
        and links the GUI reference for callbacks.
        '''
        self.manager = WaterServiceManager()
        self.manager.gui_ref = self
        self.manager.startManager()   


if __name__ == "__main__":
    # Create main window object
    window = tk.Tk()
    # Build GUI inside that window
    app = WaterAppGUI(window)
    # keep window open + listen for button clicks
    window.mainloop()

