import time
import random
from fifo_scheduler import FIFOScheduler 

class SimplifiedSimulator:
    def __init__(self, jobs_per_hour):
        self.jobs_per_hour = jobs_per_hour
        self.scheduler = FIFOScheduler()
        self.job_id = 0

    def run_simulation(self):
        print('Simulation started, running for 10 seconds...')
        # Run the simulation for 10 seconds as an example
        end_time = time.time() + 10
        job_generated = False
        while time.time() < end_time:
            # Ensuring at least one job is generated
            if not job_generated or random.random() < self.jobs_per_hour / 3600:
                self.job_id += 1
                job_info = {
                    'job_name': f'Job{self.job_id}',
                    'duration': random.randint(100, 300)  # Random job duration between 100 and 300 seconds
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
    simulator = SimplifiedSimulator(jobs_per_hour=5)
    simulator.run_simulation()