import queue
import time

class FIFOScheduler:
    def __init__(self):
        # Queue to hold jobs in FIFO order
        self.job_queue = queue.Queue()
        # Dictionary to hold job start times
        self.job_start_times = {}

    def add_job(self, job_id, job_info):
        '''Adds a new job to the scheduler queue.'''
        self.job_queue.put((job_id, job_info))

    def schedule_jobs(self):
        '''Schedules jobs in FIFO order and records start times.'''
        current_time = time.time()
        while not self.job_queue.empty():
            job_id, job_info = self.job_queue.get()
            # For simplicity, assume each job starts as soon as it's scheduled
            self.job_start_times[job_id] = current_time
            # Simulate job execution by waiting a bit
            time.sleep(0.1)  # This represents the job execution time
            print(f'Job {job_id} started at {self.job_start_times[job_id]}')

    def get_job_start_time(self, job_id):
        '''Retrieves the start time of a job.'''
        return self.job_start_times.get(job_id, None)

# Example usage
if __name__ == '__main__':
    scheduler = FIFOScheduler()
    # Simulate adding jobs to the scheduler
    scheduler.add_job(1, {'job_name': 'Job1', 'duration': 5})
    scheduler.add_job(2, {'job_name': 'Job2', 'duration': 3})
    # Schedule jobs and print their start times
    scheduler.schedule_jobs()

