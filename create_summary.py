import json
import os
import sys
import csv
from datetime import datetime

def create_summary_reports(output_dir):
    """Creates summary reports from individual JSON reports."""
    reports_dir = os.path.join(output_dir, "reports")
    all_reports = []
    for filename in os.listdir(reports_dir):
        if filename.endswith(".json"):
            with open(os.path.join(reports_dir, filename), "r") as f:
                all_reports.append(json.load(f))

    # Sort reports by weighted score with tie-breakers: Use of AI → Technical Execution → Innovation → Presentation
    all_reports.sort(
        key=lambda x: (
            x.get("scores", {}).get("weighted_score_percent", 0),
            x.get("scores", {}).get("use_of_ai", 0),
            x.get("scores", {}).get("technical_execution", 0),
            x.get("scores", {}).get("innovation", 0),
            x.get("scores", {}).get("presentation", 0),
        ),
        reverse=True,
    )

    # --- Create all_repos_summary.csv ---
    with open(os.path.join(output_dir, "all_repos_summary.csv"), "w", newline="") as csvfile:
        fieldnames = [
            "repo_name",
            "path",
            "weighted_score_percent",
            "classification",
            "top_line_summary",
            "reproducible"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for report in all_reports:
            classification = report.get("classification", "N/A")
            if isinstance(classification, list):
                classification = ", ".join(map(str, classification))
            else:
                classification = str(classification)

            notes = report.get("notes_for_judges", "")
            if isinstance(notes, list):
                notes = ", ".join(map(str, notes))
            else:
                notes = str(notes)

            score = report.get("scores", {}).get("weighted_score_percent", 0)
            if not isinstance(score, (int, float)):
                score = 0
            
            writer.writerow({
                "repo_name": report.get("name", "Unknown"),
                "path": report.get("id", "Unknown"),
                "weighted_score_percent": score,
                "classification": classification,
                "top_line_summary": notes,
                "reproducible": bool(report.get("reproducible", False)),
            })

    # --- Create full_report.json ---
    with open(os.path.join(output_dir, "full_report.json"), "w") as f:
        json.dump(all_reports, f, indent=4)

    # --- Create top10_by_score.md ---
    with open(os.path.join(output_dir, "top10_by_score.md"), "w") as f:
        f.write("# Top 10 Repositories by Score\n\n")
        for i, report in enumerate(all_reports[:10]):
            f.write(
                f"{i+1}. {report['name']} - {report['scores']['weighted_score_percent']:.2f}%\n"
            )
            
    # --- Create winners_recommendation.md ---
    with open(os.path.join(output_dir, "winners_recommendation.md"), "w") as f:
        f.write("# Winners Recommendation\n\n")
        for i, report in enumerate(all_reports[:3]):
            f.write(f"## Rank {i+1}: {report['name']}\n")
            f.write(f"**Score:** {report['scores']['weighted_score_percent']:.2f}%\n")
            f.write(f"**Justification:** {report['notes_for_judges']}\n\n")


    # --- Create anomalies.csv ---
    with open(os.path.join(output_dir, "anomalies.csv"), "w", newline="") as csvfile:
        fieldnames = ["repo_name", "tool", "description", "details"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for report in all_reports:
            risks = report.get("risks", {})
            for tool, findings in risks.items():
                if isinstance(findings, list):
                    for finding in findings:
                        writer.writerow({
                            "repo_name": report["name"],
                            "tool": tool,
                            "description": finding.get("Description", "N/A"),
                            "details": json.dumps(finding)
                        })

    # --- Create overall_report.md ---
    with open(os.path.join(output_dir, "overall_report.md"), "w") as f:
        f.write("# Overall Hackathon Evaluation Report\n\n")
        f.write("## Summary\n")
        avg_score = sum(r["scores"]["weighted_score_percent"] for r in all_reports) / len(all_reports)
        reproducible_builds = sum(1 for r in all_reports if r["reproducible"])
        demo_links = sum(1 for r in all_reports if r["presentation_link_detected"])
        
        f.write(f"- **Total Repositories Evaluated:** {len(all_reports)}\n")
        f.write(f"- **Average Score:** {avg_score:.2f}%\n")
        f.write(f"- **Reproducible Builds:** {reproducible_builds} ({reproducible_builds/len(all_reports):.1%})\n")
        f.write(f"- **Projects with Demo Links:** {demo_links} ({demo_links/len(all_reports):.1%})\n\n")

        f.write("## Full Summary Table\n")
        f.write("| Rank | Repository | Score | Classification | Reproducible | Demo |\n")
        f.write("|------|------------|-------|----------------|--------------|------|\n")
        for i, report in enumerate(all_reports):
            f.write(f"| {i+1} | {report['name']} | {report['scores']['weighted_score_percent']:.2f}% | {report['classification']} | {'Yes' if report['reproducible'] else 'No'} | {'Yes' if report['presentation_link_detected'] else 'No'} |\n")

    # --- Create final_validation_report.md ---
    with open(os.path.join(output_dir, "final_validation_report.md"), "w") as f:
        f.write("### FINAL VALIDATION SUMMARY\n\n")
        f.write(f"* Evaluation completed: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"* Total evaluated: {len(all_reports)}\n")
        
        demo_links = sum(1 for r in all_reports if r["presentation_link_detected"])
        f.write(f"* Valid demo/presentation links: {demo_links}\n")
        
        avg_score = sum(r["scores"]["weighted_score_percent"] for r in all_reports) / len(all_reports)
        f.write(f"* Average weighted score: {avg_score:.2f}\n")
        
        reproducible_builds = sum(1 for r in all_reports if r["reproducible"])
        f.write(f"* Reproducible builds: {reproducible_builds}\n")

        deductions_applied = sum(1 for r in all_reports if r.get("penalties_applied"))
        f.write(f"* Evidence deductions applied: {deductions_applied} repos\n")

        security_alerts = sum(len(r.get("risks", {}).get("gitleaks", [])) for r in all_reports)
        f.write(f"* Security alerts: {security_alerts}\n")
        f.write(f"* Winners: {', '.join([r['name'] for r in all_reports[:3]])}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_summary.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    create_summary_reports(output_dir)
    print("Summary reports created successfully.")

if __name__ == "__main__":
    main()
