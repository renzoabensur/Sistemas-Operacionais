# Define CPU 
class CPU:
    def __init__(self):
        self.time = 0
        self.current_job = None

    # Allocate job to CPU if available
    def allocateJob(self, job):
        if self.isCPUAvailable():
            self.current_job = job
            return True
        else:
            return False
    
    # Checks if CPU is available
    def isCPUAvailable(self):
        if self.current_job == None:
            return True
        else:
            return False

    # Delete job and free CPU
    def deleteJob(self):
        self.current_job = None
    
