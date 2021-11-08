# Template project to demostrate the use of python on Cluster

## Multiprocessing on deigo

### Setup

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
5. Exit from the computing node
   ```
   exit
   ```

### Test 1 core

```
ruse python3 test.py --seed 0 --cores 1
```

```
Time:           00:02:02
Memory:         51.2 MB
Cores:          12
Total_procs:    12
Active_procs:   12
Proc(%): 99.8  0.1   0.1   0.1   0.1   0.1   0.1   0.0   0.0   0.0   0.0   0.0   
```

### Test 5 cores

```
ruse python3 test.py --seed 0 --cores 5
```

```
Time:           00:00:28
Memory:         348.0 MB
Cores:          12
Total_procs:    25
Active_procs:   23
Proc(%): 97.8  97.8  97.7  97.7  97.6  0.7   0.6   0.3   0.3   0.2   0.2   0.2   0.1   0.1   0.1   0.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0   
```

### Test 10 cores

```
ruse python3 test.py --seed 0 --cores 10
```

```
Time:           00:00:16
Memory:         602.9 MB
Cores:          12
Total_procs:    25
Active_procs:   23
Proc(%): 96.1  96.1  96.1  96.1  96.1  96.0  95.9  95.9  95.8  95.7  1.4   1.3   0.6   0.6   0.6   0.4   0.4   0.4   0.3   0.3   0.1   0.1   0.1   
```