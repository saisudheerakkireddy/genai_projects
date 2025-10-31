import google.generativeai as genai
import json
import os
import re
import subprocess
import sys
from datetime import datetime

# --- AI Configuration ---
# The script now assumes it is run in an environment like Cursor
# that automatically handles Gemini API authentication.

# Configuration
MAX_SECONDS_PER_REPO = 300
MIN_EVIDENCE_PER_CRITERION = 2
EVIDENCE_MISSING_PENALTY = 2
MODEL_SIZE_LARGE_MB_THRESHOLD = 2000
SMALL_MODEL_TEST_MB_THRESHOLD = 200
ENABLE_RUNTIME_VALIDATION = True
ALLOW_NETWORK_CHECKS = False

def run_command(command, cwd, log_file):
    """Runs a shell command and logs its output."""
    start_time = datetime.now()
    log_file.write(f"--- Running command: {command} ---\n")
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=MAX_SECONDS_PER_REPO,
            cwd=cwd,
        )
        runtime_seconds = (datetime.now() - start_time).total_seconds()
        log_file.write(f"Exit Code: {process.returncode}\n")
        log_file.write(f"Runtime: {runtime_seconds:.2f}s\n")
        log_file.write("--- stdout ---\n")
        log_file.write(process.stdout)
        log_file.write("\n--- stderr ---\n")
        log_file.write(process.stderr)
        log_file.write("\n\n")
        return {
            "exit_code": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "runtime_seconds": runtime_seconds,
        }
    except subprocess.TimeoutExpired as e:
        runtime_seconds = (datetime.now() - start_time).total_seconds()
        log_file.write(f"Command timed out after {runtime_seconds:.2f}s\n")
        log_file.write(f"Error: {e}\n\n")
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Timeout expired after {MAX_SECONDS_PER_REPO} seconds.",
            "runtime_seconds": runtime_seconds,
        }

def static_analysis(repo_path, log_file):
    """Performs static analysis on the repository."""
    print("Performing static analysis...")
    evidence = {}
    
    # Git log
    git_log = run_command(
        f"git -C {repo_path} log -n 5 --pretty=format:'%h %ad %an %s' --date=short",
        repo_path,
        log_file,
    )
    evidence["git_log"] = git_log["stdout"]

    # File listing
    ls_la = run_command(f"ls -la {repo_path}", repo_path, log_file)
    evidence["file_listing"] = ls_la["stdout"]

    # AI keyword search
    ai_keywords = run_command(
        f"grep -RIn -E 'openai|transformers|langchain|huggingface|cohere|llama|vertex-ai|ollama' {repo_path} || true",
        repo_path,
        log_file,
    )
    evidence["ai_keywords"] = ai_keywords["stdout"]

    # Model file search
    model_files = run_command(
        f"find {repo_path} -type f -name '*.pt' -o -name '*.bin' -o -name '*.safetensors' -ls || true",
        repo_path,
        log_file,
    )
    evidence["model_files"] = model_files["stdout"]

    return evidence

def check_presentation(repo_path, log_file):
    """Checks for a presentation link."""
    print("Checking for presentation link...")
    presentation_check = run_command(
        f"grep -RIn -E 'youtube\\.com|youtu\\.be|vercel\\.app|netlify\\.app|render\\.com|herokuapp\\.com|huggingface\\.co/spaces' {repo_path} || true",
        repo_path,
        log_file,
    )
    if presentation_check["stdout"]:
        return {
            "presentation_link_detected": True,
            "presentation_link_excerpt": presentation_check["stdout"].strip(),
            "presentation_score": 1,
        }
    return {
        "presentation_link_detected": False,
        "presentation_link_excerpt": None,
        "presentation_score": 0,
    }

def build_and_test(repo_path, log_file):
    """Attempts to build and test the project."""
    print("Attempting to build and test...")
    reproducible = False

    # Python
    if os.path.exists(os.path.join(repo_path, "requirements.txt")):
        print("Found requirements.txt, attempting to install and test...")
        pip_install = run_command(
            "pip install -r requirements.txt --no-deps",
            repo_path,
            log_file,
        )
        if pip_install["exit_code"] == 0:
            pytest_run = run_command("pytest -q || echo pytest-failed", repo_path, log_file)
            if "pytest-failed" not in pytest_run["stdout"]:
                reproducible = True

    # Node.js
    if os.path.exists(os.path.join(repo_path, "package.json")):
        print("Found package.json, attempting to install and test...")
        npm_ci = run_command("npm ci --no-fund", repo_path, log_file)
        if npm_ci["exit_code"] == 0:
            npm_test = run_command("npm test || echo npm-test-failed", repo_path, log_file)
            if "npm-test-failed" not in npm_test["stdout"]:
                reproducible = True
    
    # Docker
    if os.path.exists(os.path.join(repo_path, "Dockerfile")):
        print("Found Dockerfile, attempting to build...")
        docker_build = run_command(
            f"docker build -t test-{os.path.basename(repo_path)} . || echo docker-build-failed",
            repo_path,
            log_file,
        )
        if "docker-build-failed" not in docker_build["stdout"]:
            reproducible = True

    return {"reproducible": reproducible}

def security_scan(repo_path, log_file):
    """Performs security scans."""
    print("Performing security scans...")
    risks = {}
    
    # Gitleaks
    gitleaks_scan = run_command(
        f"gitleaks detect --source={repo_path} --report-format=json || true",
        repo_path,
        log_file,
    )
    if gitleaks_scan["stdout"]:
        risks["gitleaks"] = json.loads(gitleaks_scan["stdout"])

    # Bandit
    bandit_scan = run_command(
        f"bandit -r {repo_path} -f json || true",
        repo_path,
        log_file,
    )
    if bandit_scan["stdout"]:
        try:
            risks["bandit"] = json.loads(bandit_scan["stdout"])
        except json.JSONDecodeError:
            risks["bandit"] = "Error parsing bandit output"

    # License scan
    license_scan = run_command(
        f"find {repo_path} -maxdepth 2 -type f \\( -name '*LICENSE*' -o -name '*COPYING*' \\) || true",
        repo_path,
        log_file,
    )
    if license_scan["stdout"]:
        risks["license"] = {"detected": True, "files": license_scan["stdout"].strip().split('\n')}
    else:
        risks["license"] = {"detected": False, "files": []}

    return {"risks": risks}

def model_and_runtime_validation(repo_path, log_file):
    """Handles model validation, runtime checks, and host recommendations."""
    print("Performing model and runtime validation...")
    validation_results = {
        "model_files_details": [],
        "gpu_detected": False,
        "gpu_info": "no-gpu",
        "host_recommendation": "CPU"
    }

    # Find model files and sizes
    model_size_cmd = run_command(
        f"find {repo_path} -type f -name '*.pt' -o -name '*.bin' -o -name '*.safetensors' -o -name '*.ggml*' -exec du -m {{}} + || true",
        repo_path,
        log_file
    )
    
    if model_size_cmd["stdout"]:
        total_size = 0
        for line in model_size_cmd["stdout"].strip().split('\n'):
            if not line:
                continue
            parts = line.split()
            size_mb, path = int(parts[0]), parts[1]
            validation_results["model_files_details"].append({"path": path, "size_mb": size_mb})
            total_size += size_mb
        
        if total_size > MODEL_SIZE_LARGE_MB_THRESHOLD:
            validation_results["host_recommendation"] = "GPU Recommended"

    # GPU probe
    gpu_probe_cmd = run_command(
        "command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || echo no-gpu",
        repo_path,
        log_file
    )

    if "no-gpu" not in gpu_probe_cmd["stdout"]:
        validation_results["gpu_detected"] = True
        validation_results["gpu_info"] = gpu_probe_cmd["stdout"].strip()
        
    return validation_results

def validate_evidence_and_apply_penalties(scores, evidence):
    """Validates evidence and applies penalties if criteria are not met."""
    penalties = []
    
    # Technical Execution Evidence
    tech_evidence_count = 0
    if evidence.get("reproducible", False):
        tech_evidence_count += 1
    if "docker-build-failed" not in evidence.get("build_and_test_log", ""):
        tech_evidence_count +=1
        
    if tech_evidence_count < MIN_EVIDENCE_PER_CRITERION:
        penalty = {
            "criterion": "technical_execution",
            "points_deducted": EVIDENCE_MISSING_PENALTY,
            "reason": f"Insufficient evidence ({tech_evidence_count}/{MIN_EVIDENCE_PER_CRITERION})"
        }
        penalties.append(penalty)
        scores["technical_execution"] = max(0, scores.get("technical_execution", 0) - EVIDENCE_MISSING_PENALTY)

    # Use of AI Evidence
    ai_evidence_count = 0
    if evidence.get("ai_keywords"):
        ai_evidence_count += len(evidence["ai_keywords"].strip().split('\n'))
        
    if evidence.get("model_files_details"):
        ai_evidence_count += len(evidence["model_files_details"])

    if ai_evidence_count < MIN_EVIDENCE_PER_CRITERION:
        penalty = {
            "criterion": "use_of_ai",
            "points_deducted": EVIDENCE_MISSING_PENALTY,
            "reason": f"Insufficient evidence ({ai_evidence_count}/{MIN_EVIDENCE_PER_CRITERION})"
        }
        penalties.append(penalty)
        scores["use_of_ai"] = max(0, scores.get("use_of_ai", 0) - EVIDENCE_MISSING_PENALTY)

    return scores, penalties

def get_ai_evaluation(evidence, repo_path, log_file):
    """
    Calls a Gemini model to get a dynamic, in-depth evaluation of the repository.
    """
    print("Getting AI evaluation...")
    log_file.write("--- Getting AI evaluation ---\n")

    # Consolidate evidence into a text block for the prompt
    context = f"""
    Repository Path: {repo_path}

    Static Analysis Evidence:
    Git Log:
    {evidence.get('git_log', 'N/A')}

    File Listing:
    {evidence.get('file_listing', 'N/A')}

    AI Keyword Search Results (grep for 'openai|transformers|langchain|...'):
    {evidence.get('ai_keywords', 'N/A')}

    Model Files Found (*.pt, *.bin, *.safetensors):
    {evidence.get('model_files', 'N/A')}

    Model & Runtime Validation:
    {json.dumps(evidence.get('model_runtime_validation', {}), indent=2)}
    
    Presentation Link Excerpt:
    {evidence.get('presentation_link_excerpt', 'N/A')}

    Build and Test Results:
    Reproducible: {evidence.get('reproducible', False)}

    Security Scan Results:
    {json.dumps(evidence.get('risks', {}), indent=2)}
    """

    prompt = f"""
    You are an expert Agentic AI Evaluation Analyst reviewing a hackathon project.
    Based on the provided context and evidence from the repository, please provide a detailed evaluation.
    Your response MUST be in a valid JSON format, enclosed in a single ```json code block. 
    Do not include any text before or after the JSON code block.

    The JSON object should have the following structure:
    {{
        "scores": {{
            "innovation": <score_integer_1_to_10>,
            "technical_execution": <score_integer_1_to_10>,
            "use_of_ai": <score_integer_1_to_10>,
            "impact_scalability": <score_integer_1_to_10>
        }},
        "strengths": ["<A specific, concise strength>", "<Another specific strength>"],
        "steelman_weaknesses": ["<A specific, constructive weakness>", "<Another weakness>"],
        "recommended_fixes": ["<A specific, actionable fix>", "<Another fix>"],
        "notes_for_judges": "<A concise, insightful summary (2-3 sentences) for the judges>"
    }}

    Here is the context for the project:
    {context[:25000]} 
    
    Please analyze the context and provide your evaluation in the specified JSON format. Justify your scores implicitly in the qualitative feedback.
    - innovation: How novel is the idea? Is it a creative use of AI?
    - technical_execution: Judge the code quality, structure, and whether it's reproducible. A project with a Dockerfile and successful build should score higher.
    - use_of_ai: How central and sophisticated is AI to the project? Does it use modern techniques (e.g., LangChain, Transformers)? Is it more than a simple API call?
    - impact_scalability: What is the potential for real-world impact? Can it scale?
    - strengths: List 2-3 specific, positive aspects based on the evidence.
    - steelman_weaknesses: List 2-3 constructive weaknesses based on the evidence.
    - recommended_fixes: Suggest specific, actionable improvements.
    - notes_for_judges: A summary of your overall impression.
    """
    
    try:
        # Removed the explicit GEMINI_API_KEY check
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Extract JSON from the markdown code block
        ai_response_text = response.text
        match = re.search(r"```json\n(.*)\n```", ai_response_text, re.DOTALL)
        if not match:
            raise ValueError("AI response did not contain a valid JSON code block.")
        
        ai_response_json = match.group(1)
        log_file.write("Successfully received AI evaluation.\n")
        return json.loads(ai_response_json)
    except Exception as e:
        error_message = f"Error getting AI evaluation: {e}"
        print(error_message)
        log_file.write(f"{error_message}\n")
        # Fallback to a default error structure if AI fails
        return {
            "scores": { "innovation": 0, "technical_execution": 0, "use_of_ai": 0, "impact_scalability": 0 },
            "strengths": ["AI evaluation failed."],
            "steelman_weaknesses": [str(e)],
            "recommended_fixes": ["Check the logs for details on the AI evaluation failure."],
            "notes_for_judges": "The AI evaluation process failed for this repository.",
        }

def get_scores(ai_scores, presentation_info):
    """Generates final scores based on AI evaluation and presentation check."""
    scores = ai_scores
    scores["presentation"] = presentation_info["presentation_score"]
    
    # Calculate weighted score
    weighted_score = (
        (scores.get("innovation", 0) * 0.25)
        + (scores.get("technical_execution", 0) * 0.25)
        + (scores.get("use_of_ai", 0) * 0.25)
        + (scores.get("impact_scalability", 0) * 0.15)
        + (scores.get("presentation", 0) * 0.10)
    )
    scores["weighted_score_percent"] = (weighted_score / 10) * 100
    
    return scores

def classify_repo(scores, reproducible):
    """Classifies the repository based on its score."""
    score = scores.get("weighted_score_percent", 0)
    if score >= 85 and reproducible and scores.get("use_of_ai", 0) >= 8:
        return "Winner-contender"
    elif 70 <= score < 85:
        return "Promising"
    elif 50 <= score < 70:
        return "Needs-work"
    else:
        return "Not-fit"

def main():
    if len(sys.argv) != 3:
        print("Usage: python process_repo.py <repo_path> <output_dir>")
        sys.exit(1)

    repo_path = sys.argv[1]
    output_dir = sys.argv[2]
    repo_name = os.path.basename(repo_path)
    log_file_path = os.path.join(output_dir, "logs", f"{repo_name}_commands.log")

    with open(log_file_path, "w") as log_file:
        # Step 1: Gather all evidence
        static_evidence = static_analysis(repo_path, log_file)
        presentation_info = check_presentation(repo_path, log_file)
        build_info = build_and_test(repo_path, log_file)
        security_info = security_scan(repo_path, log_file)
        model_runtime_info = model_and_runtime_validation(repo_path, log_file)

        full_evidence = {
            **static_evidence,
            **presentation_info,
            **build_info,
            **security_info,
            "model_runtime_validation": model_runtime_info
        }

        # Step 2: Get evaluation from AI
        ai_evaluation = get_ai_evaluation(full_evidence, repo_path, log_file)

        # Step 3: Apply penalties and construct the report
        scores, penalties = validate_evidence_and_apply_penalties(
            ai_evaluation.get("scores", {}), full_evidence
        )
        final_scores = get_scores(scores, presentation_info)
        classification = classify_repo(final_scores, build_info["reproducible"])

        report = {
            "id": repo_path,
            "name": repo_name,
            "scores": final_scores,
            "penalties_applied": penalties,
            "presentation_link_detected": presentation_info["presentation_link_detected"],
            "presentation_link_excerpt": presentation_info["presentation_link_excerpt"],
            "reproducible": build_info["reproducible"],
            "model_runtime_validation": model_runtime_info,
            "strengths": ai_evaluation.get("strengths", []),
            "steelman_weaknesses": ai_evaluation.get("steelman_weaknesses", []),
            "recommended_fixes": ai_evaluation.get("recommended_fixes", []),
            "risks": security_info["risks"],
            "classification": classification,
            "notes_for_judges": ai_evaluation.get("notes_for_judges", ""),
        }

        # Write individual JSON report
        report_path = os.path.join(output_dir, "reports", f"{repo_name}.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
        
        # Write individual Markdown report
        md_report_path = os.path.join(output_dir, "reports", f"{repo_name}.md")
        with open(md_report_path, "w") as f:
            f.write(f"# Evaluation Report for {repo_name}\n\n")
            f.write(f"**Classification:** {classification}\n\n")
            f.write(f"**Weighted Score:** {final_scores['weighted_score_percent']:.2f}%\n\n")
            f.write("## Scores\n")
            for key, value in final_scores.items():
                f.write(f"- **{key.replace('_', ' ').title()}:** {value}\n")
            f.write("\n## Details\n")
            f.write(f"- **Reproducible:** {build_info['reproducible']}\n")
            f.write(f"- **Presentation Link Detected:** {presentation_info['presentation_link_detected']}\n")
            if presentation_info['presentation_link_excerpt']:
                f.write(f"  - **Excerpt:** `{presentation_info['presentation_link_excerpt']}`\n")
            
            f.write("\n## Strengths\n")
            for strength in ai_evaluation.get("strengths", []):
                f.write(f"- {strength}\n")

            f.write("\n## Weaknesses\n")
            for weakness in ai_evaluation.get("steelman_weaknesses", []):
                f.write(f"- {weakness}\n")
            
            f.write("\n## Recommended Fixes\n")
            for fix in ai_evaluation.get("recommended_fixes", []):
                f.write(f"- {fix}\n")

            if security_info["risks"]:
                f.write("\n## Security Risks\n")
                for tool, findings in security_info["risks"].items():
                    f.write(f"### {tool.title()} Findings\n")
                    f.write(f"```json\n{json.dumps(findings, indent=2)}\n```\n")


if __name__ == "__main__":
    main()
