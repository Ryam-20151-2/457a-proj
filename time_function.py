import time

class Timer:
    def __init__(self):
        self.runtimes = {}

    def start(self, label):
        self.runtimes[label] = {'start': time.time()}

    def stop(self, label):
        if label not in self.runtimes:
            print(f"Timer '{label}' hasn't started yet.")
            return

        self.runtimes[label]['end'] = time.time()
        
    def get_elapsed_time(self, label):
        if label in self.runtimes and 'end' in self.runtimes[label]:
            return self.runtimes[label]['end'] - self.runtimes[label]['start']
        else:
            print(f"Timer '{label}' is either not started or still running.")
            return None
