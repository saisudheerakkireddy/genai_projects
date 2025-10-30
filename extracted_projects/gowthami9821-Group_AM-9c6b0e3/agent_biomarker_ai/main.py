from agent.biogpt_agent import BioGPTRNAAgent
import json

if __name__ == "__main__":
    pdb_file = "tools/luad_rna.pdb"
    agent = BioGPTRNAAgent()

    print("\n[INFO] Running Agentic Biomarker Detection...\n")
    results = agent.analyze_structure(pdb_file)

    with open("outputs/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("[DONE] Results saved to outputs/results.json")
