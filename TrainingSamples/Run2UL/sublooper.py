import os

# Ensure necessary directories exist
os.makedirs("jobs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Parameters
NJOBS = 5000
FRAG_BASE = "SMS-T1tttt_mGl-1500_mLSP-100_13TeV-pythia8_cfi"
SIM_TYPE = "FullSim"  # Change to "FastSim" for FastSim
NUM_EVENTS = 200

# Generate a job list for the .jdl file
with open("job_list.txt", "w") as job_list:
    for i in range(NJOBS):
        seed = i + 1  # Random seed for each job
        job_script_path = f"jobs/job_{FRAG_BASE}_{SIM_TYPE}_{seed}.sh"

        nano_file_path = f"jobs/{FRAG_BASE}_SUS-RunIISummer20UL16NanoAODv9_{seed}.root"
        
        # Skip job if Nano*.root file already exists
        if os.path.exists(nano_file_path):
            print(f"Skipping job {seed}: {nano_file_path} already exists.")
            continue
        
        # Write the job script
        with open(job_script_path, "w") as fsh:
            fsh.write("#!/bin/bash\n")
            fsh.write(f"# Job script for seed {seed} ({SIM_TYPE})\n")
            fsh.write("\n")
            fsh.write("# Set up the CMS environment\n")
            fsh.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
            fsh.write("cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/TrainingSamples/Run2UL\n")
            fsh.write("\n")
            fsh.write("# Run the simulation wrapper script\n")
            fsh.write(f"./runWrapper.sh {FRAG_BASE} {SIM_TYPE} {seed} {NUM_EVENTS}\n")

        # Make the job script executable
        os.chmod(job_script_path, 0o755)

        # Add the job to the job list
        job_list.write(f"{job_script_path} {FRAG_BASE} {SIM_TYPE} {seed} {NUM_EVENTS}\n")
    print('just created', job_list.name)
print("All job scripts and the job list have been generated.")

