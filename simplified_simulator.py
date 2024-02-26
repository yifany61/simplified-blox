import random
import time
from fifo_scheduler import FIFOScheduler, ClusterState

class SimplifiedSimulator:
    def __init__(self, jobs_per_hour, cluster_state):
        self.jobs_per_hour = jobs_per_hour
        self.scheduler = FIFOScheduler(cluster_state)
        self.job_id = 0
        self.job_completion_times = []  # Store completion times for each job

    def run_simulation(self, simulation_time=3600):  # Run for one hour by default
        print(f'Simulation started, running for {simulation_time} seconds...')
        end_time = time.time() + simulation_time
        while time.time() < end_time:
            if random.random() < self.jobs_per_hour / 3600:
                self.job_id += 1
                job_duration = random.randint(100, 300)  # Random job duration
                job_info = {
                    'job_name': f'Job{self.job_id}',
                    'duration': job_duration,
                    'resources': {'cpus': 2, 'gpus': 1, 'memory': 4}
                }
                print(f'Job {self.job_id} generated with duration {job_duration}s.')
                # job_start_time = time.time()
                self.scheduler.add_job(self.job_id, job_info)
            self.scheduler.schedule_jobs()
                # job_end_time = time.time()
                # job_completion_time = job_end_time - job_start_time
                # self.job_completion_times.append(job_completion_time)
                # print(f'Job {self.job_id} completed. Completion time: {job_completion_time}s.')
            for completed_job_id, completed_job_info in self.scheduler.check_completed_jobs():
                completion_time = completed_job_info['end_time'] - completed_job_info['start_time']
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
    simulator.run_simulation()