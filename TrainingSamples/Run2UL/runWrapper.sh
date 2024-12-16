#!/bin/bash
#PBS -l mem=8gb          # Request 8 GB of memory
#PBS -l ncpus=2          # Request 2 CPUs
#PBS -l walltime=04:00:00 # Set a wall time of 4 hours
#PBS -j oe               # Combine standard output and error

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /nfs/dust/cms/user/beinsam/FastSim/Refinement/FastSimRefinement/TrainingSamples/Run2UL

PROCESS=$1
SIM_TYPE=$2
RANDOM_SEED=$3
NUM_EVENTS=$4

echo "PROCESS: $PROCESS"
echo "SIM_TYPE: $SIM_TYPE"
echo "RANDOM_SEED: $RANDOM_SEED"
echo "NUM_EVENTS: $NUM_EVENTS"

# Check for correct number of arguments
if [ "$#" -ne 4 ]; then
    echo "wrapper usage: $0 <PROCESS> <SIM_TYPE> <random seed> <num events>"
    exit 1
fi

# Run the appropriate simulation script
if [ "$SIM_TYPE" == "FullSim" ]; then
    cmssw-el7 -- bash runFullSim.sh "$PROCESS" "$RANDOM_SEED" "$NUM_EVENTS"
elif [ "$SIM_TYPE" == "FastSim" ]; then
    cmssw-el7 -- bash runFastSim.sh "$PROCESS" "$RANDOM_SEED" "$NUM_EVENTS"
else
    echo "Invalid SIM_TYPE specified. Must be 'FullSim' or 'FastSim'."
    exit 1
fi

