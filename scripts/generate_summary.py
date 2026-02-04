#!/usr/bin/env python3
"""
Context Summarizer - Generate conversation context summaries

Usage:
    python generate_summary.py --session SESSION_ID --format both
    python generate_summary.py --auto-detect
    python generate_summary.py --recover SESSION_ID

Output:
    - session_summary.md (human-readable)
    - session_summary.json (machine-readable)
"""

import json
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import yaml


# ============== Data Classes ==============

@dataclass
class ProjectStatus:
    """Project status summary"""
    name: str
    description: str
    phase: int
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    pending_tasks: List[Dict[str, str]]


@dataclass
class TechDecision:
    """Technical decision"""
    decision: str
    status: str  # confirmed, pending, rejected
    reason: str


@dataclass
class CodeContext:
    """Current code context"""
    current_files: List[str]
    recent_changes: List[str]
    architecture_patterns: List[str]


@dataclass
class ConversationHistory:
    """Conversation history summary"""
    key_discussions: List[str]
    confirmed_items: List[str]
    pending_confirmations: List[str]


@dataclass
class RecoveryInstructions:
    """Recovery instructions for new session"""
    read_first: List[str]
    continue_from: str
    key_context: str


@dataclass
class ContextSummary:
    """Complete context summary"""
    version: str
    generated_at: str
    session_id: str
    project: Dict[str, Any]
    tech_decisions: List[Dict[str, str]]
    code_context: Dict[str, Any]
    conversation_history: Dict[str, Any]
    recovery_instructions: Dict[str, Any]


# ============== Summary Generator ==============

class ContextSummarizer:
    """Generate context summaries for session continuity"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.getcwd()
        self.timestamp = datetime.now(timezone.utc).isoformat()
        
    def generate(
        self,
        session_id: str,
        output_format: str = "both",
        include_sections: List[str] = None,
        max_words: int = 2000
    ) -> Dict[str, str]:
        """
        Generate context summary
        
        Args:
            session_id: Current session ID
            output_format: "text", "json", or "both"
            include_sections: Sections to include
            max_words: Maximum words in summary
            
        Returns:
            Dict with "md" and/or "json" keys
        """
        # Load project context
        project = self._load_project_status()
        decisions = self._load_tech_decisions()
        code = self._load_code_context()
        history = self._load_conversation_history()
        
        # Create recovery instructions
        recovery = RecoveryInstructions(
            read_first=["README.md", "AGENTS.md"],
            continue_from=self._get_continue_from(project),
            key_context=self._get_key_context(project)
        )
        
        # Build summary
        summary = ContextSummary(
            version="1.0",
            generated_at=self.timestamp,
            session_id=session_id,
            project=asdict(project),
            tech_decisions=[asdict(d) for d in decisions],
            code_context=asdict(code),
            conversation_history=asdict(history),
            recovery_instructions=asdict(recovery)
        )
        
        # Generate outputs
        outputs = {}
        
        if output_format in ["json", "both"]:
            outputs["json"] = self._to_json(summary)
            
        if output_format in ["text", "both"]:
            outputs["text"] = self._to_text(summary, max_words)
            
        return outputs
    
    def save(
        self,
        outputs: Dict[str, str],
        base_path: str = None
    ) -> Dict[str, str]:
        """
        Save summary to files
        
        Returns:
            Dict with file paths
        """
        base_path = base_path or self.project_root
        saved = {}
        
        if "json" in outputs:
            json_path = os.path.join(base_path, "session_summary.json")
            with open(json_path, "w", encoding="utf-8") as f:
                f.write(outputs["json"])
            saved["json"] = json_path
            
        if "text" in outputs:
            md_path = os.path.join(base_path, "session_summary.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(outputs["text"])
            saved["text"] = md_path
            
        return saved
    
    def recover(self, base_path: str = None) -> Optional[ContextSummary]:
        """
        Load summary from files for recovery
        
        Returns:
            ContextSummary or None
        """
        base_path = base_path or self.project_root
        
        json_path = os.path.join(base_path, "session_summary.json")
        
        if not os.path.exists(json_path):
            return None
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return ContextSummary(**data)
    
    # ============== Private Methods ==============
    
    def _load_project_status(self) -> ProjectStatus:
        """Load project status from AGENTS.md"""
        agents_path = os.path.join(self.project_root, "AGENTS.md")
        
        # Default values
        project = {
            "name": "Project",
            "description": "A coding project",
            "phase": 1,
            "total_tasks": 50,
            "completed_tasks": 0,
            "pending_tasks": []
        }
        
        if os.path.exists(agents_path):
            try:
                # Simple parsing for task completion
                with open(agents_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Count completed vs total tasks
                completed = content.count("[x]") + content.count("✅")
                # Estimate total from structure
                total = content.count("任务") + content.count("Task")
                
                # Try to extract phase info
                import re
                phase_match = re.search(r"第[一二三四五六七八九十]+阶段", content)
                
                project["completed_tasks"] = completed
                project["completion_rate"] = completed / max(total, 1) if total > 0 else 0
                
            except Exception as e:
                print(f"Warning: Failed to parse AGENTS.md: {e}", file=sys.stderr)
        
        # Try to load from config if exists
        config_path = os.path.join(self.project_root, "config", "project.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    project.update(config)
            except Exception:
                pass
        
        return ProjectStatus(**project)
    
    def _load_tech_decisions(self) -> List[TechDecision]:
        """Load technical decisions"""
        decisions_path = os.path.join(
            self.project_root, "docs", "tech_decisions.md"
        )
        
        default_decisions = [
            TechDecision(
                decision="Standard architecture",
                status="confirmed",
                reason="Default decision for new projects"
            )
        ]
        
        if not os.path.exists(decisions_path):
            return default_decisions
            
        try:
            with open(decisions_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Simple parsing
            decisions = []
            import re
            
            # Look for decision patterns
            patterns = re.findall(
                r"[-•]\s*(.+?):\s*(.+)",
                content,
                re.MULTILINE
            )
            
            for i, (decision, reason) in enumerate(patterns[:10]):
                decisions.append(TechDecision(
                    decision=decision.strip(),
                    status="confirmed",
                    reason=reason.strip()
                ))
            
            return decisions if decisions else default_decisions
            
        except Exception as e:
            print(f"Warning: Failed to parse tech decisions: {e}", file=sys.stderr)
            return default_decisions
    
    def _load_code_context(self) -> CodeContext:
        """Load current code context"""
        return CodeContext(
            current_files=self._list_current_files(),
            recent_changes=self._get_recent_changes(),
            architecture_patterns=self._detect_architecture()
        )
    
    def _load_conversation_history(self) -> ConversationHistory:
        """Load conversation history"""
        # Default empty history
        return ConversationHistory(
            key_discussions=[],
            confirmed_items=[],
            pending_confirmations=[]
        )
    
    def _list_current_files(self) -> List[str]:
        """List current/recent files"""
        files = []
        
        # Common source directories
        for pattern in ["src/**/*.py", "src/**/*"]:
            for path in Path(self.project_root).glob(pattern):
                if path.is_file():
                    rel_path = str(path.relative_to(self.project_root))
                    if len(files) < 10:
                        files.append(rel_path)
        
        # Config files
        for pattern in ["config/*.json", "config/*.yaml"]:
            for path in Path(self.project_root).glob(pattern):
                if path.is_file():
                    files.append(str(path.relative_to(self.project_root)))
        
        return files[:15]
    
    def _get_recent_changes(self) -> List[str]:
        """Get recent changes"""
        changes = []
        
        # Check git if available
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.project_root,
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.decode().strip().split("\n")[:5]
                for line in lines:
                    if line.strip():
                        changes.append(line.strip())
        except Exception:
            pass
        
        return changes[:5]
    
    def _detect_architecture(self) -> List[str]:
        """Detect architecture patterns"""
        patterns = []
        
        # Check for common patterns
        dirs = ["src", "tests", "config", "docs", "scripts"]
        for d in dirs:
            path = Path(self.project_root) / d
            if path.exists():
                patterns.append(d)
        
        # Check for specific files
        files = {
            "requirements.txt": "Python project",
            "package.json": "Node.js project",
            "pyproject.toml": "Python (Poetry)",
            "docker-compose.yml": "Docker",
            "AGENTS.md": "OpenCode workflow",
        }
        
        for filename, pattern in files.items():
            if (Path(self.project_root) / filename).exists():
                patterns.append(pattern)
        
        return patterns[:5]
    
    def _get_continue_from(self, project: ProjectStatus) -> str:
        """Get continue instruction"""
        if project.pending_tasks:
            next_task = project.pending_tasks[0]
            return f"Task {next_task['id']}: {next_task['name']}"
        return f"Phase {project.phase} completion"
    
    def _get_key_context(self, project: ProjectStatus) -> str:
        """Get key context string"""
        return f"{project.name} - Phase {project.phase}, {project.completion_rate:.0%} complete"
    
    def _to_json(self, summary: ContextSummary) -> str:
        """Convert to JSON"""
        return json.dumps(asdict(summary), indent=2, ensure_ascii=False)
    
    def _to_text(self, summary: ContextSummary, max_words: int = 2000) -> str:
        """Convert to human-readable text"""
        lines = []
        word_count = 0
        
        # Header
        lines.append("# Context Summary")
        lines.append(f"\nGenerated: {summary.generated_at}")
        lines.append(f"Session: {summary.session_id}")
        
        # Project Status
        project = summary.project
        lines.append("\n## Project Status")
        lines.append(f"**{project['name']}** - {project['description']}")
        lines.append(f"- Current Phase: Phase {project['phase']}")
        lines.append(f"- Completion: {project['completed_tasks']}/{project['total_tasks']} tasks ({project['completion_rate']:.0%}%)")
        
        if project['pending_tasks']:
            lines.append(f"- Pending: {', '.join(t['name'] for t in project['pending_tasks'][:3])}")
        
        word_count += 200
        
        # Pending Tasks
        if summary.pending_tasks:
            lines.append("\n## Pending Tasks")
            
            # Group by priority
            high = [t for t in summary.pending_tasks if t['priority'] == 'high']
            medium = [t for t in summary.pending_tasks if t['priority'] == 'medium']
            
            if high:
                lines.append("🔴 High Priority:")
                for task in high[:3]:
                    lines.append(f"- Task {task['id']}: {task['name']}")
            
            if medium:
                lines.append("🟡 Medium Priority:")
                for task in medium[:3]:
                    lines.append(f"- Task {task['id']}: {task['name']}")
            
            word_count += 500
        
        # Technical Decisions
        if summary.tech_decisions:
            lines.append("\n## Technical Decisions")
            lines.append("✅ Confirmed:")
            for decision in summary.tech_decisions[:5]:
                if decision['status'] == 'confirmed':
                    lines.append(f"- {decision['decision']}")
                    if decision['reason']:
                        lines.append(f"  Reason: {decision['reason'][:100]}")
            
            word_count += 300
        
        # Code Context
        if summary.code_context:
            lines.append("\n## Code Context")
            code = summary.code_context
            
            if code['current_files']:
                lines.append("📁 Current Files:")
                for f in code['current_files'][:5]:
                    lines.append(f"- {f}")
            
            if code['recent_changes']:
                lines.append("\n📝 Recent Changes:")
                for change in code['recent_changes'][:3]:
                    lines.append(f"- {change}")
            
            if code['architecture_patterns']:
                lines.append(f"\n📐 Architecture: {', '.join(code['architecture_patterns'])}")
            
            word_count += 500
        
        # Conversation History
        if summary.conversation_history:
            lines.append("\n## Conversation History")
            history = summary.conversation_history
            
            if history['key_discussions']:
                lines.append("💬 Key Discussions:")
                for d in history['key_discussions'][:3]:
                    lines.append(f"- {d}")
            
            if history['confirmed_items']:
                lines.append("\n✅ Confirmed:")
                for item in history['confirmed_items'][:3]:
                    lines.append(f"- {item}")
            
            if history['pending_confirmations']:
                lines.append("\n❓ Pending:")
                for item in history['pending_confirmations'][:3]:
                    lines.append(f"- {item}")
            
            word_count += 500
        
        # Recovery Instructions
        recovery = summary.recovery_instructions
        lines.append("\n## Recovery Instructions")
        lines.append("\n📖 Read First:")
        for f in recovery['read_first']:
            lines.append(f"- {f}")
        lines.append(f"\n🚀 Continue from: {recovery['continue_from']}")
        lines.append(f"\n🔑 Key Context: {recovery['key_context']}")
        
        # Footer
        lines.append("\n" + "="*50)
        lines.append("Ready for new session recovery! 🚀")
        
        return "\n".join(lines)
    
    def auto_detect(self) -> tuple[bool, float]:
        """
        Auto-detect if summary should be generated
        
        Returns:
            (should_generate, token_usage)
        """
        try:
            # This is a placeholder - actual implementation would
            # check actual token usage
            token_usage = self._estimate_token_usage()
            return token_usage > 0.8, token_usage
        except Exception:
            return False, 0.0
    
    def _estimate_token_usage(self) -> float:
        """
        Estimate current token usage
        
        This is a placeholder - actual implementation would
        track token usage more accurately
        """
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            # Rough estimate: 1MB ≈ 100K tokens for Python code
            # This is very approximate
            estimated_tokens = memory_info.rss / 1024 / 1024 * 100
            
            # Claude's context window varies, assume 200K tokens
            return min(estimated_tokens / 200000, 1.0)
        except Exception:
            return 0.0


# ============== CLI Interface ==============

def main():
    parser = argparse.ArgumentParser(
        description="Context Summarizer - Generate conversation context summaries"
    )
    
    parser.add_argument(
        "--session", "-s",
        help="Session ID",
        default=f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "both"],
        default="both",
        help="Output format"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output directory (default: current directory)"
    )
    
    parser.add_argument(
        "--auto-detect", "-a",
        action="store_true",
        help="Auto-detect if summary needed"
    )
    
    parser.add_argument(
        "--recover", "-r",
        help="Recover from previous summary"
    )
    
    parser.add_argument(
        "--max-words",
        type=int,
        default=2000,
        help="Maximum words in text summary"
    )
    
    args = parser.parse_args()
    
    # Handle recovery
    if args.recover:
        summarizer = ContextSummarizer()
        summary = summarizer.recover()
        if summary:
            print(json.dumps(asdict(summary), indent=2)
        else:
            print("No previous summary found", file=sys.stderr)
            sys.exit(1)
        return
    
    # Handle auto-detect
    if args.auto_detect:
        summarizer = ContextSummarizer()
        should_generate, usage = summarizer.auto_detect()
        print(f"Token usage: {usage:.0%}")
        if should_generate:
            print("⚠️ Token usage exceeds 80%. Summary recommended.")
        return
    
    # Generate summary
    summarizer = ContextSummarizer()
    
    sections = ["project", "tasks", "decisions", "code", "history"]
    
    outputs = summarizer.generate(
        session_id=args.session,
        output_format=args.format,
        include_sections=sections,
        max_words=args.max_words
    )
    
    saved = summarizer.save(outputs, args.output)
    
    print("Summary generated:")
    for fmt, path in saved.items():
        print(f"  [{fmt.upper()}] {path}")
    
    print("\nReady for new session recovery! 🚀")


if __name__ == "__main__":
    main()
