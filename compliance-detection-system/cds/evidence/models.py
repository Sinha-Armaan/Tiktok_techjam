"""
Evidence Package Data Models

This module defines the Pydantic models for evidence collection and normalization
across static analysis, runtime probes, and final compliance records.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path


class StaticSignal(BaseModel):
    """Individual static analysis signal"""
    file: str
    line: int
    message: Optional[str] = None


class GeoSignal(StaticSignal):
    """Geographic branching signal"""
    countries: List[str]


class AgeCheckSignal(StaticSignal):
    """Age verification signal"""
    lib: str
    method: Optional[str] = None


class DataResidencySignal(StaticSignal):
    """Data residency region signal"""
    region: str
    service: Optional[str] = None


class FlagSignal(BaseModel):
    """Feature flag signal"""
    name: str
    file: Optional[str] = None
    line: Optional[int] = None


class StaticSignals(BaseModel):
    """Collection of static analysis signals"""
    geo_branching: List[GeoSignal] = Field(default_factory=list)
    age_checks: List[AgeCheckSignal] = Field(default_factory=list)
    data_residency: List[DataResidencySignal] = Field(default_factory=list)
    reporting_clients: List[str] = Field(default_factory=list)
    reco_system: bool = False
    pf_controls: bool = False
    flags: List[FlagSignal] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Persona(BaseModel):
    """Test persona for runtime probing"""
    country: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    age: int = Field(..., ge=0, le=150, description="Age in years")
    region: Optional[str] = None
    language: Optional[str] = None


class FlagResolution(BaseModel):
    """Runtime feature flag resolution"""
    name: str
    value: Union[bool, str, int, float]
    source: Optional[str] = None


class NetworkTrace(BaseModel):
    """Network request trace"""
    host: str
    region_hint: Optional[str] = None
    method: str = "GET"
    path: Optional[str] = None


class RuntimeSignals(BaseModel):
    """Collection of runtime probe signals"""
    persona: Optional[Persona] = None
    blocked_actions: List[str] = Field(default_factory=list)
    ui_states: List[str] = Field(default_factory=list)
    flag_resolutions: List[FlagResolution] = Field(default_factory=list)
    network: List[NetworkTrace] = Field(default_factory=list)
    trace_uri: Optional[str] = None


class EvidenceAttachment(BaseModel):
    """File attachment for evidence"""
    type: str = Field(..., description="Attachment type: code|config|trace")
    uri: str = Field(..., description="File path or URI")
    description: Optional[str] = None


class EvidenceMetadata(BaseModel):
    """Evidence collection metadata"""
    repo: Optional[str] = None
    commit: Optional[str] = None
    branch: Optional[str] = None
    scan_timestamp: datetime = Field(default_factory=datetime.utcnow)
    scanner_version: Optional[str] = None


class EvidencePack(BaseModel):
    """Complete evidence package for a feature"""
    feature_id: str = Field(..., description="Unique feature identifier")
    signals: Dict[str, Any] = Field(default_factory=dict)
    attachments: List[EvidenceAttachment] = Field(default_factory=list)
    metadata: EvidenceMetadata = Field(default_factory=EvidenceMetadata)
    
    @property
    def static(self) -> StaticSignals:
        """Get static signals with validation"""
        static_data = self.signals.get("static", {})
        return StaticSignals.model_validate(static_data)
    
    @property 
    def runtime(self) -> RuntimeSignals:
        """Get runtime signals with validation"""
        runtime_data = self.signals.get("runtime", {})
        return RuntimeSignals.model_validate(runtime_data)

    def add_static_signals(self, signals: StaticSignals) -> None:
        """Add static analysis signals"""
        self.signals["static"] = signals.model_dump()
    
    def add_runtime_signals(self, signals: RuntimeSignals) -> None:
        """Add runtime probe signals"""
        self.signals["runtime"] = signals.model_dump()
    
    def add_attachment(self, attachment_type: str, uri: str, description: Optional[str] = None) -> None:
        """Add evidence attachment"""
        self.attachments.append(EvidenceAttachment(
            type=attachment_type,
            uri=uri,
            description=description
        ))


class RulesResult(BaseModel):
    """Result from rules engine evaluation"""
    feature_id: str
    requires_geo_logic: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    matched_rules: List[str] = Field(default_factory=list)
    missing_controls: List[str] = Field(default_factory=list)
    evaluation_timestamp: datetime = Field(default_factory=datetime.utcnow)


class FinalRecord(BaseModel):
    """Final compliance analysis record"""
    feature_id: str
    requires_geo_logic: bool
    reasoning: str
    related_regulations: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    matched_rules: List[str] = Field(default_factory=list)
    missing_controls: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    code_refs: List[str] = Field(default_factory=list)
    runtime_observation: str = ""
    needs_review: bool = False
    severity: str = Field(default="medium", pattern=r"^(low|medium|high|critical)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComplianceRule(BaseModel):
    """Individual compliance rule definition"""
    id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Human-readable rule name")
    logic: Dict[str, Any] = Field(..., description="JSON Logic rule")
    requires_controls: List[str] = Field(default_factory=list)
    regulations: List[str] = Field(default_factory=list)
    severity: str = Field(default="medium")
    description: Optional[str] = None
    enabled: bool = True


class PolicySnippet(BaseModel):
    """Regulatory policy text snippet"""
    regulation_id: str
    title: str
    content: str
    source_url: Optional[str] = None
    effective_date: Optional[datetime] = None
    jurisdiction: Optional[str] = None
