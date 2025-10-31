#!/bin/bash

# AGENTIC EVALUATOR PROMPT — FINAL MASTER VERSION (SEQUENTIAL = 1)
# This script orchestrates the evaluation of 44 local Git repositories from a Generative-AI hackathon.

# Strict mode
set -euo pipefail

# Configuration
readonly OUTPUT_DIR="/Users/sudheerakkireddy/Dev/genai_hackathon_25/evaluation_reports"
readonly REPO_PATHS=(
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/heyitsgautham-agentic-rag-ma-f809cdd"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/mehulagarwal17-devarena_group_a-bdaaf16"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/dharun-kamisetty-GROUP-AV-fc73911"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Vivek-chakali-GROUP-AW-7460578"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/mudassir-16-GROUP-P-hackathon-oct-2025-c323c1d"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/7209-ai-GROUP_U-af251e3"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/dheerajchandra28-GROUP-V-42d3def"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/konampranavi-GROUPG-92d215d"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/kavya-sri10-Group--Q-c825a44"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Punith-42-Group---K-7f5b8a5"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Vijayvarma115-Group-AB-384479d"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/vara-prasad-07-Group_AC-1d14b4d"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/pardhasaradhi-sde-Group-AN-ec9e856"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/kl-thanuja-Group-AO-e0169e7"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Mudassiruddin7-Group-AP-fb09ac1"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Pardhasarathireddy-GroupAX-Pardha-9fa8bfd"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/rishikgoud-Group-B-57b1599"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/yahya94812-Group-Ba-b292d3a"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Gupta-02-Group-BB-92e594e"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Charanjeeth-Shasta-Group_BC-661a2c4"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/himachand-dev-Group-BD-ac7a582"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/zerome24-Group-D-c5807ce"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/SRIKANTH-NAYAK-01-Group-H-7595b6f"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Maruthi0302-Group-L-08856c2"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Vadde-Sathvik-Group-M-027e44c"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/PreethamAnand-Group-N-b990df1"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/hemannayak-GroupR-650bad4"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Devyalamaddi-Group-W-82f9aa2"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/ponnavaishnavi-Group-X-a232e94"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Vaishnavi-1376-Group-Y-86623f1"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/sumeet1029-GroupAU-ef1351d"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Maniteja8883-OG-Decoders-Group-AD-635834f"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/KiranTejz20005-TEAM--T-4fb454b"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/surya-p7-Team-AF-934c471"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/vushakolaPhanindra-group_AT-d75d7a9"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/khusheranjan-hackathon-oct-2025-47ecbcd"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/Sachii257-hackathon-oct-2025-Code-Crew--3c0ce39"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/sathvik8317-hackathon-oct-2025-50994ea"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/solomon-2105-hackathon-oct-2025-76a5952"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/theshubhamgundu-hackathon-oct-2025-cb0de49"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/vaibhavnagdeo18-hackathon-oct-2025-4fe78a1"
    "/Users/sudheerakkireddy/Dev/genai_hackathon_25/extracted_projects/VishwakY-hackathon-oct-2025-5d831e9"
)

main() {
    # Ensure the output directories exist
    mkdir -p "${OUTPUT_DIR}/logs"
    mkdir -p "${OUTPUT_DIR}/reports"

    # Process each repository
    for repo_path in "${REPO_PATHS[@]}"; do
        echo "Processing repository: ${repo_path}"
        python3 process_repo.py "${repo_path}" "${OUTPUT_DIR}"
    done

    # Generate the final summary
    echo "Generating final summary..."
    python3 create_summary.py "${OUTPUT_DIR}"

    echo "Evaluation complete."
}

main "$@"
