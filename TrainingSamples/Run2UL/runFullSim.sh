#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <PROCESS> <random seed> <num events>"
    exit 1
fi

# Input arguments
PROCESS=$1
RANDOM_SEED=$2
NUM_EVENTS=$3

# Base name for output files
FRAG_BASE="SMS-T1tttt_mGl-1500_mLSP-100_13TeV-pythia8_cfi"

# Directory paths
WORKDIR=$PWD
JOBDIR="$WORKDIR/jobs"
cd "$JOBDIR"

# Define CMSSW setups
declare -A CMSSW_SETUP=(
    ["GEN"]="CMSSW_10_6_30_patch1"
    ["SIM"]="CMSSW_10_6_17_patch1"
    ["DIGI"]="CMSSW_10_6_17_patch1"
    ["HLT"]="CMSSW_10_2_16_UL"
    ["RECO"]="CMSSW_10_6_17_patch1"
    ["MiniAOD"]="CMSSW_10_6_20"
    ["NanoAOD"]="CMSSW_10_6_29"
)

# Define output files for each stage
OUTPUT_FILES=(
    "${FRAG_BASE}_SUS-RunIISummer20UL16NanoAODv9_${RANDOM_SEED}.root"
    "${FRAG_BASE}_MiniAODSIM_${RANDOM_SEED}.root"
    "${FRAG_BASE}_AODSIM_${RANDOM_SEED}.root"
    "${FRAG_BASE}_HLT_${RANDOM_SEED}.root"
    "${FRAG_BASE}_DIGI_${RANDOM_SEED}.root"
    "${FRAG_BASE}_SIM_${RANDOM_SEED}.root"
    "${FRAG_BASE}_GEN_${RANDOM_SEED}.root"
)

# Define cmsDriver commands for each stage
declare -A COMMANDS
COMMANDS["GEN"]="cmsDriver.py ${PROCESS} --eventcontent RAWSIM --datatier GEN --fileout file:${OUTPUT_FILES[6]} --conditions 106X_upgrade2018_realistic_v4 --step GEN --geometry DB:Extended --era Run2_2018 --mc -n ${NUM_EVENTS} --customise_commands \"process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(${RANDOM_SEED})\" --python_filename fragment_${FRAG_BASE}_GEN_${RANDOM_SEED}.py && cmsRun fragment_${FRAG_BASE}_GEN_${RANDOM_SEED}.py"
COMMANDS["SIM"]="cmsDriver.py --python_filename ${FRAG_BASE}_SIM_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[6]} --eventcontent RAWSIM --datatier GEN-SIM --fileout file:${OUTPUT_FILES[5]} --conditions 106X_upgrade2018_realistic_v11_L1v1 --step SIM --geometry DB:Extended --era Run2_2018 --mc --runUnscheduled -n -1"
COMMANDS["DIGI"]="cmsDriver.py --python_filename ${FRAG_BASE}_DIGI_DIGIPremix_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[5]} --eventcontent PREMIXRAW --datatier GEN-SIM-DIGI --fileout file:${OUTPUT_FILES[4]} --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --datamix PreMix --era Run2_2018 --mc --runUnscheduled -n -1"
COMMANDS["HLT"]="cmsDriver.py --python_filename ${FRAG_BASE}_HLT_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[4]} --eventcontent RAWSIM --datatier GEN-SIM-RAW --fileout file:${OUTPUT_FILES[3]} --conditions 102X_upgrade2018_realistic_v15 --step HLT:2018v32 --geometry DB:Extended --era Run2_2018 --mc -n -1"
COMMANDS["RECO"]="cmsDriver.py --python_filename ${FRAG_BASE}_RECO_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[3]} --eventcontent AODSIM --datatier AODSIM --fileout file:${OUTPUT_FILES[2]} --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --era Run2_2018 --mc --runUnscheduled -n -1"
COMMANDS["MiniAOD"]="cmsDriver.py --python_filename ${FRAG_BASE}_MiniAOD_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[2]} --eventcontent MINIAODSIM --datatier MINIAODSIM --fileout file:${OUTPUT_FILES[1]} --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --era Run2_2018 --mc --runUnscheduled -n -1"
COMMANDS["NanoAOD"]="cmsDriver.py --python_filename ${FRAG_BASE}_NanoAOD_${RANDOM_SEED}_cfg.py --filein file:${OUTPUT_FILES[1]} --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:${OUTPUT_FILES[0]} --conditions 106X_mcRun2_asymptotic_v17 --step NANO --geometry DB:Extended --era Run2_2018 --mc --runUnscheduled -n -1"

JOB_START=$(date +%s)
# Determine which stage to run
for stage in NanoAOD MiniAOD RECO HLT DIGI SIM GEN; do
    # Determine the index of the current stage
    CURRENT_STAGE_INDEX=$(echo "NanoAOD MiniAOD RECO HLT DIGI SIM GEN" | tr ' ' '\n' | grep -n "^$stage$" | cut -d: -f1)
    PREVIOUS_STAGE_INDEX=$((CURRENT_STAGE_INDEX))
    
    if [ "$stage" == "GEN" ] &&[ -f "${OUTPUT_FILES[${CURRENT_STAGE_INDEX}]}" ]; then
        echo "NANO exists, so skipping: ${OUTPUT_FILES[${CURRENT_STAGE_INDEX}]}"
        break
    fi

    # Check if the input file (output from the previous stage) exists
    if [ "$stage" == "GEN" ] || [ -f "${OUTPUT_FILES[${PREVIOUS_STAGE_INDEX}]}" ]; then
        echo "Running stage: $stage because it thinks ${OUTPUT_FILES[${PREVIOUS_STAGE_INDEX}]} exists"
        # Set up CMSSW environment
        CMSSW_VERSION=${CMSSW_SETUP[$stage]}
        if [ ! -d "../${CMSSW_VERSION}/src" ]; then
            echo "${CMSSW_VERSION} not found, setting it up..."
            cd ..
            scram p CMSSW ${CMSSW_VERSION}
            cd jobs/
        fi
        cd ../${CMSSW_VERSION}/src
        eval `scram runtime -sh`
        cd ../../jobs/

        # Run the cmsDriver command
        eval ${COMMANDS[$stage]}

        # Check elapsed time and exit if 30 minutes have passed
        ELAPSED=$(( $(date +%s) - $JOB_START ))
        if [ $ELAPSED -gt 1800 ]; then
            echo "Job has run for 30 minutes. Terminating..."
            exit 0
        fi
        
        if [ ! "$stage" == "GEN" ]; then
            echo "Delete the input file for this stage ${OUTPUT_FILES[${PREVIOUS_STAGE_INDEX}]}"        
            rm -f "${OUTPUT_FILES[${PREVIOUS_STAGE_INDEX}]}"
        fi
        break
    else
        echo "Skipping stage: $stage (input file ${OUTPUT_FILES[${PREVIOUS_STAGE_INDEX}]} doesnt exist)"
    fi
done

