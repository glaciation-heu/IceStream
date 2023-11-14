#!/bin/bash

# Define colors for printouts
# Define colors for printouts
GREEN="\033[1;32m"
BLUE="\033[1;34m"
YELLOW="\033[1;33m"
RESET="\033[0m"
CYAN="\033[1;36m"
MAGENTA="\033[1;35m"
set -e
set -o pipefail
# Impressive entry dialog
clear
echo -e "${GREEN}"
figlet -c 'GLACIATION'
echo -e "${RESET}"
sleep 3  # Pause for a few seconds to allow the user to read the banner

print_banner() {
  local color=$1
  shift  # Shift the arguments so $@ does not include the first color parameter
  echo "+-------------------------------------------------------------+"
  printf "| %-59s |\n" "$(date)"
  echo "|                                                             |"
  printf "|${color}`tput bold` %-59s `tput sgr0`${RESET}|\n" "$@"
  echo "+-------------------------------------------------------------+"
}

display_glaciation_info() {
    clear
    echo -e "${GREEN}"
    figlet -c 'GLACIATION'
    echo -e "${CYAN}Green, Privacy-Preserving Data Operations from Edge-to-Cloud.${RESET}"
    echo "Using cutting-edge tech for sustainable and private data handling."
    echo
    echo -e "${YELLOW}WHY CHOOSE GLACIATION?${RESET}"
    echo "Innovative AI & Knowledge Graphs for wide-scale interoperability."
    echo "Data operations that are private, green, and span the entire organization."
    echo -e "${RESET}"
    echo
    echo -e "${MAGENTA}This project has received funding from the European Union’s"
    echo -e "HE research and innovation programme under grant agreement No 101070141.${RESET}"
    echo
    sleep 5  # Pause for a few seconds to allow the user to read the banner
}
display_icestream_info() {

    echo -e "${GREEN}"
    figlet -c 'IceStream Novel Metadata Fabric'
    echo -e "${CYAN}IceStream is a state-of-the-art Distributed Knowledge Graph (DKG) stretching across edge-core-cloud architecture.${RESET}"
    echo "It reduces energy consumption for data processing via AI-enforced minimal data movement operations."
    echo
    echo -e "${YELLOW}ICESTREAM COMPONENTS:${RESET}"
    echo "1. Meta-data service to handle the metadata operations."
    echo "2. Data Storage Service for efficient data handling."
    echo "3. Data-processing monitoring service to oversee data operations."
    echo "4. Replica service to maintain data redundancy and reliability."
    echo "5. Trade-off service to balance between various operational parameters."
    echo "6. Prediction service for forecasting based on data analytics."
    echo
    echo "GLACIATION's technical solution leverages AI/ML and swarm intelligence for optimal data movement across the Edge to Cloud continuum."
    echo
    sleep 5  # Pause for a few seconds to allow the user to read the information
}

deploy_jena() {
    print_banner $YELLOW "IceStream: Jena Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Jena Started"
}
deploy_metadata_service() {
    print_banner $YELLOW "IceStream: Metadata Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Metadata Service Started"
}
deploy_data_storage_service() {
    print_banner $YELLOW "IceStream: Data Storage Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Data Storage Service Started"
}
deploy_data_monitoring_service() {
    print_banner $YELLOW "IceStream: Data Monitoring Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Data Monitoring Service Started"
}
deploy_replica_service() {
    print_banner $YELLOW "IceStream: Replica Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Replica Service Started"
}
deploy_tradeoff_service() {
    print_banner $YELLOW "IceStream: Trade-off Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Trade-off Service Started"
}
deploy_prediction_service() {
    print_banner $YELLOW "IceStream: Prediction Service Starting"
    sleep 5  # Pause for a few seconds to allow the user to read the information
    print_banner $GREEN "IceStream: Prediction Service Started"
}

# Start IceStream
icestream_start() {
    # Start the Power Measurement Framework components
    display_glaciation_info
    display_icestream_info
    echo -e "${CYAN}Initializing IceStream...${RESET}"
    deploy_jena
    deploy_metadata_service
    deploy_data_storage_service
    deploy_data_monitoring_service
    deploy_replica_service
    deploy_tradeoff_service
    deploy_prediction_service
}
icestream_stop() {
  echo "Stopping IceStream..."
  # Add your stop commands here
}

# Check for the parameter and call the relevant function
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <start|stop>"
  exit 1
fi
# Check if the script is being run as root or with necessary privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with necessary privileges. Exiting."
    exit 1
fi

if [ "$1" = "start" ]; then
  icestream_start
elif [ "$1" = "stop" ]; then
  icestream_stop
else
  echo "Invalid parameter: $1. Please use 'start' or 'stop'."
  exit 1
fi
