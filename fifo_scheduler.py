import queue
import time

class ClusterState:
    def __init__(self, num_machines=1, cpus_per_machine=4, gpus_per_machine=1, memory_per_machine=16):
        self.machines = [{'cpus': cpus_per_machine, 'gpus': gpus_per_machine, 'memory': memory_per_machine} for _ in range(num_machines)]
    
    def allocate_resources(self, job_resources):
        for machine in self.machines:
            if all(machine[res] >= job_resources[res] for res in job_resources):
                for res in job_resources:
                    machine[res] -= job_resources[res]
                return machine
        return None
    
    def free_resources(self, job_resources, machine):
        for res in job_resources:
            machine[res] += job_resources[res]

class FIFOScheduler:
    def __init__(self, cluster_state):
        self.job_queue = queue.Queue()
        self.cluster_state = cluster_state
        self.job_times = {}
        self.last_job_end_time = 0

    def add_job(self, job_id, job_info):
        self.job_queue.put((job_id, job_info))
        print(f'Job {job_id} submitted with resources {job_info["resources"]}')

    def schedule_jobs(self):
        current_time = time.time()
        if current_time >= self.last_job_end_time and not self.job_queue.empty():
            job_id, job_info = self.job_queue.get()
            allocated_machine = self.cluster_state.allocate_resources(job_info['resources'])
            if allocated_machine:
                start_time = max(self.last_job_end_time, current_time)
                end_time = start_time + job_info['duration']
                self.last_job_end_time = end_time
                self.job_times[job_id] = {'start_time': start_time, 'end_time': end_time, 'machine': allocated_machine}
                print(f'Job {job_id} started at {start_time} and will end at {end_time}')
                # Simulating job completion and resource deallocation
                self.cluster_state.free_resources(job_info['resources'], allocated_machine)
            else:
                print(f'Job {job_id} could not be scheduled due to insufficient resources.')
    
    def check_completed_jobs(self):
        current_time = time.time()
        for job_id, job_info in list(self.job_times.items()):
            if current_time >= job_info['end_time']:
                yield job_id, job_info
                del self.job_times[job_id] 

if __name__ == '__main__':
    cluster_state = ClusterState()
    scheduler = FIFOScheduler(cluster_state)
    # Simulate adding jobs to the scheduler with resource requirements
    scheduler.add_job(1, {'job_name': 'Job1', 'duration': 5, 'resources': {'cpus': 2, 'gpus': 1, 'memory': 4}})
    scheduler.add_job(2, {'job_name': 'Job2', 'duration': 3, 'resources': {'cpus': 1, 'gpus': 0, 'memory': 2}})
    start_time = time.time()
    while time.time() - start_time < 15:  # Simulate for 15 seconds
        scheduler.schedule_jobs()
        time.sleep(0.1) 
