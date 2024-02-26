import time
import random
from fifo_scheduler import FIFOScheduler, ClusterState

class SimplifiedSimulator:
    def __init__(self, jobs_per_hour, cluster_state):
        self.jobs_per_hour = jobs_per_hour
        self.scheduler = FIFOScheduler(cluster_state)
        self.job_id = 0

    def run_simulation(self):
        print('Simulation started, running for 1 hour...')
        # Run the simulation for 1 hour as an example
        end_time = time.time() + 3600
        job_generated = False
        while time.time() < end_time:
            # Ensuring at least one job is generated
            if not job_generated or random.random() < self.jobs_per_hour / 3600:
                self.job_id += 1
                job_info = {
                    'job_name': f'Job{self.job_id}',
                    'duration': random.randint(100, 300),  # Random job duration between 100 and 300 seconds
                    'resources': {'cpus': 2, 'gpus': 1, 'memory': 4}
                }
                self.scheduler.add_job(self.job_id, job_info)
                print(f'Job {self.job_id} submitted (simulator).')
                job_generated = True

            # Schedule jobs in FIFO order
            self.scheduler.schedule_jobs()

            # Sleep for a second before the next iteration to allow for job generation according to the jobs_per_hour rate
            time.sleep(1)
        print('Simulation ended.')

# Example usage
if __name__ == '__main__':
    # Example: Simulate a scenario where 5 jobs are submitted per hour
    cluster_state = ClusterState(num_machines=10, cpus_per_machine=4, gpus_per_machine=1, memory_per_machine=16)
    simulator = SimplifiedSimulator(jobs_per_hour=5, cluster_state=cluster_state)
    simulator.run_simulation()