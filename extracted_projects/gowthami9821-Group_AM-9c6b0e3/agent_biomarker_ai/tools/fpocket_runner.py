import subprocess
import os

def run_fpocket(pdb_file):
    """
    Run fpocket tool on RNA PDB structure.
    If fpocket not installed, return dummy data.
    """
    if os.system("which fpocket > /dev/null 2>&1") == 0:
        subprocess.run(["fpocket", "-f", pdb_file])
        # TODO: Parse fpocket output here
    else:
        return {
            "total_pockets_found": 00000000,
            "best_biomarker_site": {
                "Pocket_ID": "FAKE_001",
                "X": 4.966,
                "Y": 5.7,
                "Z": 1.146,
                "Volume": 463.99,
                "Hydrophobicity": 0.54,
                "Score": 1.0071
            }
        }
