"""
Runtime Probes Module

This module provides Playwright-based runtime probing capabilities to capture
compliance-related behavior in live applications.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Playwright imports with fallback for MVP
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    async_playwright = None

from ..evidence.models import (
    EvidencePack, RuntimeSignals, Persona, FlagResolution, 
    NetworkTrace, EvidenceMetadata
)

logger = logging.getLogger(__name__)


class PersonaManager:
    """Manages test personas for runtime probing"""
    
    @staticmethod
    def get_persona(persona_name: str) -> Persona:
        """Get predefined persona configuration"""
        personas = {
            "ut_minor": Persona(
                country="US",
                age=16,
                region="UT",
                language="en-US"
            ),
            "fr_adult": Persona(
                country="FR", 
                age=25,
                region="EU",
                language="fr-FR"
            ),
            "ca_teen": Persona(
                country="CA",
                age=17,
                region="NA",
                language="en-CA"
            ),
            "uk_adult": Persona(
                country="GB",
                age=30,
                region="EU",
                language="en-GB"
            )
        }
        
        if persona_name not in personas:
            raise ValueError(f"Unknown persona: {persona_name}. Available: {list(personas.keys())}")
        
        return personas[persona_name]


class PlaywrightProber:
    """Playwright-based runtime compliance prober"""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright not available - using mock implementation")
    
    async def __aenter__(self):
        """Async context manager entry"""
        if PLAYWRIGHT_AVAILABLE:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.page = await self.browser.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if PLAYWRIGHT_AVAILABLE and self.browser:
            await self.browser.close()
            await self.playwright.stop()
    
    async def probe_with_persona(self, url: str, persona: Persona) -> RuntimeSignals:
        """Probe URL with specific persona and capture compliance signals"""
        logger.info(f"Probing {url} with persona: {persona.country}, age {persona.age}")
        
        if not PLAYWRIGHT_AVAILABLE:
            return self._mock_runtime_signals(persona)
        
        signals = RuntimeSignals(persona=persona)
        
        try:
            # Configure browser for persona
            await self._configure_persona(persona)
            
            # Navigate to target URL
            response = await self.page.goto(url, timeout=self.timeout)
            await self.page.wait_for_load_state('networkidle')
            
            # Capture network traces
            signals.network = await self._capture_network_traces()
            
            # Test age-related restrictions
            blocked_actions = await self._test_age_restrictions()
            signals.blocked_actions.extend(blocked_actions)
            
            # Capture UI state changes
            ui_states = await self._capture_ui_states()
            signals.ui_states.extend(ui_states)
            
            # Capture feature flag resolutions
            flag_resolutions = await self._capture_flag_resolutions()
            signals.flag_resolutions.extend(flag_resolutions)
            
            # Save trace file
            trace_path = await self._save_trace()
            signals.trace_uri = str(trace_path) if trace_path else None
            
        except Exception as e:
            logger.error(f"Runtime probing failed: {e}")
            # Add error as blocked action
            signals.blocked_actions.append(f"probe_error: {str(e)}")
        
        return signals
    
    async def _configure_persona(self, persona: Persona) -> None:
        """Configure browser for persona characteristics"""
        if not self.page:
            return
        
        # Set geolocation based on persona country
        locations = {
            "US": {"latitude": 39.8283, "longitude": -98.5795},
            "FR": {"latitude": 46.2276, "longitude": 2.2137},
            "CA": {"latitude": 56.1304, "longitude": -106.3468},
            "GB": {"latitude": 55.3781, "longitude": -3.4360}
        }
        
        location = locations.get(persona.country)
        if location:
            context = self.page.context
            await context.set_geolocation(location)
            await context.grant_permissions(['geolocation'])
        
        # Set language preferences
        if persona.language:
            await self.page.context.add_init_script(f"""
                Object.defineProperty(navigator, 'language', {{
                    get: function() {{ return '{persona.language}'; }}
                }});
            """)
        
        # Inject age information for testing
        await self.page.add_init_script(f"""
            window._test_persona = {{
                country: '{persona.country}',
                age: {persona.age},
                region: '{persona.region or ""}'
            }};
        """)
    
    async def _test_age_restrictions(self) -> List[str]:
        """Test various age-restricted actions"""
        if not self.page:
            return []
        
        blocked_actions = []
        
        # Test common age-restricted elements
        age_restricted_selectors = [
            '[data-age-restricted="true"]',
            '.age-gate',
            '#age-verification',
            '[data-requires-age-verification]',
            '.minor-restricted'
        ]
        
        for selector in age_restricted_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    is_hidden = await element.is_hidden()
                    if is_hidden:
                        blocked_actions.append(f"age_restricted_element_hidden: {selector}")
                    else:
                        # Try to interact and see if blocked
                        try:
                            await element.click(timeout=1000)
                        except Exception:
                            blocked_actions.append(f"age_restricted_click_blocked: {selector}")
            except Exception as e:
                logger.debug(f"Age restriction test failed for {selector}: {e}")
        
        return blocked_actions
    
    async def _capture_ui_states(self) -> List[str]:
        """Capture relevant UI states for compliance"""
        if not self.page:
            return []
        
        ui_states = []
        
        # Check for common compliance-related UI elements
        compliance_selectors = [
            ('.cookie-banner', 'cookie_banner_visible'),
            ('.consent-modal', 'consent_modal_visible'),
            ('.age-verification-modal', 'age_verification_modal_visible'),
            ('.parental-controls', 'parental_controls_visible'),
            ('.privacy-settings', 'privacy_settings_available'),
            ('.data-deletion', 'data_deletion_available')
        ]
        
        for selector, state_name in compliance_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element and await element.is_visible():
                    ui_states.append(state_name)
            except Exception as e:
                logger.debug(f"UI state check failed for {selector}: {e}")
        
        return ui_states
    
    async def _capture_flag_resolutions(self) -> List[FlagResolution]:
        """Capture feature flag resolutions"""
        if not self.page:
            return []
        
        flag_resolutions = []
        
        try:
            # Extract feature flags from window object
            flags_data = await self.page.evaluate("""
                () => {
                    const flags = [];
                    // Check common feature flag patterns
                    if (window.featureFlags) {
                        for (const [key, value] of Object.entries(window.featureFlags)) {
                            flags.push({name: key, value: value});
                        }
                    }
                    if (window.LaunchDarkly) {
                        // LaunchDarkly pattern
                        const ldFlags = window.LaunchDarkly.allFlags();
                        for (const [key, value] of Object.entries(ldFlags || {})) {
                            flags.push({name: key, value: value, source: 'LaunchDarkly'});
                        }
                    }
                    return flags;
                }
            """)
            
            for flag_data in flags_data:
                flag_resolutions.append(FlagResolution(**flag_data))
                
        except Exception as e:
            logger.debug(f"Flag resolution capture failed: {e}")
        
        return flag_resolutions
    
    async def _capture_network_traces(self) -> List[NetworkTrace]:
        """Capture network requests for data residency analysis"""
        # For MVP, we'll return mock data
        # In full implementation, would intercept network requests
        return [
            NetworkTrace(host="api.example.com", region_hint="us-east"),
            NetworkTrace(host="cdn.example.com", region_hint="global")
        ]
    
    async def _save_trace(self) -> Optional[Path]:
        """Save browser trace for evidence"""
        # For MVP, return None
        # In full implementation, would save Playwright trace
        return None
    
    def _mock_runtime_signals(self, persona: Persona) -> RuntimeSignals:
        """Generate mock runtime signals when Playwright is not available"""
        logger.info("Using mock runtime signals - Playwright not available")
        
        signals = RuntimeSignals(persona=persona)
        
        # Mock blocked actions based on persona
        if persona.age < 18:
            signals.blocked_actions = [
                "age_restricted_content_hidden",
                "adult_features_disabled",
                "parental_consent_required"
            ]
        
        # Mock UI states
        signals.ui_states = [
            "age_verification_modal_visible" if persona.age < 18 else "standard_ui",
            "cookie_banner_visible",
            "privacy_settings_available"
        ]
        
        # Mock feature flags
        signals.flag_resolutions = [
            FlagResolution(name="compliance_mode", value=True),
            FlagResolution(name="age_verification_enabled", value=persona.age < 18),
            FlagResolution(name="gdpr_mode", value=persona.country in ["FR", "GB"]),
            FlagResolution(name="utah_minor_restrictions", value=persona.age < 18 and persona.region == "UT")
        ]
        
        # Mock network traces
        signals.network = [
            NetworkTrace(host="api.example.com", region_hint="us-east"),
            NetworkTrace(host="eu-api.example.com", region_hint="eu-west") if persona.country == "FR" else NetworkTrace(host="api.example.com", region_hint="us-east")
        ]
        
        return signals


class RuntimeProbeEngine:
    """Main runtime probe engine"""
    
    def __init__(self):
        self.persona_manager = PersonaManager()
    
    async def probe_feature(self, persona_name: str, url: str, feature_id: Optional[str] = None) -> EvidencePack:
        """Probe feature with specified persona"""
        persona = self.persona_manager.get_persona(persona_name)
        
        if feature_id is None:
            feature_id = f"probe_{persona_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        async with PlaywrightProber() as prober:
            runtime_signals = await prober.probe_with_persona(url, persona)
        
        # Create evidence pack
        evidence = EvidencePack(
            feature_id=feature_id,
            metadata=EvidenceMetadata()
        )
        evidence.add_runtime_signals(runtime_signals)
        
        return evidence


def probe_feature(persona_name: str, url: str, feature_id: Optional[str] = None) -> Dict[str, Any]:
    """Main entry point for runtime probing"""
    engine = RuntimeProbeEngine()
    
    # Run async probe
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        evidence = loop.run_until_complete(engine.probe_feature(persona_name, url, feature_id))
    finally:
        loop.close()
    
    # Save evidence to file
    if feature_id is None:
        feature_id = evidence.feature_id
    
    output_path = Path("./artifacts/evidence") / f"{feature_id}_runtime.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(evidence.model_dump(), f, indent=2, default=str)
    
    return evidence.model_dump()
