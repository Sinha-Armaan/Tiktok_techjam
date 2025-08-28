"""
Compliance Rules Engine

This module implements the json-logic based rules engine for evaluating
compliance requirements against collected evidence.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

try:
    from json_logic import jsonLogic
except ImportError:
    # Fallback implementation for MVP
    def jsonLogic(rule, data):
        """Simplified JSON Logic implementation for MVP"""
        if isinstance(rule, dict):
            if "and" in rule:
                return all(jsonLogic(sub_rule, data) for sub_rule in rule["and"])
            elif "or" in rule:
                return any(jsonLogic(sub_rule, data) for sub_rule in rule["or"])
            elif "==" in rule:
                left, right = rule["=="]
                return jsonLogic(left, data) == jsonLogic(right, data)
            elif "<" in rule:
                left, right = rule["<"]
                return jsonLogic(left, data) < jsonLogic(right, data)
            elif "in" in rule:
                item, array = rule["in"]
                return jsonLogic(item, data) in jsonLogic(array, data)
            elif "var" in rule:
                path = rule["var"]
                return _get_nested_value(data, path)
        return rule
    
    def _get_nested_value(data, path):
        """Get nested value from data using dot notation"""
        if not isinstance(path, str):
            return path
        
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                if '*' in key:
                    # Handle wildcard for list access
                    base_key = key.replace('.*', '')
                    if base_key in value and isinstance(value[base_key], list):
                        return [item for item in value[base_key] if isinstance(item, dict)]
                value = value.get(key, None)
            elif isinstance(value, list) and key.isdigit():
                idx = int(key)
                value = value[idx] if idx < len(value) else None
            else:
                return None
        return value

from ..evidence.models import EvidencePack, RulesResult, ComplianceRule

logger = logging.getLogger(__name__)


class ComplianceRulesEngine:
    """JSON-Logic based compliance rules engine"""
    
    def __init__(self, rules_path: Optional[Path] = None):
        self.rules_path = rules_path or Path(__file__).parent.parent.parent / "data" / "rules"
        self.rules: Dict[str, ComplianceRule] = {}
        self.load_rules()
    
    def load_rules(self) -> None:
        """Load compliance rules from configuration files"""
        try:
            # Load JSON Logic rules
            rules_file = self.rules_path / "compliance_rules.json"
            if rules_file.exists():
                with open(rules_file, 'r') as f:
                    rules_data = json.load(f)
                    
                for rule_data in rules_data.get("rules", []):
                    rule = ComplianceRule.model_validate(rule_data)
                    self.rules[rule.id] = rule
            else:
                # Create default rules if file doesn't exist
                self._create_default_rules()
                
        except Exception as e:
            logger.error(f"Failed to load rules: {e}")
            self._create_default_rules()
    
    def _create_default_rules(self) -> None:
        """Create default compliance rules"""
        default_rules = [
            ComplianceRule(
                id="UT_MINORS_CURFEW",
                name="Utah Minors Curfew Enforcement",
                logic={
                    "and": [
                        {"<": [{"var": "runtime.persona.age"}, 18]},
                        {"==": [{"var": "runtime.persona.country"}, "US"]},
                        {"in": ["UT", {"var": "static.geo_branching.*.countries"}]}
                    ]
                },
                requires_controls=["curfew_enforcement", "age_verification"],
                regulations=["Utah Social Media Regulation Act"],
                severity="high"
            ),
            ComplianceRule(
                id="NCMEC_REPORTING",
                name="NCMEC Mandatory Reporting",
                logic={
                    "or": [
                        {"in": ["NCMEC", {"var": "static.reporting_clients"}]},
                        {"in": ["csam_detection", {"var": "static.tags"}]},
                        {"==": [{"var": "static.reco_system"}, True]}
                    ]
                },
                requires_controls=["ncmec_report_pipeline", "content_moderation"],
                regulations=["US NCMEC reporting requirements"],
                severity="critical"
            ),
            ComplianceRule(
                id="DSA_TRANSPARENCY",
                name="EU Digital Services Act Transparency",
                logic={
                    "and": [
                        {"==": [{"var": "runtime.persona.country"}, "EU"]},
                        {"or": [
                            {"==": [{"var": "static.reco_system"}, True]},
                            {"in": ["content_moderation", {"var": "static.tags"}]}
                        ]}
                    ]
                },
                requires_controls=["transparency_reports", "user_flagging", "appeal_process"],
                regulations=["EU Digital Services Act"],
                severity="high"
            ),
            ComplianceRule(
                id="STATE_MINORS_PF_DEFAULT_OFF",
                name="State Minors Parental Features Default Off",
                logic={
                    "and": [
                        {"<": [{"var": "runtime.persona.age"}, 18]},
                        {"==": [{"var": "static.pf_controls"}, True]},
                        {"in": ["US", {"var": "static.geo_branching.*.countries"}]}
                    ]
                },
                requires_controls=["parental_consent", "default_privacy_settings"],
                regulations=["Various US state minors privacy laws"],
                severity="medium"
            ),
            ComplianceRule(
                id="GDPR_DATA_PROCESSING",
                name="GDPR Lawful Basis for Processing",
                logic={
                    "and": [
                        {"in": [{"var": "runtime.persona.country"}, ["EU", "GB", "CH"]]},
                        {"or": [
                            {"in": ["user_data", {"var": "static.tags"}]},
                            {"in": ["eu-west", {"var": "static.data_residency.*.region"}]}
                        ]}
                    ]
                },
                requires_controls=["consent_management", "data_portability", "right_to_erasure"],
                regulations=["EU GDPR"],
                severity="high"
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.id] = rule
        
        # Save default rules to file
        self._save_rules()
    
    def _save_rules(self) -> None:
        """Save rules to configuration file"""
        try:
            rules_file = self.rules_path / "compliance_rules.json"
            rules_file.parent.mkdir(parents=True, exist_ok=True)
            
            rules_data = {
                "version": "1.0",
                "rules": [rule.model_dump() for rule in self.rules.values()]
            }
            
            with open(rules_file, 'w') as f:
                json.dump(rules_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save rules: {e}")
    
    def evaluate(self, evidence: EvidencePack) -> RulesResult:
        """Evaluate evidence against compliance rules"""
        logger.info(f"Evaluating {len(self.rules)} rules against evidence for {evidence.feature_id}")
        
        # Prepare data for JSON Logic evaluation
        data = self._prepare_evaluation_data(evidence)
        
        matched_rules = []
        missing_controls = set()
        total_confidence = 0.0
        
        for rule_id, rule in self.rules.items():
            if not rule.enabled:
                continue
                
            try:
                # Evaluate JSON Logic rule
                result = jsonLogic(rule.logic, data)
                
                if result:
                    logger.debug(f"Rule {rule_id} matched")
                    matched_rules.append(rule_id)
                    missing_controls.update(rule.requires_controls)
                    
                    # Add confidence based on rule severity
                    severity_weights = {"low": 0.1, "medium": 0.3, "high": 0.5, "critical": 0.7}
                    total_confidence += severity_weights.get(rule.severity, 0.3)
                
            except Exception as e:
                logger.warning(f"Failed to evaluate rule {rule_id}: {e}")
        
        # Calculate final confidence score
        confidence = min(total_confidence / len(self.rules) if self.rules else 0.0, 1.0)
        
        # Determine if geo logic is required
        requires_geo_logic = len(matched_rules) > 0
        
        # Filter missing controls to only those that aren't already implemented
        # (This would require additional evidence about existing controls)
        missing_controls_list = list(missing_controls)
        
        return RulesResult(
            feature_id=evidence.feature_id,
            requires_geo_logic=requires_geo_logic,
            confidence=confidence,
            matched_rules=matched_rules,
            missing_controls=missing_controls_list
        )
    
    def _prepare_evaluation_data(self, evidence: EvidencePack) -> Dict[str, Any]:
        """Prepare evidence data for JSON Logic evaluation"""
        # Convert evidence to flat structure for JSON Logic
        data = {
            "static": evidence.signals.get("static", {}),
            "runtime": evidence.signals.get("runtime", {}),
            "metadata": evidence.metadata.model_dump()
        }
        
        # Add default runtime persona if missing
        if "runtime" not in data or not data["runtime"].get("persona"):
            data["runtime"]["persona"] = {
                "age": None,
                "country": "Unknown",
                "region": None
            }
        
        # Flatten complex structures for easier JSON Logic access
        static = data.get("static", {})
        
        # Convert geo_branching list to countries list
        if "geo_branching" in static:
            all_countries = []
            for geo_signal in static["geo_branching"]:
                if isinstance(geo_signal, dict) and "countries" in geo_signal:
                    all_countries.extend(geo_signal["countries"])
            data["static"]["all_countries"] = list(set(all_countries))
        else:
            data["static"]["all_countries"] = []
        
        # Convert data_residency to regions list
        if "data_residency" in static:
            all_regions = []
            for residency_signal in static["data_residency"]:
                if isinstance(residency_signal, dict) and "region" in residency_signal:
                    all_regions.append(residency_signal["region"])
            data["static"]["all_regions"] = list(set(all_regions))
        else:
            data["static"]["all_regions"] = []
        
        return data
    
    def get_rule(self, rule_id: str) -> Optional[ComplianceRule]:
        """Get specific rule by ID"""
        return self.rules.get(rule_id)
    
    def list_rules(self) -> List[ComplianceRule]:
        """Get all loaded rules"""
        return list(self.rules.values())


def evaluate_feature(feature_id: str, evidence_file: Optional[Path] = None) -> Dict[str, Any]:
    """Main entry point for feature evaluation"""
    # Load evidence
    if evidence_file is None:
        evidence_file = Path("./artifacts/evidence") / f"{feature_id}.json"
    
    if not evidence_file.exists():
        raise FileNotFoundError(f"Evidence file not found: {evidence_file}")
    
    with open(evidence_file, 'r') as f:
        evidence_data = json.load(f)
    
    evidence = EvidencePack.model_validate(evidence_data)
    
    # Evaluate with rules engine
    engine = ComplianceRulesEngine()
    result = engine.evaluate(evidence)
    
    # Save results
    results_file = evidence_file.parent / f"{feature_id}_rules_result.json"
    with open(results_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2, default=str)
    
    return result.model_dump()
