"""
Compliance Detection System (CDS) - Main CLI Entry Point

This module provides the main CLI interface for the Compliance Detection System.
"""

import typer
from rich.console import Console
from rich.table import Table
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from ..scanner.main import scan_repository
from ..runtime.main import probe_feature  
from ..rules.main import evaluate_feature
from ..llm.main import explain_feature
from ..evidence.pipeline import run_pipeline

import typer
from rich.console import Console
from rich.table import Table
import sys
from pathlib import Path
from typing import Optional

from ..scanner.main import scan_repository
from ..runtime.main import probe_feature  
from ..rules.main import evaluate_feature
from ..llm.main import explain_feature
from ..evidence.pipeline import run_pipeline

app = typer.Typer(
    name="cds",
    help="Compliance Detection System - Detect geo-specific compliance requirements",
    rich_markup_mode="rich"
)

console = Console()

@app.command()
def scan(
    repo: Path = typer.Option(..., "--repo", "-r", help="Path to repository to scan"),
    feature: str = typer.Option(..., "--feature", "-f", help="Feature name to analyze"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output evidence file path")
) -> None:
    """
    🔍 Scan repository for compliance-related signals using static analysis.
    
    This command runs semgrep rules and tree-sitter AST analysis to extract
    static signals like geo-branching, age checks, and data residency patterns.
    """
    console.print(f"[bold blue]🔍 Scanning repository:[/bold blue] {repo}")
    console.print(f"[bold blue]📋 Feature:[/bold blue] {feature}")
    
    try:
        result = scan_repository(repo, feature, output)
        
        # Display results
        table = Table(title="Static Analysis Results")
        table.add_column("Signal Type", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Files", style="yellow")
        
        signals = result.get("signals", {}).get("static", {})
        for signal_type, signal_data in signals.items():
            if isinstance(signal_data, list):
                count = len(signal_data)
                files = set()
                for item in signal_data:
                    if isinstance(item, dict) and "file" in item:
                        files.add(item["file"])
                files_str = ", ".join(sorted(files)[:3])
                if len(files) > 3:
                    files_str += f" (+{len(files) - 3} more)"
            else:
                count = 1 if signal_data else 0
                files_str = "-"
            
            table.add_row(signal_type, str(count), files_str)
        
        console.print(table)
        
        if output:
            console.print(f"[bold green]✅ Evidence saved to:[/bold green] {output}")
        else:
            console.print(f"[bold green]✅ Evidence saved to:[/bold green] ./artifacts/evidence/{feature}.json")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error during scan:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def probe(
    persona: str = typer.Option(..., "--persona", "-p", help="Test persona (ut_minor|fr_adult)"),
    url: str = typer.Option(..., "--url", "-u", help="Target URL to probe"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Feature name for evidence storage")
) -> None:
    """
    🎭 Probe application with different personas to capture runtime behavior.
    
    Uses Playwright to simulate different user personas and capture compliance-
    related runtime signals like blocked actions and UI state changes.
    """
    console.print(f"[bold blue]🎭 Probing with persona:[/bold blue] {persona}")
    console.print(f"[bold blue]🌐 Target URL:[/bold blue] {url}")
    
    try:
        result = probe_feature(persona, url, feature)
        
        # Display results
        table = Table(title="Runtime Probe Results")
        table.add_column("Signal Type", style="cyan")
        table.add_column("Value", style="green")
        
        runtime_signals = result.get("signals", {}).get("runtime", {})
        for signal_type, signal_value in runtime_signals.items():
            if isinstance(signal_value, list):
                value_str = f"{len(signal_value)} items"
            elif isinstance(signal_value, dict):
                value_str = f"{len(signal_value)} properties"
            else:
                value_str = str(signal_value)
            
            table.add_row(signal_type, value_str)
        
        console.print(table)
        console.print(f"[bold green]✅ Runtime evidence captured[/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error during probe:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def evaluate(
    feature: str = typer.Option(..., "--feature", "-f", help="Feature name to evaluate"),
    evidence_file: Optional[Path] = typer.Option(None, "--evidence", "-e", help="Path to evidence file")
) -> None:
    """
    ⚖️ Evaluate feature against compliance rules using json-logic.
    
    Applies predefined compliance rules to the collected evidence and calculates
    confidence scores for regulatory requirements.
    """
    console.print(f"[bold blue]⚖️ Evaluating feature:[/bold blue] {feature}")
    
    try:
        result = evaluate_feature(feature, evidence_file)
        
        # Display results
        console.print(f"[bold]Requires Geo Logic:[/bold] {'✅ Yes' if result.get('requires_geo_logic') else '❌ No'}")
        console.print(f"[bold]Confidence Score:[/bold] {result.get('confidence', 0.0):.2f}")
        
        matched_rules = result.get("matched_rules", [])
        if matched_rules:
            console.print(f"[bold green]📋 Matched Rules ({len(matched_rules)}):[/bold green]")
            for rule in matched_rules:
                console.print(f"  • {rule}")
        
        missing_controls = result.get("missing_controls", [])
        if missing_controls:
            console.print(f"[bold yellow]⚠️ Missing Controls ({len(missing_controls)}):[/bold yellow]")
            for control in missing_controls:
                console.print(f"  • {control}")
        
        console.print(f"[bold green]✅ Evaluation complete[/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error during evaluation:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def explain(
    feature: str = typer.Option(..., "--feature", "-f", help="Feature name to explain"),
    evidence_file: Optional[Path] = typer.Option(None, "--evidence", "-e", help="Path to evidence file")
) -> None:
    """
    🤖 Generate LLM-powered explanation for compliance requirements.
    
    Uses Gemini 1.5 Pro to analyze evidence and provide detailed reasoning
    about regulatory compliance requirements.
    """
    console.print(f"[bold blue]🤖 Generating explanation for:[/bold blue] {feature}")
    
    try:
        result = explain_feature(feature, evidence_file)
        
        # Display results
        console.print(f"\n[bold]📋 Feature ID:[/bold] {result.get('feature_id')}")
        console.print(f"[bold]🎯 Requires Geo Logic:[/bold] {'✅ Yes' if result.get('requires_geo_logic') else '❌ No'}")
        console.print(f"[bold]📊 Confidence:[/bold] {result.get('confidence', 0.0):.2f}")
        console.print(f"[bold]⚠️ Severity:[/bold] {result.get('severity', 'unknown').upper()}")
        
        console.print(f"\n[bold blue]💭 Reasoning:[/bold blue]")
        console.print(result.get('reasoning', 'No reasoning provided'))
        
        regulations = result.get("related_regulations", [])
        if regulations:
            console.print(f"\n[bold green]📋 Related Regulations:[/bold green]")
            for reg in regulations:
                console.print(f"  • {reg}")
        
        console.print(f"\n[bold green]✅ Explanation generated successfully[/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error during explanation:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def pipeline(
    dataset: Path = typer.Option(..., "--dataset", "-d", help="Input CSV dataset path"),
    output: Path = typer.Option("./artifacts/final.csv", "--output", "-o", help="Output CSV path"),
    report: Path = typer.Option("./artifacts/report.html", "--report", help="HTML report path")
) -> None:
    """
    🚀 Run complete compliance detection pipeline on dataset.
    
    Processes multiple features through the complete pipeline:
    scan → evaluate → explain → export
    """
    console.print(f"[bold blue]🚀 Running pipeline on dataset:[/bold blue] {dataset}")
    
    try:
        result = run_pipeline(dataset, output, report)
        
        # Display results
        console.print(f"\n[bold green]✅ Pipeline completed successfully![/bold green]")
        console.print(f"[bold]📊 Features processed:[/bold] {result.get('processed_count', 0)}")
        console.print(f"[bold]⚠️ Errors:[/bold] {result.get('error_count', 0)}")
        console.print(f"[bold]📄 CSV output:[/bold] {output}")
        console.print(f"[bold]📋 HTML report:[/bold] {report}")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error during pipeline:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def version():
    """📦 Show CDS version information"""
    console.print("[bold blue]CDS - Compliance Detection System[/bold blue]")
    console.print("Version: 0.1.0")
    console.print("Python: " + sys.version.split()[0])

if __name__ == "__main__":
    app()
