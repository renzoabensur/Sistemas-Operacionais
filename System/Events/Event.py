
class EventType:
    START = 0
    ARRIVAL = 1
    MEMORY_REQ = 2
    PROCESS_REQ = 3
    END_OF_PROCESS = 4
    END = 5


class Event:
    def __init__(self, event_type : EventType, time, job = None):
        self.event_type = event_type
        self.time = time
        self.job = job

    
    def __str__(self):
        events_stats = f"{self.time:03} - {self.event_type}"
        
        if self.job != None:
            events_stats += ": " + self.job.name
        
        return events_stats
