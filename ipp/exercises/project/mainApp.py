from ipp.exercises.project.WaterServiceManagerFile import WaterServiceManager
from ipp.exercises.project.LiveWaterDataWebVisualizerFile import LiveWaterDataWebVisualizer


class Application:
    '''
    Single entry point for the Water Monitoring System.
    Wires together:
    - WaterServiceManager (data pipeline)
    - LiveWaterDataWebVisualizer (listener + dashboard)
    '''

    def __init__(self):
        self.manager = WaterServiceManager()
        self.visualizer = LiveWaterDataWebVisualizer()

        # connect listener pipeline
        self.manager.setListener(self.visualizer)
        
        # FIX: ensure visualizer can reference manager if needed
        self.visualizer.manager = self.manager

    def start(self):
        print("\nStarting Water Monitoring System...\n")

        # start data collection
        self.manager.startManager()

        # start dashboard (blocking)
        self.visualizer.startVisualizer()


if __name__ == "__main__":
    app = Application()
    app.start()
    


        

 