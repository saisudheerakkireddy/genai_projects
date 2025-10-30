import subprocess

import subprocess

def query_ollama_prompt_stdin(prompt_text, model_name="deepseek-r1:7b"):
    try:
        proc = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt_text,
            capture_output=True,
            text=True,
            encoding="utf-8",    # Force utf-8 to avoid decoding issues
            errors="replace",    # Replace invalid chars instead of erroring
            check=True,
        )
        if proc.stdout is not None:
            return proc.stdout.strip()
        else:
            print("No output from Ollama CLI.")
            return None
    except subprocess.CalledProcessError as e:
        print("Ollama CLI command failed:", e)
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        return None


# Example usage:

prompt = """
You are an expert molecular bioinformatician. ONLY respond in valid JSON. 
Do NOT include explanations or instructions.

RNA STRUCTURE SUMMARY:
{"chains": ["A"], "total_residues": 46, "motifs_detected": []}

POCKET DATA:
{"Pocket_ID": "1", "Score": 0.043, "Volume": 1620.036, "Hydrophobicity_score": 4.083}

Predict:
- RNA biomarker region(s)
- Structural motif type
- Function (ligand binding, metal binding, etc.)
- Associated disease relevance
- Recommended drug targets

Respond only like this:
{"predicted_region":"A12-A20","motif_type":"stem-loop","function":"Potential ligand-binding site","associated_disease":"Hypothetical","recommended_drug_targets":["Mg2+ pocket stabilizers","RNA-ligand intercalating agents"]}
"""

response = query_ollama_prompt_stdin(prompt, "deepseek-r1:7b")
print("Ollama response:", response)
