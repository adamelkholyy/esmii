#!/bin/bash
#SBATCH --export=ALL      				 	# export all environment variables to the batch job.
#SBATCH --partition gpu      					# submit to the gpu queue
#SBATCH -D /lustre/projects/Research_Project-T116269/esmii 	# set working directory to .
#SBATCH --mail-type=ALL						# send email at job completion
#SBATCH --mail-user=a.el-kholy@exeter.ac.uk 			# email address
#SBATCH --time=03:00:00    					# maximum wall time for the job.
#SBATCH --account Research_Project-T116269    			# research project to submit under. 

#SBATCH --nodes=1                                  		# specify number of nodes.
#SBATCH --ntasks-per-node=16        				# specify number of processors per node
#SBATCH --gres=gpu:1						# num gpus	
#SBATCH --mem=4G						# requested memory	

#SBATCH --output=esmii_analysis.out   				# submit script's standard-out
#SBATCH --error=esmii_analysis.err    				# submit script's standard-error
#SBATCH --job-name=esmii_analysis


## load modules
echo Loading modules....

module use /lustre/shared/easybuild/modules/all

cd /lustre/projects/Research_Project-T116269/esmii
echo Modules loaded.

nohup ollama serve &
ollama -help
echo Ollama server started succesfully

## execute python script
start_time=$(date +%s)
echo Executing Python script...

python run_ollama.py -f KC-HM12.txt

echo Python script executed successfully.
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Elapsed time: $elapsed_time seconds"
echo End of script - job finished successfully.



