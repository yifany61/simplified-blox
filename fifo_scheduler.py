import queue
import time

class FIFOScheduler:
    def __init__(self):
        # Queue to hold jobs in FIFO order
        self.job_queue = queue.Queue()
        # Dictionary to hold job start and end times
        self.job_times = {}
        # Track the end time of the last job to schedule the next job appropriately
        self.last_job_end_time = 0

    def add_job(self, job_id, job_info):
        '''Adds a new job to the scheduler queue.'''
        self.job_queue.put((job_id, job_info))
        print(f'Job {job_id} submitted in fifo scheduler.')

    def schedule_jobs(self):
        '''Schedules jobs in FIFO order and records start and end times.'''
        current_time = time.time()
        # If there are no jobs being processed and there is at least one job waiting, schedule it
        if current_time >= self.last_job_end_time and not self.job_queue.empty():
            job_id, job_info = self.job_queue.get()
            # Start the next job at the end time of the last job or now if no jobs have been scheduled
            start_time = max(self.last_job_end_time, current_time)
            end_time = start_time + job_info['duration']
            self.last_job_end_time = end_time
            self.job_times[job_id] = {'start_time': start_time, 'end_time': end_time}
            print(f'Job {job_id} started at {start_time} and will end at {end_time}')

# Example usage
if __name__ == '__main__':
    scheduler = FIFOScheduler()
    # Simulate adding jobs to the scheduler
    scheduler.add_job(1, {'job_name': 'Job1', 'duration': 5})
    scheduler.add_job(2, {'job_name': 'Job2', 'duration': 3})
    # Schedule jobs and print their start and end times
    start_time = time.time()
    while time.time() - start_time < 15:  # Simulate for 15 seconds
        scheduler.schedule_jobs()
        time.sleep(0.1)  # Small delay to prevent tight loop from consuming too much CPU
