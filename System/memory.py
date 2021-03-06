class Partition:
    def __init__(self, base, size, job = None):
        self.job = job
        self.base = base
        self.size = size

    
    def __str__(self):
        name_str = None
        if self.job != None:
            name_str = self.job.name
        else:
            name_str = "Hole"
        print(f"    {name_str}: {self.base:05}, {self.size:05}")


class Memory:
    def __init__(self, memory_size):
        self.size = memory_size
        self.partitions = [Partition(0, memory_size)]
        self.occupation_percentage = 0

        self.allocations_accepted = 0
        self.allocations_denied = 0
        
    def __str__(self):
        print(f"Memory ({self.size/1e3:.4}k) [")
        for partition in self.partitions:
            partition.print()
        print("]")

    def isAvailable(self, job = None):
        """
        Checks if the memory is empty
        """
        if len(self.partitions) == 1:
            if self.partitions[0].job == None:
                return True
        return False

    
    def isSmaller(self, job_size):
        """
        Checks if the job size would fit in the entire memory
        """
        if job_size <= self.size:
            return True
        return False


    def allocate(self, job):
        """
        Gets a job and allocates it inside the memory
        """
        self.splitEmptyPartition(0, job)


    def splitEmptyPartition(self, index, job):
        # Get the selected empty partition
        empty_partition = self.partitions.pop(index)
        base = empty_partition.base

        # Create the new partition with the job
        new_partition = Partition(base, job.size, job)
        self.partitions.insert(index, new_partition)

        # Update the job memory metrics
        job.memory = new_partition
        job.memory_base = base
        job.memory_percentage = job.size/self.size * 100
        self.occupation_percentage += job.memory_percentage

        # Check if there will be a new empty partition
        size = empty_partition.size - new_partition.size
        if size > 0:
            # Create the new empty partition
            empty_partition = Partition(new_partition.base + new_partition.size, size)
            self.partitions.insert(index+1, empty_partition)        
    

    def free(self, job):
        """
        Frees the memory, deleting the referenced job of the allocation list (partitions)
        """
        # Find the referenced job in the partitions list
        i = -1
        for index, partition in enumerate(self.partitions):
            if partition.job != None:
                if partition.job.name == job.name:
                    i = index
                    break
        
        # Free the partition
        self.partitions[i].job = None
        job.memory = None

        # Update job memory metrics
        self.occupation_percentage -= job.memory_percentage
        job.memory_percentage = 0

        # Check if the left partition is a hole
        if i > 0:
            if self.partitions[i - 1].job == None:
                # Merge both empty partitions
                self.mergePartitions(i - 1, i)
                i -= 1
        
        # Check if the right partition is a hole
        if i + 1 < len(self.partitions):
            if self.partitions[i + 1].job == None:
                # Merge both empty partitions
                self.mergePartitions(i, i + 1)

        
    def mergePartitions(self, i, j):
        """
        Merges partitions[i] with partition[j] and pops partitions[i]
        """
        left = self.partitions[i]
        right = self.partitions[j]

        right.base = left.base
        right.size += left.size

        self.partitions.pop(i)

    


class MemoryMultiprogrammed(Memory):
    def __init__(self, memory_size, n):
        super().__init__(memory_size)
        self.n = n


    def isAvailable(self, job):
        """
        Checks if there is an empty partition in memory that fits the job.
        Also checks if it is allowed by the multiprogrammed level.
        """
        if self.firstChoice(job.size) != -1:
            if not self.isFull():
                return True
        return False


    def firstChoice(self, size):
        """
        Allocation algorithm. Finds the first partitition that fits the job, returning its index.
        If there is no partition available, returns False.
        """
        for i, partition in enumerate(self.partitions):
            if partition.job == None and partition.size >= size:
                return i
        return -1


    def isFull(self):
        """
        Checks if the multiprogrammed level is already satisfied.
        """
        job_counter = 0
        for partition in self.partitions:
            if partition.job != None:
                job_counter += 1
                if job_counter >= self.n:
                    return True

        return False


class MemoryMultiprogrammedFirstChoice(MemoryMultiprogrammed):
    def allocate(self, job):
        """
        Gets a job and allocates it inside the memory
        """
        i = self.firstChoice(job.size)
        self.splitEmptyPartition(i, job)


class MemoryMultiprogrammedWorstChoice(MemoryMultiprogrammed):
    def allocate(self, job):
        """
        Gets a job and allocates it inside the memory
        """
        i = self.worstChoice(job.size)
        self.splitEmptyPartition(i, job)
    

    def worstChoice(self, size):
        """
        Allocation algorithm. Finds the biggest partitition that fits the job, returning its index.
        If there is no partition available, returns False.
        """
        biggest = 0
        index = -1
        for i, partition in enumerate(self.partitions):
            # Check if it is a partition that fits
            if partition.job == None and partition.size >= size:
                # Check if it is the worst
                if partition.size >= biggest:
                    biggest = partition.size
                    index = i
        return index


class MemoryMultiprogrammedBestChoice(MemoryMultiprogrammed):
    def allocate(self, job):
        """
        Gets a job and allocates it inside the memory
        """
        i = self.bestChoice(job.size)
        self.splitEmptyPartition(i, job)
    

    def bestChoice(self, size):
        """
        Allocation algorithm. Finds the smallest partitition that fits the job, returning its index.
        If there is no partition available, returns False.
        """
        smallest = self.size
        index = -1
        for i, partition in enumerate(self.partitions):
            # Check if it is a partition that fits
            if partition.job == None and partition.size >= size:
                # Check if it is the best
                if partition.size <= smallest:
                    smallest = partition.size
                    index = i
        return index