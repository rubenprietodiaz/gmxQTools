import os
import shutil
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Setup your md simulation after pymemdyn equilibration.")
    parser.add_argument("-t", "--simulation-time", type=int, help="Simulation time in nanoseconds (default by PyMemDyn: 10 ns).")
    parser.add_argument("-rt", "--runtime", type=int, help="Runtime in hours (default: 24).", default=24)
    parser.add_argument("-C", "--cluster", choices=["CSB", "CESGA", "TETRA"], default="TETRA", help="Choose the cluster (default: TETRA).")
    return parser.parse_args()

def copy_files_in_directory(directory, destination_folder):
    """Iterate over the folders within the current directory and call the copy_files function."""
    # Iterate over the folders within the current directory
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            current_folder = os.path.join(root, dir)
            # Call the copy_files function to copy files in the current folder
            copy_files(current_folder, destination_folder)
    # Create submit script outside the loop
    create_submit_script(destination_folder)
    print(f"Folder {destination_folder} with scripts and necessary files created. Run 'cd {destination_folder}' and 'sh submit_md.sh' to start the simulations. If you want to do more than one replica, copy {destination_folder} before running any simulation.")


def copy_files(folder, destination_folder):
    """Copy the required files for MD simulations to the destination folder."""
    # Check the existence of each required file
    if all(os.path.isfile(os.path.join(folder, file)) for file in ["prod.mdp", "topol.top", "index.ndx", "topol.tpr"]) and os.path.exists(os.path.join(folder, "finalOutput", "confout.gro")):
        print("All the required files are present in the folder.")
        # Extract the name of the current folder
        folder_name = os.path.basename(folder)

        # Create the folder for files within the destination folder
        destination_folder_path = os.path.join(destination_folder, folder_name)
        os.makedirs(destination_folder_path, exist_ok=True)

        # Copy the files to the corresponding folder
        for file in ["prod.mdp", "topol.top", "index.ndx", "topol.tpr"]:
            shutil.copy(os.path.join(folder, file), destination_folder_path)

        # Check the existence of the finalOutput folder
        final_output_folder = os.path.join(folder, "finalOutput")
        if os.path.isdir(final_output_folder):
            confout_gro = os.path.join(final_output_folder, "confout.gro")
            if os.path.isfile(confout_gro):
                shutil.copy(confout_gro, destination_folder_path)

        # Copy .itp files if they exist
        for itp_file in os.listdir(folder):
            if itp_file.endswith(".itp"):
                shutil.copy(os.path.join(folder, itp_file), destination_folder_path)
        
        print(f"Files copied to {destination_folder_path}.")

        # Create the run_md.sh script inside the destination folder
        create_run_md_script(destination_folder_path)

        # Modify prod.mdp if simulation time is provided
        if args.simulation_time:
            modify_simulation_time(destination_folder_path)
    else:
        return False

def create_submit_script(destination_folder): # Eliminated cd "$1" from the for loop (not necessary for the current implementation)
    """Create the submit_md.sh script to submit the MD simulations."""
    submit_script_content = """#!/bin/bash

start_dir=$(pwd)

for dir in */ ; do
    cd "$dir"
    sbatch run_md.sh
    cd "$start_dir/$1"
done
"""
    submit_script_path = os.path.join(destination_folder, "submit_md.sh")
    with open(submit_script_path, "w") as submit_script_file:
        submit_script_file.write(submit_script_content)

def create_run_md_script(destination_folder):
    """Create the run_md.sh script to run the MD simulations in all the subfolders."""
    if args.cluster == "CSB":
        run_md_script_content = f"""#!/bin/bash
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -t {args.runtime}:00:00
#SBATCH --gpus-per-task=1
#SBATCH --job-name=pymemdyn
#              d-hh:mm:ss
#SBATCH --time=0-{args.runtime}:00:00

gmx grompp -f prod.mdp -c confout.gro -p topol.top -n index.ndx -o topol_prod.tpr --maxwarn 1
srun gmx mdrun -s topol_prod.tpr -o traj.trr -e ener.edr -c final.gro -g production.log -x traj_prod.xtc
"""
    elif args.cluster == "CESGA":
        run_md_script_content = f"""#!/bin/bash -l
#SBATCH -t {args.runtime}:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH -N 1
#SBATCH -c 32
#SBATCH --gres=gpu:a100

gmx grompp -f prod.mdp -c confout.gro -p topol.top -n index.ndx -o topol_prod.tpr --maxwarn 1
srun gmx_mpi mdrun -s topol_prod.tpr -o traj.trr -e ener.edr -c confout.gro -g production.log -x traj_prod.xtc
"""
    elif args.cluster == "TETRA": 
        run_md_script_content = f"""#!/bin/bash

#SBATCH --job-name=MD
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 16
#SBATCH -A naiss2023-3-5
#              d-hh:mm:ss
#SBATCH --time=0-{args.runtime}:00:00

gmx grompp -f prod.mdp -c confout.gro -p topol.top -n index.ndx -o topol_prod.tpr --maxwarn 1
srun gmx mdrun -s topol_prod.tpr -o traj.trr -e ener.edr -c final.gro -g production.log -x traj_prod.xtc"""
    
    run_md_script_path = os.path.join(destination_folder, "run_md.sh")
    with open(run_md_script_path, "w") as run_md_script_file:
        run_md_script_file.write(run_md_script_content)

    # Change permissions to make the script executable
    os.chmod(run_md_script_path, 0o755)

def modify_simulation_time(destination_folder):
    """Modify the simulation time in the prod.mdp file."""
    simulation_time_ns = args.simulation_time
    nsteps = simulation_time_ns * 500000  # 1 ns = 500000 steps

    prod_mdp_path = os.path.join(destination_folder, "prod.mdp")
    with open(prod_mdp_path, "r") as prod_mdp_file:
        lines = prod_mdp_file.readlines()

    with open(prod_mdp_path, "w") as prod_mdp_file:
        for line in lines:
            if line.strip().startswith("nsteps"):
                prod_mdp_file.write(f"nsteps              =  {nsteps}   ; total {simulation_time_ns} ns\n")
            else:
                prod_mdp_file.write(line)

# RUN
args = parse_arguments()
destination_folder = "md_input_files"
copy_files_in_directory(".", destination_folder)