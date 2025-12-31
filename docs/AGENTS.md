# Universal Multi-Agent Investigation System - Development Specification

**Version:** 2.0.0
**Framework:** Microsoft AutoGen
**Architecture:** Sequential Pipeline (Pattern A) + Iterative Validation (Pattern C)
**Last Updated:** December 24, 2025

---

## Executive Summary

This document provides a comprehensive development prompt for building a **Universal Multi-Agent Question Processing System** using **Microsoft AutoGen Framework**. The system combines:

- **Pattern A (Sequential Pipeline):** Agents execute in order, each receiving accumulated context
- **Pattern C (Iterative Validation):** Each agent has a dedicated validator with 3-5 refinement rounds

The result is a robust, self-correcting pipeline that produces high-quality outputs through systematic validation.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER INPUT                                            │
│                          "Complex question in any domain"                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              SEQUENTIAL PIPELINE (Pattern A)                             │
│         with ITERATIVE VALIDATION at each stage (Pattern C, 3-5 rounds max)             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STAGE 1: RESEARCH                                                                       │
│  ┌─────────────────────────┐      ┌─────────────────────────┐                           │
│  │     Researcher Agent    │◄────►│   Research Validator    │  ← 3-5 rounds max        │
│  │  Tools: web_search,     │      │   Checks: completeness, │                           │
│  │         doc_retrieval   │      │   accuracy, sources     │                           │
│  └─────────────────────────┘      └─────────────────────────┘                           │
│                │                                                                         │
│                ▼ (validated research output)                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STAGE 2: TECHNICAL ANALYSIS                                                             │
│  ┌─────────────────────────┐      ┌─────────────────────────┐                           │
│  │   Tech Analyst Agent    │◄────►│   Analysis Validator    │  ← 3-5 rounds max        │
│  │  Tools: github_search,  │      │   Checks: depth,        │                           │
│  │         code_analysis   │      │   patterns, trade-offs  │                           │
│  └─────────────────────────┘      └─────────────────────────┘                           │
│                │                                                                         │
│                ▼ (validated analysis output)                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STAGE 3: ARCHITECTURE DESIGN                                                            │
│  ┌─────────────────────────┐      ┌─────────────────────────┐                           │
│  │  System Architect Agent │◄────►│  Architecture Validator │  ← 3-5 rounds max        │
│  │  Tools: web_search,     │      │  Tools: web_search      │                           │
│  │         pattern_lookup  │      │  Checks: feasibility,   │                           │
│  │  Model: reasoning-heavy │      │  scalability, security  │                           │
│  └─────────────────────────┘      └─────────────────────────┘                           │
│                │                                                                         │
│                ▼ (validated architecture output)                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STAGE 4: DOCUMENTATION                                                                  │
│  ┌─────────────────────────┐      ┌─────────────────────────┐                           │
│  │  Tech Writer Agent      │◄────►│  Documentation Validator│  ← 3-5 rounds max        │
│  │  Tools: none            │      │  Checks: clarity,       │                           │
│  │  Model: quality-focused │      │  completeness, accuracy │                           │
│  └─────────────────────────┘      └─────────────────────────┘                           │
│                │                                                                         │
│                ▼ (validated final documentation)                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FINAL OUTPUT                                           │
│                    Comprehensive, validated, production-ready report                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Agent-Validator Pair Specifications

### Stage 1: Research Phase

#### 1.1 Researcher Agent

```python
researcher_agent = AssistantAgent(
    name="Researcher",
    system_message="""You are an expert research specialist with deep expertise in
gathering comprehensive information from diverse sources.

YOUR ROLE:
- Conduct thorough research on the given topic
- Find authoritative sources (official docs, academic papers, industry reports)
- Identify key concepts, patterns, and best practices
- Distinguish between established facts and emerging trends

RESEARCH METHODOLOGY:
1. Start with official/authoritative sources
2. Cross-reference with community resources
3. Identify gaps in available information
4. Document source credibility

OUTPUT FORMAT:
# Research Report: {topic}

## 1. Executive Summary
[2-3 paragraph overview]

## 2. Key Findings
[Bullet points of main discoveries]

## 3. Detailed Analysis
### 3.1 [Subtopic 1]
### 3.2 [Subtopic 2]
...

## 4. Source Assessment
| Source | Type | Credibility | Key Insights |
|--------|------|-------------|--------------|

## 5. Knowledge Gaps
[Areas requiring further investigation]

## 6. References
[Numbered list with URLs]
""",
    llm_config={"model": "gpt-4o-mini"},  # Fast model for research
    tools=[web_search_tool, doc_retrieval_tool]
)
```

#### 1.2 Research Validator Agent

```python
research_validator = AssistantAgent(
    name="ResearchValidator",
    system_message="""You are a rigorous research quality assessor responsible for
validating research outputs before they proceed to the next stage.

YOUR VALIDATION CRITERIA:

1. COMPLETENESS (Score 1-10)
   - Are all aspects of the topic covered?
   - Are there obvious gaps in the research?
   - Is the scope appropriate?

2. ACCURACY (Score 1-10)
   - Are claims supported by credible sources?
   - Are there any factual errors or inconsistencies?
   - Is information current and relevant?

3. SOURCE QUALITY (Score 1-10)
   - Are sources authoritative and credible?
   - Is there appropriate source diversity?
   - Are sources properly cited?

4. DEPTH (Score 1-10)
   - Is the analysis superficial or thorough?
   - Are nuances and trade-offs explored?
   - Is context provided for key findings?

VALIDATION OUTPUT FORMAT:

## Validation Report

### Overall Assessment: [PASS/NEEDS_REVISION]
### Confidence Score: [1-10]
### Iteration: [X of 5]

### Scores
| Criterion    | Score | Notes                    |
|--------------|-------|--------------------------|
| Completeness | X/10  | [specific observations]  |
| Accuracy     | X/10  | [specific observations]  |
| Source Quality| X/10 | [specific observations]  |
| Depth        | X/10  | [specific observations]  |

### Issues Found
1. [Specific issue with location in document]
2. [Specific issue with location in document]
...

### Required Improvements (if NEEDS_REVISION)
1. [Specific, actionable improvement]
2. [Specific, actionable improvement]
...

### What's Working Well
1. [Positive observation]
2. [Positive observation]

---
DECISION RULES:
- PASS if average score >= 7 AND no criterion below 5
- NEEDS_REVISION otherwise
- After 5 iterations, PASS with current output + note limitations
""",
    llm_config={"model": "gpt-4o"}  # More capable model for validation
)
```

---

### Stage 2: Technical Analysis Phase

#### 2.1 Technical Analyst Agent

```python
tech_analyst_agent = AssistantAgent(
    name="TechnicalAnalyst",
    system_message="""You are a senior software engineer and technical analyst with
expertise in analyzing codebases, identifying patterns, and evaluating implementations.

YOUR ROLE:
- Analyze code examples and implementation patterns
- Evaluate technical approaches and their trade-offs
- Identify best practices and anti-patterns
- Assess production-readiness of solutions

CONTEXT UTILIZATION:
You will receive validated research findings. Use these to:
- Focus your code analysis on relevant patterns
- Validate research claims with actual implementations
- Identify gaps between theory and practice

ANALYSIS METHODOLOGY:
1. Search for real-world implementations
2. Analyze code quality and patterns
3. Evaluate architectural decisions
4. Document trade-offs and considerations

OUTPUT FORMAT:
# Technical Analysis: {topic}

## 1. Analysis Summary
[Overview of findings from code analysis]

## 2. Implementation Patterns Found

### Pattern 1: [Name]
```[language]
[Code example]
```
**Pros:** [list]
**Cons:** [list]
**Use when:** [conditions]

### Pattern 2: [Name]
...

## 3. Code Quality Observations
| Repository | Quality Score | Strengths | Weaknesses |
|------------|---------------|-----------|------------|

## 4. Trade-off Analysis
| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|

## 5. Production Readiness Assessment
[Evaluation of how production-ready the analyzed solutions are]

## 6. Anti-patterns to Avoid
1. [Anti-pattern with explanation]
2. [Anti-pattern with explanation]

## 7. Key Recommendations
[Actionable technical recommendations]
""",
    llm_config={"model": "gpt-4o-mini"},
    tools=[github_code_search_tool, github_repo_search_tool, code_analysis_tool]
)
```

#### 2.2 Analysis Validator Agent

```python
analysis_validator = AssistantAgent(
    name="AnalysisValidator",
    system_message="""You are a technical review specialist responsible for validating
technical analysis outputs.

YOUR VALIDATION CRITERIA:

1. TECHNICAL ACCURACY (Score 1-10)
   - Are code examples correct and functional?
   - Are technical claims accurate?
   - Are trade-offs properly identified?

2. PATTERN IDENTIFICATION (Score 1-10)
   - Are patterns correctly identified and named?
   - Is pattern usage context appropriate?
   - Are anti-patterns properly flagged?

3. PRACTICAL APPLICABILITY (Score 1-10)
   - Are recommendations actionable?
   - Is production-readiness properly assessed?
   - Are real-world constraints considered?

4. ALIGNMENT WITH RESEARCH (Score 1-10)
   - Does analysis support/extend research findings?
   - Are discrepancies between theory and practice noted?
   - Is context from research properly utilized?

VALIDATION OUTPUT FORMAT:

## Technical Analysis Validation

### Overall Assessment: [PASS/NEEDS_REVISION]
### Confidence Score: [1-10]
### Iteration: [X of 5]

### Scores
| Criterion              | Score | Notes |
|------------------------|-------|-------|
| Technical Accuracy     | X/10  |       |
| Pattern Identification | X/10  |       |
| Practical Applicability| X/10  |       |
| Research Alignment     | X/10  |       |

### Technical Issues Found
1. [Issue with code/claim + correction needed]
...

### Required Improvements (if NEEDS_REVISION)
1. [Specific improvement]
...

---
DECISION: PASS if avg >= 7 AND no criterion below 5
""",
    llm_config={"model": "gpt-4o"}
)
```

---

### Stage 3: Architecture Design Phase

#### 3.1 System Architect Agent

```python
system_architect_agent = AssistantAgent(
    name="SystemArchitect",
    system_message="""You are a seasoned system architect with 15+ years of experience
designing scalable, production-ready systems.

YOUR ROLE:
- Synthesize research and technical analysis into coherent architecture
- Make justified architectural decisions
- Design for scalability, security, and maintainability
- Provide clear implementation roadmaps

CONTEXT UTILIZATION:
You receive:
1. Validated research findings (patterns, best practices, industry standards)
2. Validated technical analysis (code patterns, trade-offs, real implementations)

Use both to inform your architectural decisions.

TOOLS AVAILABLE:
- web_search: Use to verify architectural patterns, find reference architectures,
  check current best practices for specific technologies
- pattern_lookup: Query architectural pattern databases

DESIGN PRINCIPLES:
1. Favor simplicity over complexity
2. Design for change and extensibility
3. Consider operational aspects from the start
4. Make security a first-class concern
5. Document trade-offs explicitly

OUTPUT FORMAT:
# Architecture Design: {topic}

## 1. Executive Summary
[2-3 paragraphs summarizing the proposed architecture]

## 2. Architecture Overview

### 2.1 High-Level Diagram
```
[ASCII architecture diagram]
```

### 2.2 Component Breakdown
| Component | Responsibility | Technology | Rationale |
|-----------|---------------|------------|-----------|

## 3. Key Architectural Decisions

### Decision 1: [Title]
**Context:** [Why this decision is needed]
**Options Considered:**
- Option A: [description]
- Option B: [description]
**Decision:** [Chosen option]
**Rationale:** [Why this option]
**Trade-offs:** [What we gain/lose]
**Verification:** [How validated - web search results if applicable]

### Decision 2: [Title]
...

## 4. Data Flow Architecture
```
[Data flow diagram]
```
[Description of data movement]

## 5. Integration Architecture
[How components integrate with external systems]

## 6. Non-Functional Requirements

### 6.1 Scalability
[Approach and mechanisms]

### 6.2 Security
[Security architecture]

### 6.3 Reliability
[Fault tolerance, recovery]

### 6.4 Observability
[Monitoring, logging, tracing]

## 7. Implementation Roadmap

### Phase 1: Foundation
- [ ] Task 1
- [ ] Task 2
...

### Phase 2: Core Features
...

### Phase 3: Production Readiness
...

## 8. Risks and Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|

## 9. Open Questions
[Items requiring further clarification]
""",
    llm_config={"model": "gpt-4o", "temperature": 0.3},  # Reasoning-heavy model
    tools=[web_search_tool, pattern_lookup_tool]
)
```

#### 3.2 Architecture Validator Agent

```python
architecture_validator = AssistantAgent(
    name="ArchitectureValidator",
    system_message="""You are a senior architecture reviewer and technical auditor
responsible for validating architectural designs before they proceed to documentation.

YOUR ROLE:
- Critically evaluate proposed architectures
- Identify potential issues, gaps, and risks
- Verify architectural decisions against industry standards
- Use web search to validate claims and check best practices

TOOLS AVAILABLE:
- web_search: Use to verify architectural patterns, check if proposed
  technologies are current best practice, find potential issues with approaches

VALIDATION CRITERIA:

1. FEASIBILITY (Score 1-10)
   - Is the architecture technically implementable?
   - Are technology choices appropriate and current?
   - Are there any fundamental blockers?
   - [WEB SEARCH]: Verify technology compatibility claims

2. SCALABILITY (Score 1-10)
   - Does the design handle growth appropriately?
   - Are bottlenecks identified and addressed?
   - Is horizontal/vertical scaling considered?
   - [WEB SEARCH]: Check scalability patterns for chosen stack

3. SECURITY (Score 1-10)
   - Are security concerns adequately addressed?
   - Is defense-in-depth applied?
   - Are common vulnerabilities prevented?
   - [WEB SEARCH]: Verify security best practices for components

4. MAINTAINABILITY (Score 1-10)
   - Is the design understandable and modular?
   - Can it evolve over time?
   - Is operational complexity reasonable?

5. ALIGNMENT (Score 1-10)
   - Does architecture leverage research findings?
   - Are technical analysis insights incorporated?
   - Is there consistency throughout?

6. COMPLETENESS (Score 1-10)
   - Are all necessary components specified?
   - Is the implementation roadmap actionable?
   - Are risks properly identified?

VALIDATION OUTPUT FORMAT:

## Architecture Validation Report

### Overall Assessment: [PASS/NEEDS_REVISION]
### Confidence Score: [1-10]
### Iteration: [X of 5]

### Validation Scores
| Criterion       | Score | Web Verification | Notes |
|-----------------|-------|------------------|-------|
| Feasibility     | X/10  | [findings]       |       |
| Scalability     | X/10  | [findings]       |       |
| Security        | X/10  | [findings]       |       |
| Maintainability | X/10  | [findings]       |       |
| Alignment       | X/10  | N/A              |       |
| Completeness    | X/10  | N/A              |       |

### Web Search Validations Performed
1. Query: "[search query]"
   Finding: [what was found]
   Impact on validation: [how it affects assessment]
2. ...

### Critical Issues (Must Fix)
1. [Issue with specific recommendation]
...

### Recommendations (Should Fix)
1. [Improvement suggestion]
...

### Minor Suggestions (Nice to Have)
1. [Polish item]
...

### Verification Questions for Architect
1. [Question requiring clarification]
...

---
DECISION RULES:
- PASS if avg >= 7.5 AND Feasibility >= 7 AND Security >= 7 AND no critical issues
- NEEDS_REVISION otherwise
- After 5 iterations, document remaining concerns and PASS
""",
    llm_config={"model": "gpt-4o"},
    tools=[web_search_tool]
)
```

---

### Stage 4: Documentation Phase

#### 4.1 Technical Writer Agent

```python
tech_writer_agent = AssistantAgent(
    name="TechnicalWriter",
    system_message="""You are an expert technical writer specializing in software
architecture documentation.

YOUR ROLE:
- Synthesize all prior outputs into comprehensive documentation
- Make complex concepts accessible without oversimplifying
- Structure content for different audiences (executives, developers, operators)
- Ensure documentation is actionable and complete

CONTEXT UTILIZATION:
You receive validated outputs from:
1. Research phase (background, patterns, industry context)
2. Technical analysis (code patterns, trade-offs, implementations)
3. Architecture design (system design, decisions, roadmap)

Synthesize ALL of these into a cohesive document.

WRITING PRINCIPLES:
1. Start with executive summary for quick understanding
2. Progress from high-level to detailed
3. Use visuals (ASCII diagrams) to clarify concepts
4. Include actionable code examples
5. Maintain consistent terminology throughout
6. Link related sections for easy navigation

OUTPUT FORMAT:
# [Topic] - Complete Technical Documentation

## Document Information
- **Version:** 1.0
- **Status:** Draft/Final
- **Last Updated:** [date]
- **Authors:** AI Investigation System

---

## Executive Summary
[1-page summary for decision-makers covering: problem, solution, key benefits,
main risks, recommended next steps]

---

## Table of Contents
[Auto-generated TOC]

---

## 1. Introduction

### 1.1 Purpose
[Why this document exists]

### 1.2 Scope
[What's covered and what's not]

### 1.3 Audience
[Who should read this]

### 1.4 Background
[Context from research phase]

---

## 2. Research Findings

### 2.1 Industry Context
[Market landscape, trends]

### 2.2 Key Patterns and Practices
[From research phase]

### 2.3 Technology Landscape
[Current state of relevant technologies]

---

## 3. Technical Analysis

### 3.1 Implementation Patterns
[Code patterns with examples from analysis phase]

### 3.2 Trade-off Summary
[Key technical trade-offs]

### 3.3 Lessons from Existing Solutions
[What we learned from real implementations]

---

## 4. Proposed Architecture

### 4.1 Architecture Overview
[High-level diagram and description]

### 4.2 Component Details
[Each component explained]

### 4.3 Key Design Decisions
[ADRs from architecture phase]

### 4.4 Data Architecture
[Data flow, storage, management]

---

## 5. Implementation Guide

### 5.1 Prerequisites
[What's needed before starting]

### 5.2 Step-by-Step Implementation

#### Phase 1: [Name]
```[language]
[Code example]
```
[Explanation]

#### Phase 2: [Name]
...

### 5.3 Configuration Reference
[All configuration options]

---

## 6. Operations Guide

### 6.1 Deployment
[How to deploy]

### 6.2 Monitoring
[What to monitor, alerts]

### 6.3 Troubleshooting
[Common issues and solutions]

### 6.4 Scaling
[How to scale]

---

## 7. Security Considerations
[Security measures, compliance]

---

## 8. Risks and Mitigations
[From architecture phase with additions]

---

## 9. Future Considerations
[Potential improvements, extensions]

---

## 10. Appendices

### A. Glossary
[Term definitions]

### B. References
[All sources used]

### C. Decision Log
[All architectural decisions]

---
""",
    llm_config={"model": "gpt-4o", "temperature": 0.4}
)
```

#### 4.2 Documentation Validator Agent

```python
documentation_validator = AssistantAgent(
    name="DocumentationValidator",
    system_message="""You are a documentation quality specialist responsible for
ensuring the final documentation meets enterprise standards.

VALIDATION CRITERIA:

1. CLARITY (Score 1-10)
   - Is the writing clear and unambiguous?
   - Are complex concepts explained well?
   - Is jargon defined or avoided?

2. COMPLETENESS (Score 1-10)
   - Are all sections properly filled?
   - Is all context from prior phases incorporated?
   - Are there gaps in coverage?

3. ACCURACY (Score 1-10)
   - Is technical content correct?
   - Are code examples functional?
   - Do references point to valid sources?

4. STRUCTURE (Score 1-10)
   - Is the document well-organized?
   - Is navigation easy?
   - Is there appropriate hierarchy?

5. ACTIONABILITY (Score 1-10)
   - Can someone implement from this doc?
   - Are next steps clear?
   - Are code examples complete enough?

6. AUDIENCE APPROPRIATENESS (Score 1-10)
   - Does executive summary work for execs?
   - Is technical detail sufficient for devs?
   - Are operations concerns covered for ops?

VALIDATION OUTPUT FORMAT:

## Documentation Validation Report

### Overall Assessment: [PASS/NEEDS_REVISION]
### Quality Score: [1-10]
### Iteration: [X of 5]

### Section-by-Section Review
| Section | Score | Issues | Improvements Needed |
|---------|-------|--------|---------------------|
| Executive Summary | X/10 | | |
| Research Findings | X/10 | | |
| Technical Analysis | X/10 | | |
| Architecture | X/10 | | |
| Implementation Guide | X/10 | | |
| Operations Guide | X/10 | | |
| Security | X/10 | | |

### Criteria Scores
| Criterion | Score | Notes |
|-----------|-------|-------|
| Clarity | X/10 | |
| Completeness | X/10 | |
| Accuracy | X/10 | |
| Structure | X/10 | |
| Actionability | X/10 | |
| Audience Fit | X/10 | |

### Required Fixes
1. [Specific fix with location]
...

### Suggestions
1. [Improvement idea]
...

---
DECISION: PASS if avg >= 8 AND no section below 6
""",
    llm_config={"model": "gpt-4o"}
)
```

---

## Orchestration Logic

### Main Orchestrator Implementation

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from typing import Dict, Any, Optional
import json

class InvestigationOrchestrator:
    """
    Orchestrates the multi-agent investigation pipeline with validation loops.

    Architecture:
    - Sequential pipeline (Pattern A): Research → Analysis → Architecture → Documentation
    - Iterative validation (Pattern C): Each stage has validator with 3-5 rounds max
    """

    MAX_VALIDATION_ROUNDS = 5
    MIN_PASS_SCORE = 7.0

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._init_agents()
        self._init_validators()
        self.context = SharedContext()

    def _init_agents(self):
        """Initialize main agents."""
        self.researcher = self._create_researcher()
        self.analyst = self._create_analyst()
        self.architect = self._create_architect()
        self.writer = self._create_writer()

    def _init_validators(self):
        """Initialize validator agents."""
        self.research_validator = self._create_research_validator()
        self.analysis_validator = self._create_analysis_validator()
        self.architecture_validator = self._create_architecture_validator()
        self.documentation_validator = self._create_documentation_validator()

    async def investigate(self, topic: str) -> InvestigationResult:
        """
        Run full investigation pipeline.

        Flow:
        1. Research phase with validation loop
        2. Analysis phase with validation loop (receives research context)
        3. Architecture phase with validation loop (receives research + analysis)
        4. Documentation phase with validation loop (receives all prior context)
        """

        # Stage 1: Research with validation
        research_output = await self._run_validated_stage(
            agent=self.researcher,
            validator=self.research_validator,
            stage_name="Research",
            input_context={"topic": topic},
            accumulated_context={}
        )
        self.context.add("research", research_output)

        # Stage 2: Technical Analysis with validation
        analysis_output = await self._run_validated_stage(
            agent=self.analyst,
            validator=self.analysis_validator,
            stage_name="Technical Analysis",
            input_context={"topic": topic},
            accumulated_context={"research": research_output}
        )
        self.context.add("analysis", analysis_output)

        # Stage 3: Architecture Design with validation
        architecture_output = await self._run_validated_stage(
            agent=self.architect,
            validator=self.architecture_validator,
            stage_name="Architecture Design",
            input_context={"topic": topic},
            accumulated_context={
                "research": research_output,
                "analysis": analysis_output
            }
        )
        self.context.add("architecture", architecture_output)

        # Stage 4: Documentation with validation
        documentation_output = await self._run_validated_stage(
            agent=self.writer,
            validator=self.documentation_validator,
            stage_name="Documentation",
            input_context={"topic": topic},
            accumulated_context={
                "research": research_output,
                "analysis": analysis_output,
                "architecture": architecture_output
            }
        )

        return InvestigationResult(
            topic=topic,
            research=research_output,
            analysis=analysis_output,
            architecture=architecture_output,
            documentation=documentation_output,
            metadata=self.context.get_metadata()
        )

    async def _run_validated_stage(
        self,
        agent: AssistantAgent,
        validator: AssistantAgent,
        stage_name: str,
        input_context: Dict,
        accumulated_context: Dict
    ) -> StageOutput:
        """
        Run a single stage with validation loop.

        Pattern C Implementation:
        1. Agent produces output
        2. Validator reviews output
        3. If PASS: proceed to next stage
        4. If NEEDS_REVISION: agent revises based on feedback
        5. Repeat up to MAX_VALIDATION_ROUNDS times
        6. After max rounds: proceed with best effort + limitations noted
        """

        current_output = None
        validation_history = []

        for round_num in range(1, self.MAX_VALIDATION_ROUNDS + 1):

            # Build agent prompt with context
            agent_prompt = self._build_agent_prompt(
                stage_name=stage_name,
                input_context=input_context,
                accumulated_context=accumulated_context,
                previous_output=current_output,
                validation_feedback=validation_history[-1] if validation_history else None,
                round_num=round_num
            )

            # Agent generates/revises output
            current_output = await agent.generate(agent_prompt)

            # Validator reviews output
            validation_prompt = self._build_validation_prompt(
                stage_name=stage_name,
                agent_output=current_output,
                accumulated_context=accumulated_context,
                round_num=round_num,
                max_rounds=self.MAX_VALIDATION_ROUNDS
            )

            validation_result = await validator.generate(validation_prompt)
            validation_parsed = self._parse_validation(validation_result)
            validation_history.append(validation_parsed)

            # Log progress
            self._log_validation_round(stage_name, round_num, validation_parsed)

            # Check if passed
            if validation_parsed.decision == "PASS":
                return StageOutput(
                    content=current_output,
                    validation_rounds=round_num,
                    final_score=validation_parsed.score,
                    validation_history=validation_history
                )

        # Max rounds reached - proceed with limitations noted
        return StageOutput(
            content=current_output,
            validation_rounds=self.MAX_VALIDATION_ROUNDS,
            final_score=validation_history[-1].score,
            validation_history=validation_history,
            limitations=self._extract_remaining_issues(validation_history[-1])
        )

    def _build_agent_prompt(
        self,
        stage_name: str,
        input_context: Dict,
        accumulated_context: Dict,
        previous_output: Optional[str],
        validation_feedback: Optional[ValidationResult],
        round_num: int
    ) -> str:
        """Build prompt for agent including context and revision instructions."""

        prompt_parts = [f"# {stage_name} Task\n"]

        # Add topic
        prompt_parts.append(f"## Topic\n{input_context['topic']}\n")

        # Add accumulated context from prior stages
        if accumulated_context:
            prompt_parts.append("## Context from Prior Stages\n")
            for stage, output in accumulated_context.items():
                prompt_parts.append(f"### {stage.title()} Output\n{output.content}\n")

        # If revision round, add feedback
        if previous_output and validation_feedback:
            prompt_parts.append(f"""
## Revision Required (Round {round_num} of {self.MAX_VALIDATION_ROUNDS})

Your previous output received the following validation feedback:

### Validation Score: {validation_feedback.score}/10
### Decision: {validation_feedback.decision}

### Issues to Address:
{self._format_issues(validation_feedback.issues)}

### Specific Improvements Required:
{self._format_improvements(validation_feedback.improvements)}

Please revise your output addressing ALL the issues above.
Maintain what was working well while fixing the problems.
""")
        else:
            prompt_parts.append("\n## Instructions\nGenerate your output following your role specification.\n")

        return "\n".join(prompt_parts)
```

---

## Data Structures

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ValidationDecision(Enum):
    PASS = "PASS"
    NEEDS_REVISION = "NEEDS_REVISION"

@dataclass
class ValidationResult:
    decision: ValidationDecision
    score: float
    round_num: int
    scores_breakdown: Dict[str, float]
    issues: List[str]
    improvements: List[str]
    strengths: List[str]
    web_search_findings: Optional[List[Dict]] = None

@dataclass
class StageOutput:
    content: str
    validation_rounds: int
    final_score: float
    validation_history: List[ValidationResult]
    limitations: Optional[List[str]] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class InvestigationResult:
    topic: str
    research: StageOutput
    analysis: StageOutput
    architecture: StageOutput
    documentation: StageOutput
    metadata: Dict

    @property
    def total_validation_rounds(self) -> int:
        return (
            self.research.validation_rounds +
            self.analysis.validation_rounds +
            self.architecture.validation_rounds +
            self.documentation.validation_rounds
        )

    @property
    def average_quality_score(self) -> float:
        scores = [
            self.research.final_score,
            self.analysis.final_score,
            self.architecture.final_score,
            self.documentation.final_score
        ]
        return sum(scores) / len(scores)

class SharedContext:
    """Manages shared context between agents."""

    def __init__(self):
        self._stages: Dict[str, StageOutput] = {}
        self._metadata: Dict = {
            "start_time": datetime.now(),
            "events": []
        }

    def add(self, stage_name: str, output: StageOutput):
        self._stages[stage_name] = output
        self._metadata["events"].append({
            "type": "stage_complete",
            "stage": stage_name,
            "timestamp": datetime.now().isoformat(),
            "validation_rounds": output.validation_rounds,
            "score": output.final_score
        })

    def get(self, stage_name: str) -> Optional[StageOutput]:
        return self._stages.get(stage_name)

    def get_all(self) -> Dict[str, StageOutput]:
        return self._stages.copy()

    def get_metadata(self) -> Dict:
        self._metadata["end_time"] = datetime.now()
        self._metadata["duration_seconds"] = (
            self._metadata["end_time"] - self._metadata["start_time"]
        ).total_seconds()
        return self._metadata
```

---

## Tool Definitions

```python
from autogen import register_function
import httpx

# Web Search Tool (for Researcher, Architect, Architecture Validator)
@register_function
def web_search(query: str, num_results: int = 5) -> str:
    """
    Search the web for information.

    Args:
        query: Search query string
        num_results: Number of results to return (default 5)

    Returns:
        Formatted search results with titles, snippets, and URLs
    """
    # Implementation using Serper API or similar
    results = _execute_search(query, num_results)

    formatted = f"## Search Results for: {query}\n\n"
    for i, result in enumerate(results, 1):
        formatted += f"""### Result {i}
**Title:** {result['title']}
**URL:** {result['url']}
**Snippet:** {result['snippet']}

"""
    return formatted

# GitHub Code Search Tool (for Technical Analyst)
@register_function
def github_code_search(
    query: str,
    language: str = None,
    num_results: int = 5
) -> str:
    """
    Search GitHub for code examples.

    Args:
        query: Code search query
        language: Filter by programming language (optional)
        num_results: Number of results to return

    Returns:
        Code examples with repository info and snippets
    """
    results = _execute_github_code_search(query, language, num_results)

    formatted = f"## GitHub Code Search: {query}\n"
    if language:
        formatted += f"**Language:** {language}\n"
    formatted += "\n"

    for i, result in enumerate(results, 1):
        formatted += f"""### Result {i}: {result['repo']}
**File:** {result['path']}
**URL:** {result['url']}
```{result['language']}
{result['code_snippet']}
```

"""
    return formatted

# GitHub Repository Search Tool (for Technical Analyst)
@register_function
def github_repo_search(query: str, num_results: int = 5) -> str:
    """
    Search GitHub for repositories.

    Args:
        query: Repository search query
        num_results: Number of results to return

    Returns:
        Repository information including stars, description, and language
    """
    results = _execute_github_repo_search(query, num_results)

    formatted = f"## GitHub Repositories: {query}\n\n"
    for i, result in enumerate(results, 1):
        formatted += f"""### {i}. {result['full_name']}
**Stars:** {result['stars']} | **Language:** {result['language']}
**Description:** {result['description']}
**URL:** {result['url']}

"""
    return formatted

# Pattern Lookup Tool (for System Architect)
@register_function
def pattern_lookup(pattern_name: str) -> str:
    """
    Look up architectural pattern details.

    Args:
        pattern_name: Name of the pattern to look up

    Returns:
        Pattern description, use cases, pros/cons
    """
    # Could be backed by a patterns database or API
    pattern = _lookup_pattern(pattern_name)

    return f"""## Architectural Pattern: {pattern['name']}

**Category:** {pattern['category']}
**Also Known As:** {', '.join(pattern['aliases'])}

### Description
{pattern['description']}

### When to Use
{pattern['when_to_use']}

### Pros
{_format_list(pattern['pros'])}

### Cons
{_format_list(pattern['cons'])}

### Example
```
{pattern['example']}
```

### Related Patterns
{', '.join(pattern['related'])}
"""
```

---

## Configuration

```python
from pydantic_settings import BaseSettings
from typing import Optional

class AgentConfig(BaseSettings):
    """Configuration for the multi-agent investigation system."""

    # Model Configuration
    RESEARCH_MODEL: str = "gpt-4o-mini"
    ANALYSIS_MODEL: str = "gpt-4o-mini"
    ARCHITECT_MODEL: str = "gpt-4o"
    WRITER_MODEL: str = "gpt-4o"
    VALIDATOR_MODEL: str = "gpt-4o"

    # Validation Configuration
    MAX_VALIDATION_ROUNDS: int = 5
    MIN_PASS_SCORE: float = 7.0
    CRITICAL_CRITERIA_MIN: float = 7.0  # For security, feasibility

    # API Keys
    OPENAI_API_KEY: str
    SERPER_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None

    # Output Configuration
    OUTPUT_DIR: str = "outputs"
    LOG_DIR: str = "logs"
    VERBOSE: bool = True

    # Performance
    TIMEOUT_SECONDS: int = 300
    MAX_TOKENS_PER_AGENT: int = 8000

    class Config:
        env_file = ".env"
```

---

## Execution Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              COMPLETE EXECUTION FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

User Input: "Design a real-time notification system for a social media platform"

═══════════════════════════════════════════════════════════════════════════════════════════
STAGE 1: RESEARCH (Researcher ↔ Research Validator)
═══════════════════════════════════════════════════════════════════════════════════════════

Round 1:
┌─────────────┐     Output      ┌──────────────────┐
│ Researcher  │ ───────────────►│ Research         │
│ Agent       │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘   NEEDS_REVISION└──────────────────┘
                  Score: 6.5
                  Issues: Missing real-time patterns,
                         weak source diversity

Round 2:
┌─────────────┐     Revised     ┌──────────────────┐
│ Researcher  │ ───────────────►│ Research         │
│ Agent       │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘      PASS       └──────────────────┘
                  Score: 8.2

Output → Shared Context ["research"]

═══════════════════════════════════════════════════════════════════════════════════════════
STAGE 2: TECHNICAL ANALYSIS (Analyst ↔ Analysis Validator)
═══════════════════════════════════════════════════════════════════════════════════════════

Input: Topic + Research Output

Round 1:
┌─────────────┐     Output      ┌──────────────────┐
│ Technical   │ ───────────────►│ Analysis         │
│ Analyst     │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘      PASS       └──────────────────┘
                  Score: 7.8

Output → Shared Context ["research", "analysis"]

═══════════════════════════════════════════════════════════════════════════════════════════
STAGE 3: ARCHITECTURE (Architect ↔ Architecture Validator)
═══════════════════════════════════════════════════════════════════════════════════════════

Input: Topic + Research + Analysis

Round 1:
┌─────────────┐     Output      ┌──────────────────┐
│ System      │ ───────────────►│ Architecture     │
│ Architect   │ (web_search)    │ Validator        │
│             │◄─────────────── │ (web_search)     │
└─────────────┘   NEEDS_REVISION└──────────────────┘
                  Score: 6.8
                  Issues: Security model incomplete,
                         scaling strategy unclear

Round 2:
┌─────────────┐     Revised     ┌──────────────────┐
│ System      │ ───────────────►│ Architecture     │
│ Architect   │ (web_search)    │ Validator        │
│             │◄─────────────── │ (web_search)     │
└─────────────┘   NEEDS_REVISION└──────────────────┘
                  Score: 7.2
                  Issues: Message ordering guarantees
                         need clarification

Round 3:
┌─────────────┐     Revised     ┌──────────────────┐
│ System      │ ───────────────►│ Architecture     │
│ Architect   │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘      PASS       └──────────────────┘
                  Score: 8.5

Output → Shared Context ["research", "analysis", "architecture"]

═══════════════════════════════════════════════════════════════════════════════════════════
STAGE 4: DOCUMENTATION (Writer ↔ Documentation Validator)
═══════════════════════════════════════════════════════════════════════════════════════════

Input: Topic + Research + Analysis + Architecture

Round 1:
┌─────────────┐     Output      ┌──────────────────┐
│ Technical   │ ───────────────►│ Documentation    │
│ Writer      │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘   NEEDS_REVISION└──────────────────┘
                  Score: 7.0
                  Issues: Implementation guide
                         lacks code examples

Round 2:
┌─────────────┐     Revised     ┌──────────────────┐
│ Technical   │ ───────────────►│ Documentation    │
│ Writer      │                 │ Validator        │
│             │◄─────────────── │                  │
└─────────────┘      PASS       └──────────────────┘
                  Score: 8.8

═══════════════════════════════════════════════════════════════════════════════════════════
FINAL OUTPUT
═══════════════════════════════════════════════════════════════════════════════════════════

Investigation Complete:
- Topic: "Design a real-time notification system for a social media platform"
- Total Validation Rounds: 2 + 1 + 3 + 2 = 8
- Average Quality Score: (8.2 + 7.8 + 8.5 + 8.8) / 4 = 8.33
- Final Document: outputs/investigation_notification_system_20251224.md
```

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Set up project structure with MS AutoGen
- [ ] Implement configuration management (pydantic-settings)
- [ ] Create base agent classes with common functionality
- [ ] Implement SharedContext for cross-agent communication
- [ ] Set up logging infrastructure

### Phase 2: Core Agents
- [ ] Implement Researcher agent with web_search tool
- [ ] Implement Technical Analyst with GitHub tools
- [ ] Implement System Architect with web_search + pattern_lookup
- [ ] Implement Technical Writer

### Phase 3: Validators
- [ ] Implement Research Validator
- [ ] Implement Analysis Validator
- [ ] Implement Architecture Validator with web_search
- [ ] Implement Documentation Validator

### Phase 4: Orchestration
- [ ] Implement validation loop logic (_run_validated_stage)
- [ ] Implement context accumulation between stages
- [ ] Implement prompt building with revision feedback
- [ ] Add timeout and error handling

### Phase 5: Tools
- [ ] Implement web_search tool (Serper/DuckDuckGo)
- [ ] Implement github_code_search tool
- [ ] Implement github_repo_search tool
- [ ] Implement pattern_lookup tool

### Phase 6: Integration
- [ ] Create CLI entry point
- [ ] Create API endpoint (FastAPI)
- [ ] Create Gradio UI
- [ ] End-to-end testing

### Phase 7: Production Readiness
- [ ] Add comprehensive logging
- [ ] Implement cost tracking
- [ ] Add rate limiting
- [ ] Create monitoring dashboards
- [ ] Write deployment documentation

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | MS AutoGen | Native Python, flexible agent composition, good tool support |
| Validation Approach | Dedicated validators | Separation of concerns, specialized critique prompts |
| Max Rounds | 5 | Balance between quality and cost/time |
| Pass Threshold | 7.0 avg | High enough for quality, achievable in reasonable rounds |
| Web Search for Architect | Yes | Validates architectural decisions against current practices |
| Context Passing | Full prior outputs | Ensures each stage has complete information |
| Model Selection | GPT-4o for validation | Validators need strong reasoning for accurate assessment |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Average Quality Score | >= 8.0 | Mean of final validation scores |
| Validation Efficiency | <= 2.5 rounds/stage avg | Total rounds / 4 stages |
| User Satisfaction | >= 4.5/5 | Post-investigation survey |
| Factual Accuracy | >= 95% | Spot-check of claims |
| Cost per Investigation | <= $5 | Token usage * pricing |
| Time to Complete | <= 10 min | End-to-end duration |

---

## Appendix: MS AutoGen Quick Reference

```python
# Basic agent creation
from autogen import AssistantAgent, UserProxyAgent

agent = AssistantAgent(
    name="AgentName",
    system_message="Your role...",
    llm_config={
        "model": "gpt-4o",
        "temperature": 0.3,
        "max_tokens": 4000
    }
)

# Agent with tools
agent_with_tools = AssistantAgent(
    name="ToolAgent",
    system_message="...",
    llm_config={"model": "gpt-4o"},
    tools=[tool1, tool2]
)

# Two-agent conversation
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config=False
)

result = user_proxy.initiate_chat(
    agent,
    message="Your task..."
)

# Group chat (for more complex flows)
from autogen import GroupChat, GroupChatManager

group_chat = GroupChat(
    agents=[agent1, agent2, validator],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"model": "gpt-4o"}
)
```

---

*This specification provides a complete blueprint for implementing a production-grade multi-agent investigation system using Microsoft AutoGen with sequential execution and iterative validation.*
