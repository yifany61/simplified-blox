import queue
import time

class FIFOScheduler:
    def __init__(self):
        # Queue to hold jobs in FIFO order
        self.job_queue = queue.Queue()
        # Dictionary to hold job start and end times
        self.job_times = {}

    def add_job(self, job_id, job_info):
        '''Adds a new job to the scheduler queue.'''
        self.job_queue.put((job_id, job_info))
        print(f'Job {job_id} submitted.')

    def schedule_jobs(self):
        '''Schedules jobs in FIFO order and records start and end times.'''
        # If there are no jobs being processed and there is at least one job waiting, schedule it
        if not self.job_times and not self.job_queue.empty():
            job_id, job_info = self.job_queue.get()
            current_time = time.time()
            # Start the next job at the end time of the last job or now if no jobs have been scheduled
            start_time = self.job_times.get(job_id - 1, {}).get('end_time', current_time)
            end_time = start_time + job_info['duration']
            self.job_times[job_id] = {'start_time': start_time, 'end_time': end_time}
            print(f'Job {job_id} started at {start_time} and will end at {end_time}')
            # Simulate job execution by waiting for the job duration
            time.sleep(job_info['duration'])

# Example usage
if __name__ == '__main__':
    scheduler = FIFOScheduler()
    # Simulate adding jobs to the scheduler
    scheduler.add_job(1, {'job_name': 'Job1', 'duration': 5})
    scheduler.add_job(2, {'job_name': 'Job2', 'duration': 3})
    # Schedule jobs and print their start and end times
    while not scheduler.job_queue.empty():
        scheduler.schedule_jobs()