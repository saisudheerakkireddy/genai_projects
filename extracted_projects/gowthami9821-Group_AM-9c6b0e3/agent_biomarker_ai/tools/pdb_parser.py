from Bio.PDB import PDBParser
from math import sqrt

def distance(atom1, atom2):
    """Euclidean distance between two atoms"""
    diff = atom1.coord - atom2.coord
    return sqrt(sum(diff*diff))

def extract_structure_summary(pdb_file, pair_distance=4.0):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("RNA", pdb_file)

    motifs = []
    chains_info = []

    for chain in structure.get_chains():
        residues = list(chain.get_residues())
        chain_id = chain.id
        chains_info.append(chain_id)

        paired = [False] * len(residues)

        # Detect paired residues
        for i in range(len(residues)):
            for j in range(i+1, len(residues)):
                try:
                    # Use N1 for pyrimidines (C,U) and N9 for purines (A,G)
                    atom_i = residues[i]['N1'] if residues[i].resname in ['C','U'] else residues[i]['N9']
                    atom_j = residues[j]['N1'] if residues[j].resname in ['C','U'] else residues[j]['N9']
                    if distance(atom_i, atom_j) <= pair_distance:
                        paired[i] = True
                        paired[j] = True
                except KeyError:
                    continue  # skip residues without the key atom

        # Detect motifs based on pairing pattern
        i = 0
        while i < len(residues):
            if paired[i]:
                # Stem start
                stem_start = i
                while i < len(residues) and paired[i]:
                    i += 1
                stem_end = i - 1
                # Check for hairpin/loop after stem
                loop_start = i
                loop_end = i
                while loop_end < len(residues) and not paired[loop_end]:
                    loop_end += 1
                if loop_end - loop_start >= 3:  # minimum loop size
                    motifs.append({
                        "type": "hairpin",
                        "chain": chain_id,
                        "residues": (stem_start, loop_end - 1)
                    })
                else:
                    # internal bulge
                    if loop_end - loop_start > 0:
                        motifs.append({
                            "type": "internal bulge",
                            "chain": chain_id,
                            "residues": (loop_start, loop_end - 1)
                        })
                i = loop_end
            else:
                i += 1

    return {
        "chains": chains_info,
        "total_residues": sum(1 for _ in structure.get_residues()),
        "motifs_detected": motifs
    }

# Example usage
if __name__ == "__main__":
    pdb_file = "luad_rna.pdb"
    summary = extract_structure_summary(pdb_file)
    print(summary)
