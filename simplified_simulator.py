import random
import time
from fifo_scheduler import FIFOScheduler, ClusterState

class SimplifiedSimulator:
    def __init__(self, jobs_per_hour, cluster_state):
        self.jobs_per_hour = jobs_per_hour
        self.scheduler = FIFOScheduler(cluster_state)
        self.job_id = 0
        self.job_completion_times = []  

    def generate_and_submit_jobs(self, num_jobs): 
        for i in range(num_jobs):
            self.job_id += 1
            job_duration = random.randint(100, 300)  # Random job duration
            job_info = {
                'job_name': f'Job{self.job_id}',
                'duration': job_duration,
                'resources': {'cpus': 2, 'gpus': 1, 'memory': 4}
            }
            print(f'Job {self.job_id} generated with duration {job_duration}s.')
            self.scheduler.add_job(self.job_id, job_info)

    def run_simulation(self, simulation_time=3600, batch_submission=False, num_batch_jobs=5):  
        print(f'Simulation started, running for {simulation_time} seconds...')
        if batch_submission:
            self.generate_and_submit_jobs(num_batch_jobs)

        end_time = time.time() + simulation_time
        while time.time() < end_time:
            if not batch_submission and random.random() < self.jobs_per_hour / 3600:
                self.generate_and_submit_jobs(1) # generate and submit job one by one                
            self.scheduler.schedule_jobs()
            for completed_job_id, completed_job_info in self.scheduler.check_completed_jobs():
                submission_time = completed_job_info['submit_time']
                completion_time = completed_job_info['end_time'] - submission_time
                self.job_completion_times.append(completion_time)
                print(f'Job {completed_job_id} completed. Completion time: {completion_time}s.')
            time.sleep(1)
        print('Simulation ended.')
        self.calculate_average_completion_time()

    def calculate_average_completion_time(self):
        if self.job_completion_times:
            average_time = sum(self.job_completion_times) / len(self.job_completion_times)
            print(f'Average job completion time: {average_time} seconds')
        else:
            print('No jobs were completed during the simulation.')

if __name__ == '__main__':
    cluster_state = ClusterState(num_machines=10, cpus_per_machine=4, gpus_per_machine=1, memory_per_machine=16)
    simulator = SimplifiedSimulator(jobs_per_hour=5, cluster_state=cluster_state)
    simulator.run_simulation(batch_submission=True, num_batch_jobs=5)