"""
Static Analysis Scanner

This module provides static code analysis capabilities using semgrep and tree-sitter
to detect compliance-related patterns in source code.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from ..evidence.models import (
    EvidencePack, StaticSignals, GeoSignal, AgeCheckSignal, 
    DataResidencySignal, FlagSignal, EvidenceMetadata
)

logger = logging.getLogger(__name__)


class SemgrepScanner:
    """Semgrep-based pattern scanner for compliance signals"""
    
    def __init__(self, rules_path: Optional[Path] = None):
        self.rules_path = rules_path or Path(__file__).parent.parent.parent / "data" / "rules" / "semgrep.yml"
    
    def scan(self, repo_path: Path) -> Dict[str, List[Dict]]:
        """Run semgrep scan on repository"""
        try:
            cmd = [
                "semgrep",
                "--config", str(self.rules_path),
                "--json",
                "--no-git-ignore",
                str(repo_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            # Check for actual failures (non-zero exit code with no stdout)
            if result.returncode != 0 and not result.stdout:
                logger.error(f"Semgrep scan failed: {result.stderr}")
                return {}
            
            # Log warnings but don't fail (semgrep often outputs warnings to stderr)
            if result.stderr and result.stderr.strip():
                logger.warning(f"Semgrep warnings: {result.stderr}")
            
            data = json.loads(result.stdout)
            
            # Group findings by rule ID
            findings = {}
            for finding in data.get("results", []):
                rule_id = finding.get("check_id", "unknown")
                if rule_id not in findings:
                    findings[rule_id] = []
                findings[rule_id].append({
                    "file": finding.get("path", ""),
                    "line": finding.get("start", {}).get("line", 0),
                    "message": finding.get("extra", {}).get("message", ""),
                    "code": finding.get("extra", {}).get("lines", "").strip()
                })
            
            return findings
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Semgrep scan failed: {e.stderr}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse semgrep output: {e}")
            return {}


class TreeSitterScanner:
    """Tree-sitter AST scanner for advanced pattern matching"""
    
    def __init__(self):
        # Tree-sitter setup would go here
        # For MVP, we'll use simple regex patterns
        pass
    
    def scan(self, repo_path: Path) -> Dict[str, List[Dict]]:
        """Scan for AST patterns (stubbed for MVP)"""
        # For MVP, return empty results
        # In full implementation, would use tree-sitter to parse AST
        return {}


class StaticAnalysisEngine:
    """Main static analysis engine combining multiple scanners"""
    
    def __init__(self):
        self.semgrep = SemgrepScanner()
        self.treesitter = TreeSitterScanner()
    
    def scan_repository(self, repo_path: Path, feature_id: str) -> EvidencePack:
        """Perform comprehensive static analysis scan"""
        logger.info(f"Starting static scan of {repo_path} for feature {feature_id}")
        
        # Run scanners
        semgrep_findings = self.semgrep.scan(repo_path)
        treesitter_findings = self.treesitter.scan(repo_path)
        
        # Convert findings to structured signals
        signals = self._convert_findings_to_signals(semgrep_findings, treesitter_findings)
        
        # Create evidence pack
        evidence = EvidencePack(
            feature_id=feature_id,
            metadata=EvidenceMetadata(repo=str(repo_path))
        )
        evidence.add_static_signals(signals)
        
        # Add code attachments
        self._add_code_attachments(evidence, semgrep_findings, repo_path)
        
        logger.info(f"Static scan complete: {len(signals.geo_branching)} geo signals, "
                   f"{len(signals.age_checks)} age signals, "
                   f"{len(signals.data_residency)} residency signals")
        
        return evidence
    
    def _convert_findings_to_signals(self, semgrep: Dict, treesitter: Dict) -> StaticSignals:
        """Convert raw scanner findings to structured signals"""
        signals = StaticSignals()
        
        # Process semgrep findings
        for rule_id, findings in semgrep.items():
            if "geo-country-lists" in rule_id:
                for finding in findings:
                    # Extract country codes from the code
                    countries = self._extract_countries_from_code(finding.get("code", ""))
                    signals.geo_branching.append(GeoSignal(
                        file=finding["file"],
                        line=finding["line"],
                        countries=countries,
                        message=finding["message"]
                    ))
            
            elif "age-verification" in rule_id:
                for finding in findings:
                    lib = self._extract_library_name(finding.get("code", ""))
                    signals.age_checks.append(AgeCheckSignal(
                        file=finding["file"],
                        line=finding["line"],
                        lib=lib,
                        message=finding["message"]
                    ))
            
            elif "data-residency" in rule_id:
                for finding in findings:
                    region = self._extract_region_from_code(finding.get("code", ""))
                    signals.data_residency.append(DataResidencySignal(
                        file=finding["file"],
                        line=finding["line"],
                        region=region,
                        message=finding["message"]
                    ))
            
            elif "ncmec-reporting" in rule_id:
                for finding in findings:
                    signals.reporting_clients.append("NCMEC")
            
            elif "parental-controls" in rule_id:
                signals.pf_controls = True
            
            elif "compliance-flags" in rule_id:
                for finding in findings:
                    flag_name = self._extract_flag_name(finding.get("code", ""))
                    signals.flags.append(FlagSignal(
                        name=flag_name,
                        file=finding["file"],
                        line=finding["line"]
                    ))
        
        return signals
    
    def _extract_countries_from_code(self, code: str) -> List[str]:
        """Extract country codes from code snippet"""
        import re
        # Simple regex to find country codes
        pattern = r'["\']([A-Z]{2})["\']'
        matches = re.findall(pattern, code)
        return list(set(matches))
    
    def _extract_library_name(self, code: str) -> str:
        """Extract library name from import statement"""
        if "age_gate" in code:
            return "age_gate"
        elif "age_verify" in code:
            return "age_verify"
        else:
            return "unknown"
    
    def _extract_region_from_code(self, code: str) -> str:
        """Extract region from code snippet"""
        if "us-east" in code.lower():
            return "us-east"
        elif "eu-west" in code.lower():
            return "eu-west"
        elif "asia-pacific" in code.lower():
            return "asia-pacific"
        else:
            return "unknown"
    
    def _extract_flag_name(self, code: str) -> str:
        """Extract feature flag name from code"""
        import re
        pattern = r'FEATURE_FLAG_(\w+)'
        match = re.search(pattern, code)
        return match.group(1) if match else "unknown"
    
    def _add_code_attachments(self, evidence: EvidencePack, findings: Dict, repo_path: Path) -> None:
        """Add relevant code files as attachments"""
        attached_files = set()
        
        for rule_findings in findings.values():
            for finding in rule_findings:
                file_path = finding.get("file", "")
                if file_path and file_path not in attached_files:
                    full_path = repo_path / file_path
                    if full_path.exists():
                        evidence.add_attachment("code", str(full_path), f"Source file with compliance signals")
                        attached_files.add(file_path)


def scan_repository(repo_path: Path, feature_id: str, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """Main entry point for static repository scanning"""
    engine = StaticAnalysisEngine()
    evidence = engine.scan_repository(repo_path, feature_id)
    
    # Save evidence to file
    if output_path is None:
        output_path = Path("./artifacts/evidence") / f"{feature_id}.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(evidence.model_dump(), f, indent=2, default=str)
    
    return evidence.model_dump()
