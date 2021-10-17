from Event import EventType, Event

class EventQueue:
    def __init__(self, end_time = 999):
        self.queue = [Event("start", 0), Event("end", end_time)]

    def __str__(self):
        msg = "Event Queue: "       

        for event in self.queue:
            msg += f"{event}"

        return msg

    def is_empty(self):
        return len(self.queue) == 0


    def add_job_mix(self, job_mix):
        for job in job_mix.list:
            self.add_event(Event(EventType.ARRIVAL, job.arrival, job))
        

    def add_event(self, new_event):
        self.queue.append(new_event)

        self.queue.sort(key = lambda event: event.time)


    def extract_event(self):
        return self.queue.pop(0)


class EventQueueAntecipated(EventQueue):
    def __init__(self, end_time = 999):
        super().__init__(end_time)

    def add_job_mix(self, job_mix):
        for job in job_mix.list:
            self.add_event(Event(EventType.ARRIVAL, job.arrival, job))

        self.queue.sort(key = self.sort)

    def sort(self, event):
        if (event.job is None):
            return event.time
        else:
            return event.job.duration
            