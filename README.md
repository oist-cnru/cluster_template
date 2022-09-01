# Template project to demostrate the use of python on Cluster

## Setup

1. Ssh into deigo
2. Run a temporary job. This will log into a computation node, and needs to be done to avoid overloading the login nodes.
   ```
   srun -p short -t 0:30:00 --mem=10G -c 10 --x11 --pty bash
   ```
3. Clone this project
    ```
    cd ~/Code/
    git clone git@github.com:oist-cnru/cluster_template.git    
    ```
4. Create and activate virtual environment and install all required libraries.
    ```
    cd cluster_template    
    module load python/3.7.3
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt    
    ```
5. If you need to test pvrnn you need to set it up in the curren environment, e.g.,
   ```
   cd ../LibPvrnn
   ./rebuild.py
   ```
6. Exit from the computing node
   ```
   exit
   ```


## Deigo

The python module `deigo/test_deigo.py` is a simple script to demostrate how to run jobs on deigo.

The script can be launched as a **single job** (with 1 or more cores), or as an **array of jobs** (each with a single or more cores).

The code creates a random array of integers and checks how many prime numbers are in the array. The array is generated randomly according to a specific `seed` given as input. 

In the multiple cores version, the array is divided in n parts (where n is the number of cores), and each core is responsible to count the primes in its own partition.

### Single Job - Interactive Run

To test how much memory time the job would take we can run it on a single core, using the interactive mode `srun`:

```
srun -p short -t 0:30:00 --mem=10G -c 10 --x11 --pty bash
cd ~/Code/cluster_template
module load python/3.7.3
module load ruse
ruse python3 test.py --seed 0 --cores 1
```

If we inspect the `ruse` file in output we would see the following

```
Time:           00:02:02
Memory:         51.2 MB
Cores:          12
Total_procs:    12
Active_procs:   12
Proc(%): 99.8  0.1   0.1   0.1   0.1   0.1   0.1   0.0   0.0   0.0   0.0   0.0   
```

If we run the same command above with `--cores 5` we get the following:

```
Time:           00:00:28
Memory:         348.0 MB
Cores:          12
Total_procs:    25
Active_procs:   23
Proc(%): 97.8  97.8  97.7  97.7  97.6  0.7   0.6   0.3   0.3   0.2   0.2   0.2   0.1   0.1   0.1   0.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0   
```

We can notice that while the times is reduced by a factor 5, the momery being employed has increase. This is because the code stores a separate copy of the array used in the computation for each separate core.

### Single Job - Batch Run

In order to run the job in batch mode, we need to run the `sbatch` command followed by the `slurm` file: 

- 1 Core
    ```
    sbatch slurm/deigo_test_single_1core.slurm 
    ```
- 5 Core    
    ```
    sbatch slurm/deigo_test_single_5cores.slurm      
    ```

The folloiwng is the header of the file `deigo_test_single_5cores.slurm`

```bash
#!/bin/bash
#SBATCH --partition=short
#SBATCH --time=0:10:00
#SBATCH --job-name=test_deigo
#SBATCH --mem=5G
#SBATCH --cpus-per-task=5
```

which species to use `short` partition in deigo, allocates a node for `10 minutes` with `5G` of memory and `5 cores`.

When inspecting the file we also notice that we specify the seed manually

```
seed=0
```

This line would need to change if we need to run the script for a different seeds.

### Array of Jobs - Batch Run

If we want to run the same script for 100 different seeds, instead of running the `slurm` file 100 times (changin the seed manually) we can make use of job arrays. This require a slightly modified version of the slurm files above:

- 1 Core (array of 100 jobs)
    ```
    sbatch slurm/deigo_test_array_1core.slurm 
    ```
- 5 Core (array of 100 jobs) 
    ```
    sbatch slurm/deigo_test_array_5cores.slurm      
    ```

The folloiwng is the header of the file `deigo_test_array_5cores.slurm`

```bash
#!/bin/bash
#SBATCH --partition=short
#SBATCH --time=0:10:00
#SBATCH --job-name=test_deigo
#SBATCH --mem=5G
#SBATCH --cpus-per-task=5
#SBATCH --array=1-100%20
```

All parameters are the same of the single job, except for the last line which instantiates an array of 100 separate jobs, each with an internal `ID` that goes from `1` to `100`. The `%20` at the end of the line indicates that we don't want to submit more that 20 jobs to the queue at the time. This is particular important to prevent too many jobs to break Slurm for everyone. **Make sure this number does not exceed 200**.

If you run `squeue` after submitting this array of job, you would see that 20 jobs are exectured as expected, whereas the rest remains on hold and executed as soon as the running jobs are completed.

```
[federico-sangati2@deigo-login4 slurm]$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON) 
12054310_[21-100%2     short test_dei federico PD       0:00      1 (JobArrayTaskLimit) 
        12054310_1     short test_dei federico  R       0:21      1 deigo021708 
        12054310_2     short test_dei federico  R       0:21      1 deigo021709 
        12054310_3     short test_dei federico  R       0:21      1 deigo021709 
        12054310_4     short test_dei federico  R       0:21      1 deigo021710 
        12054310_5     short test_dei federico  R       0:21      1 deigo021710 
        12054310_6     short test_dei federico  R       0:21      1 deigo021712 
        12054310_7     short test_dei federico  R       0:21      1 deigo021712 
        12054310_8     short test_dei federico  R       0:21      1 deigo021711 
        12054310_9     short test_dei federico  R       0:21      1 deigo021711 
       12054310_10     short test_dei federico  R       0:21      1 deigo021711 
       12054310_11     short test_dei federico  R       0:21      1 deigo021711 
       12054310_12     short test_dei federico  R       0:21      1 deigo021711 
       12054310_13     short test_dei federico  R       0:21      1 deigo021711 
       12054310_14     short test_dei federico  R       0:21      1 deigo021711 
       12054310_15     short test_dei federico  R       0:21      1 deigo021711 
       12054310_16     short test_dei federico  R       0:21      1 deigo020301 
       12054310_17     short test_dei federico  R       0:21      1 deigo020301 
       12054310_18     short test_dei federico  R       0:21      1 deigo020301 
       12054310_19     short test_dei federico  R       0:21      1 deigo020301 
       12054310_20     short test_dei federico  R       0:21      1 deigo020301 
```

The `ID` of each job (ranging from 1 to 100 as explained above) is saved in each instance in an environmental variable `SLURM_ARRAY_TASK_ID`. We read this variable in the script to set the seed.

```bash
seed=${SLURM_ARRAY_TASK_ID}
```

Alternatively you can read this variable from you python file with the command:

```python
import os
job_id = os.environ['SLURM_ARRAY_TASK_ID']
```
