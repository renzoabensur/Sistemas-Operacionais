from CPU import CPU

# Define CPU multiprogrammed class
class CPUMultiprogrammed(CPU):
    def __init__(self, time_slice):
        super.__init__()
        self.time_slice = time_slice # Quantum of time
        self.ready_list = [] # List of jobs in the execution circular list

        # Simulation Metrics
        self.n_time_stamps = [[0, 0]] # Time stamps containing the multiprogrammed level

        # Post Simulation Metrics
        self.mean_n = 0.0

    # Allocate job to CPU if available
    # Else allocate in the wait list
    def allocate_job(self, job):
        if self.isCPUAvailable():
            self.current_job = job
            return True
        else:
            self.ready_list.append(job)
            return False

    # Return the slice time, if the next time slice of the job is enough to finish the current job execution
    def sliceTime(self):
        # Calculate the remaining execution time of the current job in the CPU
        remaining_time = self.current_job.duration - self.current_job.executed

        # Check if the next time slice is enough to finish the current job execution
        if remaining_time <= self.time_slice:
            return True, remaining_time
        
        return False, self.time_slice

    # Finishes the time slice by pushing the current job in execution to the wait list 
    # and gets the new current job from it.
    def endTimeSlice(self):
        if self.current_job != None:
            # Update the current job execution time
            self.current_job.executed = round(self.current_job.executed + self.time_slice, 2)

            # Send the current job to the wait list
            self.ready_list.append(self.current_job)

        # Get new current job
        self.newCurrentJob()


    # Get new current job
    def newCurrentJob(self):
        if len(self.ready_list) != 0:
            self.current_job = self.ready_list.pop(0)
            self.current_job.states["Execution"].append([self.time])

            # Check if the next time slice is the last for this job
            last_slice, switch_time = self.generateTimeSlice()
        
            return last_slice, switch_time
        else:
            return 0, 0

    # 
    def updateNTimeStamp(self):
        """
        Update the multiprogrammed level time stamp, 
        according to the number of jobs in the wait list + current job.
        """
        n = 0
        if self.current_job != None:
            n += 1
        n += len(self.ready_list)
        self.n_time_stamps.append([self.time, n])


    def getMeanN(self):
        total_n = 0
        for time_stamp in self.n_time_stamps:
            total_n += time_stamp[1]
        self.mean_n = total_n / len(self.n_time_stamps)
        return self.mean_n