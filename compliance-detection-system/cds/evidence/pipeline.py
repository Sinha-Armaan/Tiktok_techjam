"""
Evidence Pipeline Module

This module provides the main pipeline for processing datasets through
the complete compliance detection workflow.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import pandas as pd
from jinja2 import Template

from .models import FinalRecord
from ..scanner.main import scan_repository
from ..rules.main import evaluate_feature
from ..llm.main import explain_feature

logger = logging.getLogger(__name__)


class CSVExporter:
    """CSV export functionality for final results"""
    
    def __init__(self):
        self.required_columns = [
            "feature_id", "requires_geo_logic", "reasoning", "related_regulations",
            "confidence", "matched_rules", "missing_controls", "evidence_refs",
            "code_refs", "runtime_observation", "needs_review", "severity", "created_at"
        ]
    
    def export_results(self, results: List[FinalRecord], output_path: Path) -> None:
        """Export results to CSV format"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.required_columns)
            writer.writeheader()
            
            for result in results:
                row = result.model_dump()
                # Convert lists to string representation
                for col in ["related_regulations", "matched_rules", "missing_controls", "evidence_refs", "code_refs"]:
                    if col in row and isinstance(row[col], list):
                        row[col] = "; ".join(row[col])
                
                # Format datetime
                if "created_at" in row:
                    row["created_at"] = row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"])
                
                writer.writerow(row)
        
        logger.info(f"Exported {len(results)} results to {output_path}")


class HTMLReporter:
    """HTML report generation using Jinja2 templates"""
    
    def __init__(self):
        self.template = self._get_html_template()
    
    def generate_report(self, results: List[FinalRecord], output_path: Path, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Generate HTML compliance report"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare report data
        report_data = {
            "title": "Compliance Detection System Report",
            "generated_at": datetime.now().isoformat(),
            "total_features": len(results),
            "requires_geo_logic_count": sum(1 for r in results if r.requires_geo_logic),
            "high_severity_count": sum(1 for r in results if r.severity in ["high", "critical"]),
            "needs_review_count": sum(1 for r in results if r.needs_review),
            "results": results,
            "metadata": metadata or {}
        }
        
        # Add summary statistics
        if results:
            report_data["avg_confidence"] = sum(r.confidence for r in results) / len(results)
            severity_counts = {}
            for result in results:
                severity_counts[result.severity] = severity_counts.get(result.severity, 0) + 1
            report_data["severity_distribution"] = severity_counts
        
        # Render template
        html_content = self.template.render(**report_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML report: {output_path}")
    
    def _get_html_template(self) -> Template:
        """Get Jinja2 HTML template"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { border-bottom: 2px solid #007acc; padding-bottom: 20px; margin-bottom: 20px; }
        .header h1 { color: #007acc; margin: 0; }
        .header .subtitle { color: #666; margin-top: 5px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .summary-card { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; border-left: 4px solid #007acc; }
        .summary-card h3 { margin: 0 0 10px 0; font-size: 1.8em; color: #007acc; }
        .summary-card p { margin: 0; color: #666; }
        .results-section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .result-card { background: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 20px; }
        .result-header { display: flex; justify-content: between; align-items: center; margin-bottom: 15px; }
        .result-header h3 { margin: 0; color: #333; }
        .severity { padding: 3px 8px; border-radius: 3px; color: white; font-size: 0.8em; font-weight: bold; }
        .severity.low { background-color: #28a745; }
        .severity.medium { background-color: #ffc107; color: #000; }
        .severity.high { background-color: #fd7e14; }
        .severity.critical { background-color: #dc3545; }
        .confidence { float: right; color: #666; }
        .reasoning { margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; line-height: 1.5; }
        .regulations { margin: 10px 0; }
        .regulations ul { margin: 5px 0; padding-left: 20px; }
        .code-refs { margin: 10px 0; font-family: monospace; font-size: 0.9em; background: #f1f1f1; padding: 10px; border-radius: 5px; }
        .missing-controls { color: #d63031; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="subtitle">Generated on {{ generated_at }}</div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{{ total_features }}</h3>
                <p>Total Features</p>
            </div>
            <div class="summary-card">
                <h3>{{ requires_geo_logic_count }}</h3>
                <p>Require Geo Logic</p>
            </div>
            <div class="summary-card">
                <h3>{{ high_severity_count }}</h3>
                <p>High/Critical Severity</p>
            </div>
            <div class="summary-card">
                <h3>{{ needs_review_count }}</h3>
                <p>Need Review</p>
            </div>
            {% if avg_confidence %}
            <div class="summary-card">
                <h3>{{ "%.1f%%" | format(avg_confidence * 100) }}</h3>
                <p>Avg Confidence</p>
            </div>
            {% endif %}
        </div>
        
        <div class="results-section">
            <h2>Compliance Analysis Results</h2>
            
            {% for result in results %}
            <div class="result-card">
                <div class="result-header">
                    <h3>{{ result.feature_id }}</h3>
                    <div>
                        <span class="severity {{ result.severity }}">{{ result.severity.upper() }}</span>
                        <span class="confidence">{{ "%.0f%%" | format(result.confidence * 100) }} confidence</span>
                    </div>
                </div>
                
                <div class="reasoning">
                    <strong>Analysis:</strong> {{ result.reasoning }}
                </div>
                
                {% if result.related_regulations %}
                <div class="regulations">
                    <strong>Related Regulations:</strong>
                    <ul>
                        {% for reg in result.related_regulations %}
                        <li>{{ reg }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                {% if result.matched_rules %}
                <div class="matched-rules">
                    <strong>Matched Rules:</strong> {{ result.matched_rules | join(", ") }}
                </div>
                {% endif %}
                
                {% if result.missing_controls %}
                <div class="missing-controls">
                    <strong>Missing Controls:</strong> {{ result.missing_controls | join(", ") }}
                </div>
                {% endif %}
                
                {% if result.code_refs %}
                <div class="code-refs">
                    <strong>Code References:</strong><br>
                    {{ result.code_refs | join("<br>") }}
                </div>
                {% endif %}
                
                {% if result.runtime_observation %}
                <div class="runtime-obs">
                    <strong>Runtime Observations:</strong> {{ result.runtime_observation }}
                </div>
                {% endif %}
                
                {% if result.needs_review %}
                <div class="review-flag" style="color: #d63031; font-weight: bold; margin-top: 10px;">
                    ⚠️ Manual review recommended
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p>Generated by Compliance Detection System (CDS) v0.1.0</p>
            <p>This report contains compliance analysis based on static code analysis, runtime probing, and AI-powered reasoning.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return Template(template_str)


class CompliancePipeline:
    """Main compliance detection pipeline"""
    
    def __init__(self):
        self.csv_exporter = CSVExporter()
        self.html_reporter = HTMLReporter()
        self._scan_cache = {}  # Cache for scan results by repo_path
    
    def _get_scan_result(self, repo_path: Path, feature_id: str):
        """Get scan result from cache or perform new scan"""
        repo_str = str(repo_path.resolve())
        
        if repo_str not in self._scan_cache:
            if repo_path.exists():
                logger.info(f"Running scan for repository: {repo_path}")
                self._scan_cache[repo_str] = scan_repository(repo_path, feature_id)
            else:
                logger.warning(f"Repository not found: {repo_path}")
                self._scan_cache[repo_str] = None
        else:
            logger.debug(f"Using cached scan result for: {repo_path}")
        
        return self._scan_cache[repo_str]
    
    def run_pipeline(self, dataset_path: Path, output_csv: Path, 
                    report_html: Path) -> Dict[str, Any]:
        """Run complete compliance detection pipeline"""
        logger.info(f"Starting pipeline with dataset: {dataset_path}")
        
        # Load dataset
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")
        
        dataset = pd.read_csv(dataset_path)
        required_columns = ["feature_id"]
        
        if not all(col in dataset.columns for col in required_columns):
            raise ValueError(f"Dataset must contain columns: {required_columns}")
        
        results = []
        processed_count = 0
        error_count = 0
        
        for _, row in dataset.iterrows():
            feature_id = row["feature_id"]
            repo_path = Path(row.get("repo_path", "./dataset_variations/original_comprehensive_focused/enhanced_code"))
            
            try:
                logger.info(f"Processing feature: {feature_id}")
                
                # Step 1: Static scan (with caching to avoid duplicate scans)
                scan_result = self._get_scan_result(repo_path, feature_id)
                
                # Step 2: Rules evaluation
                rules_result = evaluate_feature(feature_id)
                
                # Step 3: LLM explanation
                final_record_data = explain_feature(feature_id)
                final_record = FinalRecord.model_validate(final_record_data)
                
                results.append(final_record)
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Failed to process {feature_id}: {e}")
                error_count += 1
                
                # Create error record
                error_record = FinalRecord(
                    feature_id=feature_id,
                    requires_geo_logic=False,
                    reasoning=f"Processing failed: {str(e)}",
                    confidence=0.0,
                    needs_review=True,
                    severity="critical"
                )
                results.append(error_record)
        
        # Export results
        self.csv_exporter.export_results(results, output_csv)
        
        # Generate HTML report
        metadata = {
            "dataset_path": str(dataset_path),
            "total_rows": len(dataset),
            "processed_count": processed_count,
            "error_count": error_count
        }
        self.html_reporter.generate_report(results, report_html, metadata)
        
        summary = {
            "total_features": len(dataset),
            "processed_count": processed_count,
            "error_count": error_count,
            "results_count": len(results),
            "csv_output": str(output_csv),
            "html_report": str(report_html)
        }
        
        logger.info(f"Pipeline complete: {summary}")
        return summary


def run_pipeline(dataset_path: Path, output_csv: Path, report_html: Path) -> Dict[str, Any]:
    """Main entry point for pipeline execution"""
    pipeline = CompliancePipeline()
    return pipeline.run_pipeline(dataset_path, output_csv, report_html)
