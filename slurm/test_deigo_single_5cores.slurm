#!/bin/bash
#SBATCH --partition=short
#SBATCH --time=0:10:00
#SBATCH --job-name=test_deigo
#SBATCH --mem=5G
#SBATCH --cpus-per-task=5

module load python/3.7.3

# modify output directories (make sure they exist)
output_flash_dir=/flash/TaniU/fede
output_bucket_dir=/bucket/TaniU/Members/fede/test_deigo

# set seed and number of cores
seed=0
num_cores=5

# create a temporary directory for this job and save the name
seed_dir=${SLURM_JOB_ID}_`printf "%03d" ${seed}`
tempdir=${output_flash_dir}/seed_${seed_dir}
mkdir ${tempdir}

# Start 'myprog' with input from bucket,
# and output to our temporary directory
cd ~/Code/cluster_template
source .venv/bin/activate

python -m deigo.test_deigo \
--seed ${seed} \
--cores ${num_cores} \
--dir ${tempdir} \

# copy our result back to Bucket. We use "scp" to copy the data 
# back  as bucket isn't writable directly from the compute nodes.
rsync -avq ${tempdir}/* deigo:${output_bucket_dir}

# Clean up by removing our temporary directory
rm -r $tempdir