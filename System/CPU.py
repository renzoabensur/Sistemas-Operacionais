# Define CPU class
class CPU:
    def __init__(self):
        self.current_instant = 0
        self.current_job = None

    def __str__(self):
        return f"CPU (Time: {self.current_instant})"

        if(self.current_job != None):
            print(f"[ {self.current_job} ]")

    def allocate_job(self, job):
        if not self.is_executing_job():
            self.current_job = job
            return True
        else:
            return False
    
    def is_executing_job(self):
        if self.current_job == None:
            return False
        else:
            return True

    def finish_job(self):
        self.current_job = None
    
    def update_time(self, time):
        self.current_instant = max(self.current_instant, time)
