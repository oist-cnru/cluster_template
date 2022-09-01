#!/bin/bash
#SBATCH --partition=compute
#SBATCH --time=0:10:00
#SBATCH --job-name=test_pvrnn
#SBATCH --mem=5G
#SBATCH --cpus-per-task=1
#SBATCH --array=1-10%10

module load python/3.10.2 gcc/11.2.1

(change your user name)
dir_user=fede

# setting working output directories (in flash)
# and let's make sure they exist
output_flash_dir=/flash/TaniU/${dir_user}
mkdir -p ${output_flash_dir}
PVRNN_SAVE_DIR=${output_flash_dir}

# setting final output directory (in bucket)
# this needs to be created manually (nodes can't write to bucket)
output_bucket_dir=/bucket/TaniU/Members/fede/test_pvrnn

# create a temporary directory for this job and save the name
# SLURM_JOB_ID at the end is to make sure the dir is unique
job_id=`printf "%04d" ${SLURM_ARRAY_TASK_ID}`_${SLURM_JOB_ID}
tempdir=${output_flash_dir}/seed_${seed_dir}
mkdir ${tempdir}


# Start 'myprog' 
# we can have input from bucket if necessary
# but we can only output to flash
cd ~/Code/cluster_template
source .venv/bin/activate

# running python to compile new config.toml
python -m deigo.pvrnn_deigo --dir ${output_flash_dir}

# runnning pvrnn on new config.toml
pvrnn train ${output_flash_dir}/config.toml

# copy our result back to Bucket. We use "scp" to copy the data 
# back  as bucket isn't writable directly from the compute nodes.
rsync -avq ${tempdir} deigo:${output_bucket_dir}

# Clean up by removing our temporary directory in flash
rm -r $tempdir