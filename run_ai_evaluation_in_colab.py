import google.generativeai as genai
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

# ==============================================================================
#  STANDALONE GITHUB REPOSITORY EVALUATION SCRIPT (FOR COLAB)
# ==============================================================================
#
#  This script is designed to be a self-contained utility for evaluating a
#  single Git repository based on the GenAI Hackathon 2025 criteria.
#
#  Instructions for Use in Google Colab:
#  1. Upload this script to your Colab environment.
#  2. Set your Gemini API key in Colab Secrets (see authentication section).
#  3. Update the `REPO_PATH_TO_EVALUATE` variable to point to the repository
#     you want to analyze.
#  4. Run the script.
#
# ==============================================================================

# --- Configuration ---
MAX_SECONDS_PER_COMMAND = 300
MIN_EVIDENCE_PER_CRITERION = 2
EVIDENCE_MISSING_PENALTY = 2
MODEL_SIZE_LARGE_MB_THRESHOLD = 2000

# --- Helper Functions (Copied from process_repo.py for portability) ---

def run_command(command, cwd, log_file):
    """Runs a shell command and logs its output."""
    log_file.write(f"--- Running command: {command} ---\n")
    try:
        process = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=MAX_SECONDS_PER_COMMAND, cwd=cwd
        )
        log_file.write(f"Exit Code: {process.returncode}\n")
        log_file.write("--- stdout ---\n" + process.stdout + "\n--- stderr ---\n" + process.stderr + "\n\n")
        return {"stdout": process.stdout, "stderr": process.stderr}
    except subprocess.TimeoutExpired:
        log_file.write(f"Command timed out after {MAX_SECONDS_PER_COMMAND}s\n\n")
        return {"stdout": "", "stderr": "Timeout expired."}

def static_analysis(repo_path, log_file):
    """Performs static analysis on the repository."""
    evidence = {}
    evidence["git_log"] = run_command(f"git -C {repo_path} log -n 5 --pretty=format:'%h %ad %an %s' --date=short", repo_path, log_file)["stdout"]
    evidence["file_listing"] = run_command(f"ls -la {repo_path}", repo_path, log_file)["stdout"]
    evidence["ai_keywords"] = run_command(f"grep -RIn -E 'openai|transformers|langchain' {repo_path} || true", repo_path, log_file)["stdout"]
    evidence["model_files"] = run_command(f"find {repo_path} -type f -name '*.pt' -o -name '*.bin' -ls || true", repo_path, log_file)["stdout"]
    return evidence

def check_presentation(repo_path, log_file):
    """Checks for a presentation link."""
    result = run_command(f"grep -RIn -E 'youtube\\.com|vercel\\.app|huggingface\\.co' {repo_path} || true", repo_path, log_file)
    return {"detected": bool(result["stdout"]), "excerpt": result["stdout"].strip()}

def build_and_test(repo_path, log_file):
    """Attempts to build and test the project."""
    if os.path.exists(os.path.join(repo_path, "requirements.txt")):
        pip_install = run_command("pip install -r requirements.txt --no-deps", repo_path, log_file)
        if "error" in pip_install["stderr"].lower(): return False
        pytest_run = run_command("pytest -q || echo pytest-failed", repo_path, log_file)
        return "pytest-failed" not in pytest_run["stdout"]
    return False

def security_scan(repo_path, log_file):
    """Performs security scans."""
    risks = {}
    gitleaks_scan = run_command(f"gitleaks detect --source={repo_path} --report-format=json || true", repo_path, log_file)
    if gitleaks_scan["stdout"]:
        try:
            risks["gitleaks"] = json.loads(gitleaks_scan["stdout"])
        except json.JSONDecodeError:
            risks["gitleaks"] = "Error parsing gitleaks output"
    return risks
    
def model_and_runtime_validation(repo_path, log_file):
    """Handles model validation and runtime checks."""
    validation = {"details": [], "host_recommendation": "CPU"}
    model_size_cmd = run_command(f"find {repo_path} -type f -name '*.pt' -o -name '*.bin' -exec du -m {{}} + || true", repo_path, log_file)
    if model_size_cmd["stdout"]:
        total_size = 0
        for line in model_size_cmd["stdout"].strip().split('\\n'):
            if not line: continue
            size_mb, path = int(line.split()[0]), line.split()[1]
            validation["details"].append({"path": path, "size_mb": size_mb})
            total_size += size_mb
        if total_size > MODEL_SIZE_LARGE_MB_THRESHOLD:
            validation["host_recommendation"] = "GPU Recommended"
    return validation

# --- AI Evaluation Function ---

def get_ai_evaluation(evidence, repo_path, retries=3, delay=5):
    """Calls a Gemini model to get a dynamic, in-depth evaluation."""
    print(f"Getting AI evaluation for: {repo_path}")

    # Create a comprehensive context string from all collected evidence
    context = f"""
    Repository Path: {repo_path}
    Git Log: {evidence.get('git_log', 'N/A')}
    File Listing: {evidence.get('file_listing', 'N/A')}
    AI Keywords Found: {evidence.get('ai_keywords', 'N/A')}
    Model Files: {evidence.get('model_files', 'N/A')}
    Presentation Link: {evidence.get('presentation', {}).get('excerpt', 'N/A')}
    Reproducible Build: {evidence.get('reproducible', False)}
    Security Scan Results: {json.dumps(evidence.get('risks', {}), indent=2)}
    Model/Runtime Info: {json.dumps(evidence.get('model_runtime', {}), indent=2)}
    """

    prompt = f"""
    # Agentic AI Hackathon Project Evaluation Prompt
    You are an expert Agentic AI Evaluation Analyst reviewing a hackathon project. Based on the provided context and evidence from the repository, please provide a detailed, rigorous evaluation in JSON format.

    ## Required JSON Structure
    ```json
    {{
        "scores": {{
            "innovation": <integer 1-10>,
            "technical_execution": <integer 1-10>,
            "use_of_ai": <integer 1-10>,
            "impact_scalability": <integer 1-10>
        }},
        "strengths": ["<specific strength 1>", "<specific strength 2>"],
        "steelman_weaknesses": ["<constructive weakness 1>", "<constructive weakness 2>"],
        "recommended_fixes": ["<actionable fix 1>", "<actionable fix 2>"],
        "notes_for_judges": "<2-3 sentence insightful summary>"
    }}
    ```

    ## Evaluation Criteria & Scoring Guidelines
    - **Innovation (1-10):** Novelty and creativity of the AI application. 9-10 for groundbreaking approaches.
    - **Technical Execution (1-10):** Code quality, architecture, and reproducibility. 9-10 for clean, tested, production-ready code.
    - **Use of AI (1-10):** Depth and sophistication of AI integration. 9-10 for agentic workflows or fine-tuned models.
    - **Impact & Scalability (1-10):** Real-world applicability and growth potential. 9-10 for solving a significant problem with a scalable architecture.
    
    ## Analysis Guidelines
    - **Strengths:** Reference concrete evidence. Be specific (e.g., "Implements RAG with Pinecone" not "Uses AI well").
    - **Steelman Weaknesses:** Be honest but fair. Focus on missing evidence, architectural concerns, or scalability limits.
    - **Recommended Fixes:** Provide specific, actionable suggestions.
    - **Notes to Judges:** Synthesize your overall impression in 2-3 sentences.

    ---
    ## Project Context to Evaluate
    {context[:28000]}
    ---

    Now, analyze the provided project context and return your evaluation in the specified JSON format.
    """

    for attempt in range(retries):
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt)
            match = re.search(r"```json\n(.*)\n```", response.text, re.DOTALL)
            if not match:
                raise ValueError("AI response did not contain a valid JSON code block.")
            print(f"Successfully evaluated: {repo_path}")
            return json.loads(match.group(1))
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {repo_path}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"All attempts failed for {repo_path}.")
                return None

# --- Main Execution Logic ---

def main():
    """
    Main function to run the evaluation on a single repository.
    """
    # --- Colab Authentication ---
    # Assumes the Gemini API key is stored as a secret named 'GEMINI_API_KEY' in Colab.
    try:
        from google.colab import userdata
        genai.configure(api_key=userdata.get('GEMINI_API_KEY'))
    except (ImportError, userdata.SecretNotFoundError):
        print("ERROR: Could not find GEMINI_API_KEY in Colab secrets.")
        print("Please go to 'Secrets' (key icon) and add your Gemini API key.")
        return

    # --- User Configuration ---
    # IMPORTANT: Update this path to point to the repository you want to evaluate.
    # This path should be accessible from your Colab environment (e.g., cloned or uploaded).
    REPO_PATH_TO_EVALUATE = "/content/sample_data/my_repo_to_evaluate" 
    
    if not os.path.isdir(REPO_PATH_TO_EVALUATE):
        print(f"ERROR: The specified repository path does not exist: {REPO_PATH_TO_EVALUATE}")
        print("Please update the `REPO_PATH_TO_EVALUATE` variable.")
        return

    repo_name = os.path.basename(REPO_PATH_TO_EVALUATE)
    output_log_path = f"{repo_name}_evaluation_log.txt"
    output_report_path = f"{repo_name}_evaluation_report.json"

    with open(output_log_path, "w") as log_file:
        print(f"--- Starting Evaluation for {repo_name} ---")
        
        # 1. Gather all evidence
        evidence = static_analysis(REPO_PATH_TO_EVALUATE, log_file)
        evidence["presentation"] = check_presentation(REPO_PATH_TO_EVALUATE, log_file)
        evidence["reproducible"] = build_and_test(REPO_PATH_TO_EVALUATE, log_file)
        evidence["risks"] = security_scan(REPO_PATH_TO_EVALUATE, log_file)
        evidence["model_runtime"] = model_and_runtime_validation(REPO_PATH_TO_EVALUATE, log_file)
        
        # 2. Get AI evaluation
        ai_evaluation = get_ai_evaluation(evidence, REPO_PATH_TO_EVALUATE)
        
        # 3. Combine and save the final report
        if ai_evaluation:
            final_report = {
                "repository_path": REPO_PATH_TO_EVALUATE,
                "repository_name": repo_name,
                "evaluation_date": datetime.now().isoformat(),
                **ai_evaluation,
                "evidence_summary": {
                    "presentation_detected": evidence["presentation"]["detected"],
                    "is_reproducible": evidence["reproducible"],
                    "security_risks_found": bool(evidence["risks"]),
                }
            }
            
            with open(output_report_path, "w") as f:
                json.dump(final_report, f, indent=4)
            print(f"\n--- Evaluation Complete ---")
            print(f"Full report saved to: {output_report_path}")
            print(f"Detailed logs saved to: {output_log_path}")
        else:
            print(f"\n--- Evaluation Failed ---")
            print(f"Could not generate an AI evaluation for the repository.")
            print(f"Check the logs for details: {output_log_path}")

if __name__ == "__main__":
    main()
