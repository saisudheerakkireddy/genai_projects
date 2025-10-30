import { useEffect, useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Plus, Search, Brain, Dna, CheckCircle, ChevronDown, ChevronUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface PatientDetails {
  fullName?: string;
}

interface RnaAnalysisFormProps {
  patientDetails: PatientDetails;
  prompt?: string;
  setPrompt?: (value: string) => void;
  patientFile?: File | null;
  setPatientFile?: (file: File | null) => void;
  isAnalyzing?: boolean;
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleAnalyze?: () => void;
}

const RnaAnalysisForm: React.FC<RnaAnalysisFormProps> = ({
  patientDetails,
  prompt,
  setPrompt,
  patientFile,
  setPatientFile,
  isAnalyzing,
  handleFileChange,
  handleAnalyze,
}) => {
  const viewerRef = useRef<HTMLDivElement>(null);
  const [scriptLoaded, setScriptLoaded] = useState(false);
  const [pdbInput, setPdbInput] = useState("");
  const [metadata, setMetadata] = useState("Metadata will appear here...");
  const [showToasts, setShowToasts] = useState(false);
  const [toastIndex, setToastIndex] = useState(0);
  const [showResultBox, setShowResultBox] = useState(false);
  const [showDrugAnalysis, setShowDrugAnalysis] = useState(false);
  const [expandedPocket, setExpandedPocket] = useState<number>(1);

  const analysisSteps = [
    { 
      icon: Search, 
      text: "Initializing protein structure analysis...", 
      subtext: "Loading PDB data and preprocessing molecular geometry",
      progress: 15
    },
    { 
      icon: Dna, 
      text: "Analyzing molecular pockets and binding sites...", 
      subtext: "Computing alpha spheres and surface accessibility",
      progress: 35
    },
    { 
      icon: Brain, 
      text: "Detecting cancer biomarkers and mutations...", 
      subtext: "Scanning for oncogenic signatures in RNA sequences",
      progress: 60
    },
    { 
      icon: Search, 
      text: "Calculating druggability scores...", 
      subtext: "Evaluating therapeutic potential of identified pockets",
      progress: 80
    },
    { 
      icon: CheckCircle, 
      text: "Analysis complete - Results ready", 
      subtext: "Found 8 potential binding pockets with detailed metrics",
      progress: 100
    },
  ];

  const biomarkerData = [
    {
      pocket_id: "1",
      predicted_region: "A12-A20",
      motif_type: "stem-loop",
      function: "Potential ligand-binding site",
      associated_disease: "Lung carcinoma (hypothetical)",
      recommended_drug_targets: [
        "Mg2+ pocket stabilizers",
        "RNA-ligand intercalating agents"
      ]
    },
    {
      pocket_id: "2",
      predicted_region: "A25-A30",
      motif_type: "hairpin loop",
      function: "Metal-binding site",
      associated_disease: "Renal carcinoma (hypothetical)",
      recommended_drug_targets: [
        "Metal ion chelators",
        "RNA folding stabilizers"
      ]
    },
    {
      pocket_id: "3",
      predicted_region: "A33-A38",
      motif_type: "tetraloop",
      function: "Ligand recognition",
      associated_disease: "Lung carcinoma (hypothetical)",
      recommended_drug_targets: [
        "RNA-ligand intercalating agents"
      ]
    }
  ];

  const pocketData = [
    {
      pocket: 1,
      score: 0.043,
      druggabilityScore: 0.000,
      alphaSpheresCount: 98,
      totalSASA: 349.937,
      polarSASA: 281.102,
      apolarSASA: 68.835,
      volume: 1620.036,
      meanLocalHydrophobicDensity: 3.000,
      meanAlphaSphereRadius: 4.284,
      meanAlphaSphSolventAccess: 0.557,
      apolarAlphaSphereProporti: 0.041,
      hydrophobicityScore: 4.083,
      volumeScore: 3.333,
      polarityScore: 8,
      chargeScore: 0,
      proportionPolarAtoms: 67.105,
      alphaSphereDensity: 7.494,
      centMassAlphaSphereMaxDist: 19.006,
      flexibility: 0.000
    },
    {
      pocket: 2,
      score: -0.027,
      druggabilityScore: 0.000,
      alphaSpheresCount: 21,
      totalSASA: 106.877,
      polarSASA: 93.593,
      apolarSASA: 13.284,
      volume: 433.755,
      meanLocalHydrophobicDensity: 0.000,
      meanAlphaSphereRadius: 4.235,
      meanAlphaSphSolventAccess: 0.608,
      apolarAlphaSphereProporti: 0.000,
      hydrophobicityScore: 3.167,
      volumeScore: 2.500,
      polarityScore: 3,
      chargeScore: 0,
      proportionPolarAtoms: 73.684,
      alphaSphereDensity: 3.600,
      centMassAlphaSphereMaxDist: 6.916,
      flexibility: 0.000
    },
    {
      pocket: 3,
      score: -0.045,
      druggabilityScore: 0.000,
      alphaSpheresCount: 15,
      totalSASA: 70.878,
      polarSASA: 53.971,
      apolarSASA: 16.907,
      volume: 216.877,
      meanLocalHydrophobicDensity: 0.000,
      meanAlphaSphereRadius: 3.865,
      meanAlphaSphSolventAccess: 0.533,
      apolarAlphaSphereProporti: 0.067,
      hydrophobicityScore: 12.000,
      volumeScore: 2.600,
      polarityScore: 2,
      chargeScore: 0,
      proportionPolarAtoms: 53.846,
      alphaSphereDensity: 2.254,
      centMassAlphaSphereMaxDist: 5.384,
      flexibility: 0.000
    }
  ];

  useEffect(() => {
    if (showToasts && toastIndex < analysisSteps.length) {
      const timer = setTimeout(() => setToastIndex(prev => prev + 1), 2000);
      return () => clearTimeout(timer);
    } else if (showToasts && toastIndex === analysisSteps.length) {
      const fadeTimer = setTimeout(() => {
        setShowToasts(false);
        setToastIndex(0);
        setShowResultBox(true);
      }, 1500);
      return () => clearTimeout(fadeTimer);
    }
  }, [showToasts, toastIndex]);

  useEffect(() => {
    if ((window as any).NGL) {
      setScriptLoaded(true);
      if (viewerRef.current) {
        (window as any).nglStage = new (window as any).NGL.Stage(viewerRef.current);
      }
      return;
    }

    const script = document.createElement("script");
    script.src = "https://unpkg.com/ngl@latest/dist/ngl.js";
    script.async = true;
    script.onload = () => {
      setScriptLoaded(true);
      if (viewerRef.current && (window as any).NGL) {
        (window as any).nglStage = new (window as any).NGL.Stage(viewerRef.current);
      }
    };
    document.body.appendChild(script);
  }, []);

  const handleLoadStructure = () => {
  const pdbId = pdbInput.trim().toLowerCase();
  if (!pdbId || !(window as any).nglStage) return;

  const stage = (window as any).nglStage;
  stage.removeAllComponents();
  stage.loadFile(rcsb://${pdbId}, { defaultRepresentation: true }).then((component: any) => {
    component.autoView();
  });

  fetch(https://data.rcsb.org/rest/v1/core/entry/${pdbId})
    .then((res) => res.json())
    .then((entryData) => {
      const title = entryData.struct?.title || "N/A";
      const method = entryData.exptl?.[0]?.method || "N/A";
      const resolution = entryData.rcsb_entry_info?.resolution_combined?.[0] || "N/A";

      const entityIds = entryData.rcsb_entry_container_identifiers?.non_polymer_entity_ids || [];

      if (entityIds.length === 0) {
        setMetadata(
          🔬 Title: ${title}\n🧪 Method: ${method}\n📏 Resolution: ${resolution} Å\n❌ No ligand found.
        );
        return;
      }

      const entityId = entityIds[0];
      return fetch(https://data.rcsb.org/rest/v1/core/nonpolymer_entity/${pdbId}/${entityId})
        .then((res) => res.json())
        .then((entityData) => {
          const name = entityData.pdbx_entity_nonpoly?.name || "N/A";
          const compId = entityData.pdbx_entity_nonpoly?.comp_id || "N/A";

          setMetadata(
            🔬 Title: ${title}\n🧪 Method: ${method}\n📏 Resolution: ${resolution} Å\n🧬 Ligand: ${name} (${compId})
          );
        });
    })
    .catch((err) => {
      console.error("Metadata fetch error:", err);
      setMetadata("❌ Error fetching metadata.");
    });
};



  const getValueColor = (label: string, value: number): string => {
    // High values (attention needed) - orange/red
    if (label.includes("Score") || label.includes("SASA") || label.includes("Volume") || label.includes("Alpha Spheres")) {
      if (value > 100) return "bg-orange-500/20 border-orange-400/30";
      if (value > 50) return "bg-amber-500/20 border-amber-400/30";
    }
    
    // Proportions and ratios
    if (label.includes("proportion") || label.includes("density") || label.includes("radius")) {
      if (value > 5) return "bg-rose-500/20 border-rose-400/30";
      if (value > 2) return "bg-emerald-500/20 border-emerald-400/30";
    }
    
    // Low/Zero values - blue/gray
    if (value === 0) return "bg-slate-500/20 border-slate-400/30";
    if (value < 1) return "bg-blue-500/20 border-blue-400/30";
    
    // Default neutral - green
    return "bg-emerald-500/20 border-emerald-400/30";
  };

  const getTextColor = (label: string, value: number): string => {
    if (label.includes("Score") || label.includes("SASA") || label.includes("Volume") || label.includes("Alpha Spheres")) {
      if (value > 100) return "text-orange-300";
      if (value > 50) return "text-amber-300";
    }
    
    if (label.includes("proportion") || label.includes("density") || label.includes("radius")) {
      if (value > 5) return "text-rose-300";
      if (value > 2) return "text-emerald-300";
    }
    
    if (value === 0) return "text-slate-300";
    if (value < 1) return "text-blue-300";
    
    return "text-emerald-300";
  };

  const renderPocketProperty = (label: string, value: number | string) => {
    const numValue = typeof value === 'number' ? value : 0;
    const bgColor = getValueColor(label, numValue);
    const textColor = getTextColor(label, numValue);
    
    return (
      <div className={flex flex-col py-3 px-4 rounded-lg border ${bgColor} backdrop-blur-sm}>
        <span className="text-xs font-medium text-gray-200 mb-1">{label}</span>
        <span className={text-lg font-bold ${textColor}}>
          {typeof value === 'number' ? value.toFixed(3) : value}
        </span>
      </div>
    );
  };


  return (
    <Card>
      <CardHeader>
        <CardTitle>RNA Analysis Parameters</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-1">
                RNA sequence prompt
            </label>
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-medium mb-2">NGL Viewer: Protein/RNA 3D View</h3>
            <div className="flex items-center gap-2 mb-4">
              <Input
                placeholder="Enter PDB ID (e.g. 8RBJ)"
                value={pdbInput}
                onChange={(e) => setPdbInput(e.target.value)}
                className="w-1/2"
              />
              <Button onClick={handleLoadStructure} disabled={!scriptLoaded}>
                Load
              </Button>
            </div>
            <div
              id="viewport"
              ref={viewerRef}
              style={{
                width: "100%",
                height: "500px",
                border: "1px solid #ccc",
                borderRadius: "8px",
              }}
            />
            <div className="mt-4 p-4 border rounded-md bg-muted text-sm" style={{ whiteSpace: "pre-wrap", fontFamily: "monospace" }}>
              {metadata}
            </div>
          </div>

          <div className="flex justify-center mt-8">
            <Button
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md shadow-md"
              onClick={() => {
                setShowToasts(true);
                setShowResultBox(false);
              }}
            >
              Continue for Biomarker Detection
            </Button>
          </div>

          <AnimatePresence>
            {showResultBox && (
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.8 }}
                className="mt-8 relative overflow-hidden rounded-xl border border-green-200 dark:border-green-800 bg-gradient-to-br from-green-50 via-white to-emerald-50 dark:from-gray-900 dark:via-gray-800 dark:to-green-950 shadow-lg"
              >
                <div className="relative w-full h-[400px] overflow-hidden rounded-lg">
                <iframe
                  src="https://www.leskoff.com/s01815-0"
                  className="absolute top-[-100px] left-0 w-full h-[450px] border-0"
                  scrolling="no"
                  title="Converter"
                />
              </div>
                <div className="absolute top-0 right-0 w-64 h-64 bg-green-200 dark:bg-green-900 rounded-full blur-3xl opacity-20 -translate-y-1/2 translate-x-1/2"></div>

                <div className="relative p-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                      <span className="text-2xl">🧬</span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">
                      Biomarker Detection Summary
                    </h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
                      <span className="text-xs uppercase tracking-wide font-semibold text-gray-500 dark:text-gray-400">Target</span>
                      <p className="text-lg font-bold text-gray-900 dark:text-gray-100 mt-1">LUAD_RNA</p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 shadow-sm">
                      <span className="text-xs uppercase tracking-wide font-semibold text-gray-500 dark:text-gray-400">Total Pockets</span>
                      <p className="text-lg font-bold text-gray-900 dark:text-gray-100 mt-1">3</p>
                    </div>
                  </div>

                  {/* Biomarker Highlights Section */}
                  <div className="mb-8">
                    <div className="bg-white dark:bg-gray-800/50 rounded-lg border border-green-200 dark:border-green-700/50 p-6 shadow-sm">
                      <div className="flex items-center gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
                        <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                          <Dna className="text-green-600 dark:text-green-400" size={20} />
                        </div>
                        <div>
                          <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                            Key Biomarkers Identified
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Critical RNA motifs with therapeutic potential
                          </p>
                        </div>
                      </div>

                      <div className="space-y-3">
                        {biomarkerData.map((biomarker) => (
                          <motion.div
                            key={biomarker.pocket_id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden hover:border-green-300 dark:hover:border-green-600 transition-colors"
                          >
                            <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 px-4 py-2.5 border-b border-gray-200 dark:border-gray-700">
                              <div className="flex items-center justify-between">
                                <span className="text-gray-900 dark:text-gray-100 font-semibold text-sm">
                                  Pocket {biomarker.pocket_id} • {biomarker.predicted_region}
                                </span>
                                <span className="px-2.5 py-1 bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-300 rounded-md text-xs font-medium border border-green-200 dark:border-green-700">
                                  {biomarker.motif_type}
                                </span>
                              </div>
                            </div>

                            <div className="p-4 space-y-3">
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                  <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                                    Function
                                  </span>
                                  <p className="text-sm text-gray-900 dark:text-gray-100 mt-1 font-medium">
                                    {biomarker.function}
                                  </p>
                                </div>

                                <div>
                                  <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                                    Associated Disease
                                  </span>
                                  <p className="text-sm text-red-600 dark:text-red-400 mt-1 font-bold">
                                    {biomarker.associated_disease}
                                  </p>
                                </div>
                              </div>

                              <div>
                                <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2 block">
                                  Recommended Drug Targets
                                </span>
                                <div className="flex flex-wrap gap-2">
                                  {biomarker.recommended_drug_targets.map((target, idx) => (
                                    <span
                                      key={idx}
                                      className="px-3 py-1.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-xs font-medium border border-blue-200 dark:border-blue-800"
                                    >
                                      {target}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Detailed Pocket Analysis Section */}
                  <div className="mb-6">
                    <h4 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4 flex items-center gap-2">
                      <Brain size={20} className="text-green-600" />
                      Detailed Pocket Analysis
                    </h4>
                  </div>

                  <div className="flex flex-wrap gap-3 mb-6">
                    {pocketData.map((pocket) => (
                      <Button
                        key={pocket.pocket}
                        onClick={() => setExpandedPocket(pocket.pocket)}
                        className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                          expandedPocket === pocket.pocket
                            ? "bg-green-600 hover:bg-green-700 text-white shadow-lg"
                            : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600"
                        }`}
                      >
                        Pocket {pocket.pocket}
                      </Button>
                    ))}
                  </div>

                  <AnimatePresence mode="wait">
                    {pocketData
                      .filter((pocket) => pocket.pocket === expandedPocket)
                      .map((pocket) => (
                        <motion.div
                          key={pocket.pocket}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -20 }}
                          transition={{ duration: 0.3 }}
                          className="bg-gradient-to-br from-slate-800 to-slate-900 dark:from-slate-900 dark:to-black rounded-xl shadow-xl p-6"
                        >
                          <div className="mb-6 pb-4 border-b border-white/20">
                            <h4 className="text-xl font-bold text-white flex items-center gap-3">
                              <span className="px-3 py-1 bg-white/20 rounded-full text-sm">
                                Pocket {pocket.pocket}
                              </span>
                              Score: {pocket.score.toFixed(3)}
                            </h4>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {renderPocketProperty("Score", pocket.score)}
                            {renderPocketProperty("Druggability Score", pocket.druggabilityScore)}
                            {renderPocketProperty("Number of Alpha Spheres", pocket.alphaSpheresCount)}
                            {renderPocketProperty("Total SASA", pocket.totalSASA)}
                            {renderPocketProperty("Polar SASA", pocket.polarSASA)}
                            {renderPocketProperty("Apolar SASA", pocket.apolarSASA)}
                            {renderPocketProperty("Volume", pocket.volume)}
                            {renderPocketProperty("Mean local hydrophobic density", pocket.meanLocalHydrophobicDensity)}
                            {renderPocketProperty("Mean alpha sphere radius", pocket.meanAlphaSphereRadius)}
                            {renderPocketProperty("Mean alp. sph. solvent access", pocket.meanAlphaSphSolventAccess)}
                            {renderPocketProperty("Apolar alpha sphere proportion", pocket.apolarAlphaSphereProporti)}
                            {renderPocketProperty("Hydrophobicity score", pocket.hydrophobicityScore)}
                            {renderPocketProperty("Volume score", pocket.volumeScore)}
                            {renderPocketProperty("Polarity score", pocket.polarityScore)}
                            {renderPocketProperty("Charge score", pocket.chargeScore)}
                            {renderPocketProperty("Proportion of polar atoms", pocket.proportionPolarAtoms)}
                            {renderPocketProperty("Alpha sphere density", pocket.alphaSphereDensity)}
                            {renderPocketProperty("Cent. of mass - Alpha Sphere max dist", pocket.centMassAlphaSphereMaxDist)}
                            {renderPocketProperty("Flexibility", pocket.flexibility)}
                          </div>
                        </motion.div>
                      ))}
                  </AnimatePresence>

                  <div className="flex justify-center mt-6">
                    <Button
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md shadow-md"
                      onClick={() => setShowDrugAnalysis(true)}
                    >
                      Drug Analysis
                    </Button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showDrugAnalysis && (
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.8 }}
                className="mt-8 relative overflow-hidden rounded-xl border border-blue-200 dark:border-blue-800 bg-white dark:bg-gray-900 shadow-lg"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">
                      Drug Analysis Dashboard
                    </h3>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setShowDrugAnalysis(false)}
                    >
                      Close
                    </Button>
                  </div>
                  <iframe
                    src="http://127.0.0.1:5001/"
                    className="w-full h-[2080px] border-0 rounded-lg"
                    // scrolling="no"
                    title="Drug Analysis"
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showToasts && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="fixed bottom-6 right-6 z-50 w-[480px] bg-white dark:bg-gray-900 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden"
              >
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                      <Brain className="text-white" size={20} />
                    </div>
                    <div>
                      <h3 className="text-white font-bold text-lg">Biomarker Detection</h3>
                      <p className="text-blue-100 text-xs">RNA Analysis in Progress</p>
                    </div>
                  </div>
                </div>

                <div className="p-6 space-y-4">
                  {analysisSteps.slice(0, toastIndex + 1).map((step, idx) => {
                    const Icon = step.icon;
                    const isActive = idx === toastIndex;
                    const isComplete = idx < toastIndex;
                    
                    return (
                      <motion.div
                        key={idx}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: idx * 0.1 }}
                        className={`relative pl-8 pb-4 ${idx < analysisSteps.length - 1 ? 'border-l-2' : ''} ${
                          isComplete ? 'border-green-500' : isActive ? 'border-blue-500' : 'border-gray-300'
                        }`}
                      >
                        <div className={`absolute left-0 top-0 -translate-x-1/2 w-6 h-6 rounded-full flex items-center justify-center ${
                          isComplete ? 'bg-green-500' : isActive ? 'bg-blue-500' : 'bg-gray-300'
                        }`}>
                          <Icon size={14} className="text-white" />
                        </div>
                        
                        <div className="space-y-1">
                          <p className={`text-sm font-semibold ${
                            isComplete ? 'text-gray-600 dark:text-gray-400' : 'text-gray-900 dark:text-gray-100'
                          }`}>
                            {step.text}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-500">
                            {step.subtext}
                          </p>
                          
                          {isActive && (
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: "100%" }}
                              className="mt-2"
                            >
                              <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400 mb-1">
                                <span>Progress</span>
                                <span className="font-bold text-blue-600">{step.progress}%</span>
                              </div>
                              <div className="h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                <motion.div
                                  initial={{ width: 0 }}
                                  animate={{ width: ${step.progress}% }}
                                  transition={{ duration: 1.5, ease: "easeOut" }}
                                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                                />
                              </div>
                            </motion.div>
                          )}
                        </div>
                      </motion.div>
                    );
                  })}
                </div>

                {toastIndex === analysisSteps.length - 1 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="px-6 pb-6"
                  >
                    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                      <div className="flex items-center gap-2 text-green-700 dark:text-green-400">
                        <CheckCircle size={18} />
                        <span className="text-sm font-semibold">Analysis completed successfully</span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </CardContent>
    </Card>
  );


export default RnaAnalysisForm;