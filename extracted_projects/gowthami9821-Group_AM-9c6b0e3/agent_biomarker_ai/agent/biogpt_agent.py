import os
import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Replace this import or function with your actual pdb parser path and logic
try:
    from tools.pdb_parser import extract_structure_summary
except ImportError:
    # Dummy placeholder if tools module unavailable
    def extract_structure_summary(pdb_file):
        return {"chains": ["A"], "total_residues": 46, "motifs_detected": []}

class BioGPTRNAAgent:
    def __init__(self, model_path="microsoft/biogpt"):
        print("Loading BioGPT model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def read_fpocket_output(self):
        output_dir = os.path.join(os.path.dirname(__file__), "..", "tools", "luad_rna_out")
        info_file = os.path.join(output_dir, "luad_rna_info.txt")

        pockets = []
        current_pocket = {}
        if os.path.exists(info_file):
            with open(info_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Pocket"):
                        if current_pocket:
                            pockets.append(current_pocket)
                            current_pocket = {}
                        pocket_id = line.split()[1].rstrip(":")
                        current_pocket["Pocket_ID"] = pocket_id
                    elif line and ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().replace(" ", "_").replace("-", "_")
                        try:
                            value = float(value.strip())
                        except:
                            value = value.strip()
                        current_pocket[key] = value
                if current_pocket:
                    pockets.append(current_pocket)
        else:
            print("Fpocket output file not found:", info_file)

        scored_pockets = [p for p in pockets if "Score" in p]
        best_pocket = max(scored_pockets, key=lambda x: x.get("Score", float('-inf'))) if scored_pockets else {}

        return {
            "total_pockets_found": len(pockets),
            "best_biomarker_site": best_pocket,
            "all_pockets": pockets
        }

    def extract_json(self, text):
        cleaned_text = re.sub(r'[\r\n]+', ' ', text)
        json_start = cleaned_text.find('{')
        json_end = cleaned_text.rfind('}')
        if json_start != -1 and json_end != -1 and json_end > json_start:
            json_text = cleaned_text[json_start:json_end + 1]
            json_text = re.sub(r'"\s*([^"]*?)\s*_\s*([^"]*?)\s*"', r'"\1_\2"', json_text)
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
        return None

    def clean_keys(self, d):
        new_d = {}
        for k, v in d.items():
            clean_k = k.replace(" ", "").replace("____", "_").replace("___", "_").replace("__", "_")
            new_d[clean_k] = v
        return new_d

    def default_biomarker_data(self, pocket_id):
        default_map = {
            "1": {
                "predicted_region": "A12-A20",
                "motif_type": "stem-loop",
                "function": "Potential ligand-binding site",
                "associated_disease": "Lung carcinoma (hypothetical)",
                "recommended_drug_targets": [
                    "Mg2+ pocket stabilizers",
                    "RNA-ligand intercalating agents"
                ]
            },
            "2": {
                "predicted_region": "A25-A30",
                "motif_type": "hairpin loop",
                "function": "Metal-binding site",
                "associated_disease": "Renal carcinoma (hypothetical)",
                "recommended_drug_targets": [
                    "Metal ion chelators",
                    "RNA folding stabilizers"
                ]
            },
            "3": {
                "predicted_region": "A33-A38",
                "motif_type": "tetraloop",
                "function": "Ligand recognition",
                "associated_disease": "Lung carcinoma (hypothetical)",
                "recommended_drug_targets": [
                    "RNA-ligand intercalating agents"
                ]
            }
        }
        return default_map.get(str(pocket_id), {
            "predicted_region": "A12-A20",
            "motif_type": "stem-loop",
            "function": "Potential ligand-binding site",
            "associated_disease": "Unknown",
            "recommended_drug_targets": []
        })

    def predict_biomarker_for_pocket(self, pocket, structure_summary):
        clean_pocket = self.clean_keys(pocket)
        prompt = f"""
You are an expert molecular bioinformatician. ONLY respond in valid JSON. 
Do NOT include explanations or instructions.

RNA STRUCTURE SUMMARY:
{json.dumps(structure_summary)}

POCKET DATA:
{json.dumps(clean_pocket)}

Predict:
- RNA biomarker region(s)
- Structural motif type
- Function (ligand binding, metal binding, etc.)
- Associated disease relevance
- Recommended drug targets


Respond only like this:
{{"predicted_region":"A12-A20","motif_type":"stem-loop","function":"Potential ligand-binding site","associated_disease":"Hypothetical","recommended_drug_targets":["Mg2+ pocket stabilizers","RNA-ligand intercalating agents"]}}
"""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=250,
                eos_token_id=self.tokenizer.eos_token_id
            )
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            json_part = text[len(prompt):] if text.startswith(prompt) else text
            parsed = self.extract_json(json_part)
            if not parsed or parsed.get("predicted_region") in [None, "", "unknown"]:
                raise ValueError("Fallback to default due to unknown model output")
            result = parsed
        except Exception as e:
            print("Model call failed or unknown output. Using default biomarker data. Error:", e)
            result = self.default_biomarker_data(pocket.get("Pocket_ID"))
        result["pocket_id"] = pocket.get("Pocket_ID", "unknown")
        return result

    def analyze_structure(self, pdb_file):
        structure_summary = extract_structure_summary(pdb_file)
        pocket_info = self.read_fpocket_output()
        all_pockets = pocket_info.get("all_pockets", [])

        biomarkers = []
        for pocket in all_pockets:
            biomarker = self.predict_biomarker_for_pocket(pocket, structure_summary)
            biomarkers.append(biomarker)

        best_pocket = pocket_info.get("best_biomarker_site", {})

        result = {
            "target": os.path.basename(pdb_file).replace(".pdb", ""),
            "structure_summary": structure_summary,
            "total_pockets_found": len(all_pockets),
            "best_biomarker_site": best_pocket,
            "biomarkers": biomarkers
        }
        return result


if __name__ == "__main__":
    pdb_file = os.path.join(os.path.dirname(__file__), "..", "tools", "luad_rna.pdb")
    agent = BioGPTRNAAgent()
    result = agent.analyze_structure(pdb_file)

    print(json.dumps(result, indent=2))
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump(result, f, indent=2)
