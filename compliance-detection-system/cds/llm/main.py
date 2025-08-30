"""
LLM Integration Module

This module provides Gemini 1.5 Pro integration for compliance analysis
and explanation generation.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google AI imports with fallbacks
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

try:
    from google.cloud import aiplatform
    from vertexai.preview.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

from ..evidence.models import EvidencePack, RulesResult, FinalRecord, PolicySnippet

logger = logging.getLogger(__name__)


class PolicySnippetManager:
    """Manages regulatory policy snippets for LLM context"""
    
    def __init__(self, snippets_path: Optional[Path] = None):
        self.snippets_path = snippets_path or Path(__file__).parent.parent.parent / "data" / "policy_snippets.json"
        self.snippets: Dict[str, PolicySnippet] = {}
        self.load_snippets()
    
    def load_snippets(self) -> None:
        """Load policy snippets from configuration"""
        try:
            if self.snippets_path.exists():
                with open(self.snippets_path, 'r') as f:
                    snippets_data = json.load(f)
                    
                # Handle both list format and dict format
                if isinstance(snippets_data, list):
                    # Direct list of snippets
                    for snippet_data in snippets_data:
                        snippet = PolicySnippet.model_validate(snippet_data)
                        self.snippets[snippet.regulation_id] = snippet
                elif isinstance(snippets_data, dict) and "snippets" in snippets_data:
                    # Dict with snippets key
                    for snippet_data in snippets_data["snippets"]:
                        snippet = PolicySnippet.model_validate(snippet_data)
                        self.snippets[snippet.regulation_id] = snippet
                else:
                    # Treat as dict of snippets
                    for snippet_data in snippets_data.values():
                        snippet = PolicySnippet.model_validate(snippet_data)
                        self.snippets[snippet.regulation_id] = snippet
            else:
                self._create_default_snippets()
                
        except Exception as e:
            logger.error(f"Failed to load policy snippets: {e}")
            self._create_default_snippets()
    
    def _create_default_snippets(self) -> None:
        """Create default policy snippets"""
        default_snippets = [
            PolicySnippet(
                regulation_id="utah_social_media_act",
                title="Utah Social Media Regulation Act - Minor Protections",
                content="Social media companies must implement curfew restrictions for users under 18 in Utah, blocking access between 10:30 PM and 6:30 AM unless parental consent is provided.",
                source_url="https://le.utah.gov/~2023/bills/static/SB0152.html",
                jurisdiction="Utah, USA"
            ),
            PolicySnippet(
                regulation_id="ncmec_reporting",
                title="NCMEC Mandatory Reporting Requirements",
                content="Electronic service providers must report known instances of child sexual abuse material (CSAM) to the National Center for Missing & Exploited Children within a reasonable time.",
                source_url="https://www.missingkids.org/gethelpnow/cybertipline",
                jurisdiction="United States"
            ),
            PolicySnippet(
                regulation_id="eu_dsa",
                title="EU Digital Services Act - Transparency Obligations",
                content="Very large online platforms must provide transparency reports, implement user flagging mechanisms, and establish appeal processes for content moderation decisions.",
                source_url="https://digital-strategy.ec.europa.eu/en/policies/digital-services-act-package",
                jurisdiction="European Union"
            ),
            PolicySnippet(
                regulation_id="gdpr",
                title="GDPR - Lawful Basis for Processing",
                content="Processing personal data requires a lawful basis under Article 6. Data subjects have rights to access, portability, erasure, and objection to processing.",
                source_url="https://gdpr.eu/article-6-how-to-process-personal-data-legally/",
                jurisdiction="European Union"
            ),
            PolicySnippet(
                regulation_id="coppa",
                title="COPPA - Children's Online Privacy Protection",
                content="Websites directed to children under 13 must obtain verifiable parental consent before collecting personal information from children.",
                source_url="https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/childrens-online-privacy-protection-rule",
                jurisdiction="United States"
            )
        ]
        
        for snippet in default_snippets:
            self.snippets[snippet.regulation_id] = snippet
        
        self._save_snippets()
    
    def _save_snippets(self) -> None:
        """Save snippets to configuration file"""
        try:
            self.snippets_path.parent.mkdir(parents=True, exist_ok=True)
            snippets_data = {
                "version": "1.0",
                "snippets": [snippet.model_dump() for snippet in self.snippets.values()]
            }
            
            with open(self.snippets_path, 'w') as f:
                json.dump(snippets_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save policy snippets: {e}")
    
    def get_relevant_snippets(self, regulations: List[str]) -> List[PolicySnippet]:
        """Get policy snippets for specified regulations"""
        relevant_snippets = []
        
        for regulation in regulations:
            # Direct match
            if regulation.lower() in self.snippets:
                relevant_snippets.append(self.snippets[regulation.lower()])
                continue
            
            # Fuzzy matching
            for snippet_id, snippet in self.snippets.items():
                if any(reg_word in snippet.title.lower() for reg_word in regulation.lower().split()):
                    relevant_snippets.append(snippet)
                    break
        
        return relevant_snippets


class GeminiClient:
    """Gemini client supporting both Google AI Studio and Vertex AI"""
    
    def __init__(self):
        # Google AI Studio configuration (preferred)
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        # Vertex AI configuration (fallback)
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GEMINI_LOCATION", "us-central1")
        
        # Model configuration
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
        
        # Determine which API to use
        self.use_google_ai = self.api_key and GOOGLE_AI_AVAILABLE
        self.use_vertex_ai = self.project_id and VERTEX_AI_AVAILABLE
        
        if self.use_google_ai:
            genai.configure(api_key=self.api_key)
            logger.info(f"Using Google AI Studio API with model: {self.model_name}")
        elif self.use_vertex_ai:
            logger.info(f"Using Vertex AI with project: {self.project_id}")
        else:
            logger.warning("Neither Google AI Studio API key nor Vertex AI project configured - using mock implementation")
    
    def analyze_compliance(self, evidence: EvidencePack, rules_result: RulesResult, 
                          policy_snippets: List[PolicySnippet]) -> FinalRecord:
        """Analyze compliance evidence and generate final record"""
        
        if self.use_google_ai:
            return self._analyze_with_google_ai(evidence, rules_result, policy_snippets)
        elif self.use_vertex_ai:
            return self._analyze_with_vertex_ai(evidence, rules_result, policy_snippets)
        else:
            return self._mock_analysis(evidence, rules_result, policy_snippets)
    
    def _analyze_with_google_ai(self, evidence: EvidencePack, rules_result: RulesResult, 
                               policy_snippets: List[PolicySnippet]) -> FinalRecord:
        """Analyze using Google AI Studio API"""
        try:
            # Initialize the model
            model = genai.GenerativeModel(self.model_name)
            
            # Prepare prompt
            prompt = self._build_analysis_prompt(evidence, rules_result, policy_snippets)
            
            # Configure generation
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=2048,
                candidate_count=1
            )
            
            # Generate response
            response = model.generate_content(prompt, generation_config=generation_config)
            
            # Parse response
            response_text = response.text.strip()
            
            # Handle markdown code blocks
            if response_text.startswith('```json') and response_text.endswith('```'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```') and response_text.endswith('```'):
                response_text = response_text[3:-3].strip()
            
            try:
                result_data = json.loads(response_text)
                return self._create_final_record(evidence.feature_id, result_data, rules_result)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Gemini response as JSON. Response was: {response.text[:500]}...")
                return self._create_fallback_record(evidence, rules_result)
                
        except Exception as e:
            logger.error(f"Google AI Studio analysis failed: {e}")
            return self._create_fallback_record(evidence, rules_result)
    
    def _analyze_with_vertex_ai(self, evidence: EvidencePack, rules_result: RulesResult, 
                               policy_snippets: List[PolicySnippet]) -> FinalRecord:
        """Analyze using Vertex AI"""
        try:
            # Initialize Vertex AI
            aiplatform.init(project=self.project_id, location=self.location)
            model = GenerativeModel(self.model_name)
            
            # Prepare prompt
            prompt = self._build_analysis_prompt(evidence, rules_result, policy_snippets)
            
            # Generate response
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": 2048,
                    "candidate_count": 1
                }
            )
            
            # Parse response
            response_text = response.text.strip()
            
            # Handle markdown code blocks
            if response_text.startswith('```json') and response_text.endswith('```'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```') and response_text.endswith('```'):
                response_text = response_text[3:-3].strip()
            
            try:
                result_data = json.loads(response_text)
                return self._create_final_record(evidence.feature_id, result_data, rules_result)
            except json.JSONDecodeError:
                logger.error("Failed to parse Gemini response as JSON")
                return self._create_fallback_record(evidence, rules_result)
                
        except Exception as e:
            logger.error(f"Vertex AI analysis failed: {e}")
            return self._create_fallback_record(evidence, rules_result)
    
    def _build_analysis_prompt(self, evidence: EvidencePack, rules_result: RulesResult, 
                              policy_snippets: List[PolicySnippet]) -> str:
        """Build comprehensive analysis prompt for Gemini"""
        
        # Prepare evidence summary
        static_signals = evidence.static
        runtime_signals = evidence.runtime
        
        prompt = f"""You are LexLLM, a compliance analysis assistant. Analyze the provided evidence and rules to determine if a feature requires geo-specific compliance logic.

Base your response ONLY on the evidence provided. Include specific file:line references in your reasoning.

**FEATURE ID:** {evidence.feature_id}

**STATIC ANALYSIS EVIDENCE:**
- Geographic Branching Signals: {len(static_signals.geo_branching)} found
"""
        
        for geo_signal in static_signals.geo_branching[:3]:  # Limit for prompt size
            prompt += f"  • File: {geo_signal.file}:{geo_signal.line} - Countries: {geo_signal.countries}\n"
        
        prompt += f"- Age Verification Signals: {len(static_signals.age_checks)} found\n"
        for age_signal in static_signals.age_checks[:3]:
            prompt += f"  • File: {age_signal.file}:{age_signal.line} - Library: {age_signal.lib}\n"
        
        prompt += f"- Data Residency Signals: {len(static_signals.data_residency)} found\n"
        for residency_signal in static_signals.data_residency[:3]:
            prompt += f"  • File: {residency_signal.file}:{residency_signal.line} - Region: {residency_signal.region}\n"
        
        prompt += f"- Reporting Clients: {static_signals.reporting_clients}\n"
        prompt += f"- Recommendation System: {static_signals.reco_system}\n"
        prompt += f"- Parental Controls: {static_signals.pf_controls}\n"
        
        if runtime_signals.persona:
            prompt += f"\n**RUNTIME EVIDENCE:**\n"
            prompt += f"- Test Persona: {runtime_signals.persona.country}, age {runtime_signals.persona.age}\n"
            prompt += f"- Blocked Actions: {runtime_signals.blocked_actions}\n"
            prompt += f"- UI States: {runtime_signals.ui_states}\n"
            prompt += f"- Feature Flags: {len(runtime_signals.flag_resolutions)} resolved\n"
        
        prompt += f"\n**RULES ENGINE RESULTS:**\n"
        prompt += f"- Requires Geo Logic: {rules_result.requires_geo_logic}\n"
        prompt += f"- Confidence Score: {rules_result.confidence:.2f}\n"
        prompt += f"- Matched Rules: {rules_result.matched_rules}\n"
        prompt += f"- Missing Controls: {rules_result.missing_controls}\n"
        
        if policy_snippets:
            prompt += f"\n**RELEVANT REGULATIONS:**\n"
            for snippet in policy_snippets[:3]:  # Limit for prompt size
                prompt += f"- {snippet.title}: {snippet.content[:200]}...\n"
        
        prompt += """
**INSTRUCTIONS:**
Analyze this evidence and provide your assessment in the following JSON format:

{
  "requires_geo_logic": boolean,
  "reasoning": "Detailed explanation based on the evidence, including specific file:line references where applicable",
  "related_regulations": ["list", "of", "applicable", "regulations"],
  "confidence": number between 0.0 and 1.0,
  "missing_controls": ["list", "of", "missing", "compliance", "controls"],
  "evidence_refs": ["list", "of", "evidence", "references"],
  "code_refs": ["file:line", "references", "from", "evidence"],
  "runtime_observation": "summary of runtime behavior observations",
  "needs_review": boolean,
  "severity": "low|medium|high|critical"
}

**CONFIDENCE SCORING GUIDELINES:**
- 0.9-1.0: Clear evidence of geo-specific compliance requirements (explicit legal references, multiple compliance signals)
- 0.7-0.89: Strong indicators but some ambiguity (regional variations with unclear legal basis)
- 0.4-0.69: GRAY AREA - Mixed signals, unclear intent, needs human review (e.g., "available globally except KR", vague regional restrictions)
- 0.2-0.39: Weak indicators, likely business-driven rather than legal
- 0.0-0.19: No evidence of geo-specific compliance requirements

**GRAY AREA EXAMPLES REQUIRING HUMAN REVIEW (0.4-0.69 confidence):**
- Regional restrictions without clear legal justification ("except certain regions")
- Age-related controls with unclear regulatory basis
- Data handling variations that might be business policy vs legal compliance
- Geographic content blocking without explicit compliance reasoning
- Implementation that partially addresses regulations but may be insufficient

Focus on:
1. Geographic variations in compliance requirements
2. Age-related restrictions and protections  
3. Data residency and cross-border data transfer implications
4. Mandatory reporting obligations
5. Transparency and user control requirements

Provide specific, evidence-based reasoning. Flag uncertainty when evidence is ambiguous about whether geographic variations are legally required vs business-driven.
"""
        
        return prompt
    
    def _create_final_record(self, feature_id: str, llm_data: Dict[str, Any], 
                           rules_result: RulesResult) -> FinalRecord:
        """Create final record from LLM response"""
        return FinalRecord(
            feature_id=feature_id,
            requires_geo_logic=llm_data.get("requires_geo_logic", rules_result.requires_geo_logic),
            reasoning=llm_data.get("reasoning", "Analysis completed"),
            related_regulations=llm_data.get("related_regulations", []),
            confidence=llm_data.get("confidence", rules_result.confidence),
            matched_rules=rules_result.matched_rules,
            missing_controls=llm_data.get("missing_controls", rules_result.missing_controls),
            evidence_refs=llm_data.get("evidence_refs", []),
            code_refs=llm_data.get("code_refs", []),
            runtime_observation=llm_data.get("runtime_observation", ""),
            needs_review=llm_data.get("needs_review", False),
            severity=llm_data.get("severity", "medium")
        )
    
    def _create_fallback_record(self, evidence: EvidencePack, rules_result: RulesResult) -> FinalRecord:
        """Create fallback record when LLM analysis fails"""
        return FinalRecord(
            feature_id=evidence.feature_id,
            requires_geo_logic=rules_result.requires_geo_logic,
            reasoning="Analysis completed using fallback logic due to LLM unavailability",
            confidence=rules_result.confidence,
            matched_rules=rules_result.matched_rules,
            missing_controls=rules_result.missing_controls,
            needs_review=True,
            severity="medium"
        )
    
    def _mock_analysis(self, evidence: EvidencePack, rules_result: RulesResult, 
                      policy_snippets: List[PolicySnippet]) -> FinalRecord:
        """Mock analysis when Gemini is not available"""
        logger.info("Using mock LLM analysis - Vertex AI not available")
        
        # Generate mock reasoning based on evidence
        reasoning_parts = []
        
        static_signals = evidence.static
        if static_signals.geo_branching:
            reasoning_parts.append(f"Geographic branching detected in {len(static_signals.geo_branching)} locations with countries: {', '.join([', '.join(sig.countries) for sig in static_signals.geo_branching])}")
        
        if static_signals.age_checks:
            reasoning_parts.append(f"Age verification systems found using {', '.join(set([sig.lib for sig in static_signals.age_checks]))}")
        
        if static_signals.data_residency:
            regions = [sig.region for sig in static_signals.data_residency]
            reasoning_parts.append(f"Data residency patterns detected for regions: {', '.join(regions)}")
        
        if rules_result.matched_rules:
            reasoning_parts.append(f"Compliance rules triggered: {', '.join(rules_result.matched_rules)}")
        
        reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Limited compliance indicators found in evidence"
        
        # Determine related regulations
        related_regulations = []
        for snippet in policy_snippets:
            related_regulations.append(snippet.title)
        
        # Extract code references
        code_refs = []
        for sig in static_signals.geo_branching + static_signals.age_checks + static_signals.data_residency:
            code_refs.append(f"{sig.file}:{sig.line}")
        
        return FinalRecord(
            feature_id=evidence.feature_id,
            requires_geo_logic=rules_result.requires_geo_logic,
            reasoning=reasoning,
            related_regulations=related_regulations[:5],  # Limit to 5
            confidence=rules_result.confidence,
            matched_rules=rules_result.matched_rules,
            missing_controls=rules_result.missing_controls,
            evidence_refs=[f"evidence/{evidence.feature_id}.json"],
            code_refs=code_refs[:10],  # Limit to 10
            runtime_observation="Mock runtime analysis completed" if evidence.signals.get("runtime") else "",
            needs_review=rules_result.confidence < 0.7,
            severity="high" if rules_result.requires_geo_logic else "medium"
        )


class LLMAnalysisEngine:
    """Main LLM analysis engine"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.policy_manager = PolicySnippetManager()
    
    def explain_feature(self, feature_id: str, evidence_file: Optional[Path] = None, 
                       rules_file: Optional[Path] = None) -> FinalRecord:
        """Generate LLM explanation for feature compliance"""
        logger.info(f"Generating explanation for feature: {feature_id}")
        
        # Load evidence
        if evidence_file is None:
            evidence_file = Path("./artifacts/evidence") / f"{feature_id}.json"
        
        if not evidence_file.exists():
            raise FileNotFoundError(f"Evidence file not found: {evidence_file}")
        
        with open(evidence_file, 'r') as f:
            evidence_data = json.load(f)
        evidence = EvidencePack.model_validate(evidence_data)
        
        # Load rules result
        if rules_file is None:
            rules_file = evidence_file.parent / f"{feature_id}_rules_result.json"
        
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules result file not found: {rules_file}")
        
        with open(rules_file, 'r') as f:
            rules_data = json.load(f)
        rules_result = RulesResult.model_validate(rules_data)
        
        # Get relevant policy snippets
        all_regulations = rules_result.matched_rules + [
            snippet.regulation_id for snippet in self.policy_manager.snippets.values() 
            if any(rule in snippet.regulation_id.lower() for rule in rules_result.matched_rules)
        ]
        policy_snippets = self.policy_manager.get_relevant_snippets(all_regulations)
        
        # Generate LLM analysis
        final_record = self.gemini_client.analyze_compliance(evidence, rules_result, policy_snippets)
        
        return final_record


def explain_feature(feature_id: str, evidence_file: Optional[Path] = None) -> Dict[str, Any]:
    """Main entry point for LLM-powered explanation"""
    engine = LLMAnalysisEngine()
    final_record = engine.explain_feature(feature_id, evidence_file)
    
    # Save final record
    output_file = Path("./artifacts/evidence") / f"{feature_id}_final_record.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(final_record.model_dump(), f, indent=2, default=str)
    
    return final_record.model_dump()
