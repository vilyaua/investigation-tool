"""Task definitions for the MCP investigation workflow."""

from crewai import Task
from crewai import Agent


def create_mcp_research_task(agent: Agent, topic: str) -> Task:
    """
    Create the MCP research task.

    Args:
        agent: The MCP Research Agent
        topic: Investigation topic (e.g., "web scraping MCP tool")

    Returns:
        Configured Task instance
    """
    return Task(
        description=f"""Research the Model Context Protocol (MCP) in the context of: {topic}

Your research should cover:
1. **MCP Overview**: Core concepts, architecture, and how MCP works
2. **Relevant MCP Tools**: Existing MCP tools related to {topic}
3. **MCP Patterns**: Common patterns and best practices for building MCP tools
4. **Integration Examples**: How MCP tools integrate with LLM applications
5. **Official Documentation**: Links to official MCP specs and resources
6. **Community Resources**: Tutorials, blog posts, and community implementations

Focus on:
- Official MCP documentation from Anthropic
- Real-world implementations
- Best practices and patterns
- Recent developments (2024-2025)

Cite all sources with URLs.""",
        expected_output="""A comprehensive research report in markdown format with:

# MCP Research Report: {topic}

## 1. MCP Protocol Overview
- Brief explanation of MCP
- Key concepts and architecture
- Why MCP matters for {topic}

## 2. Existing MCP Tools
- List of relevant MCP tools
- Brief description of each
- Links to repositories/documentation

## 3. Common Patterns
- Architectural patterns for MCP tools
- Best practices
- Common pitfalls to avoid

## 4. Integration Approaches
- How MCP tools connect to LLMs
- Example integration patterns
- Client-server architecture

## 5. Resources
- Official documentation links
- Community resources
- Example repositories

All sections should include relevant URLs and citations.""",
        agent=agent
    )


def create_technical_analysis_task(agent: Agent, topic: str, context: list) -> Task:
    """
    Create the technical analysis task.

    Args:
        agent: The Technical Research Agent
        topic: Investigation topic
        context: Previous task outputs for context

    Returns:
        Configured Task instance
    """
    return Task(
        description=f"""Analyze code examples and implementation patterns for MCP tools related to: {topic}

Using the context from the research phase, your analysis should:
1. **Find Code Examples**: Search GitHub for relevant MCP tool implementations
2. **Analyze Patterns**: Identify common architectural and code patterns
3. **Extract Insights**: What makes a good MCP tool implementation?
4. **Identify Trade-offs**: Pros/cons of different implementation approaches
5. **Security & Performance**: Any security or performance considerations

Focus on:
- Real production code (not toy examples)
- Well-maintained repositories
- Code quality and patterns
- Practical implementation details

Provide specific code examples where relevant.""",
        expected_output="""A technical analysis report in markdown format with:

# Technical Analysis: {topic}

## 1. Code Examples Found
- Repository links
- Brief description of each
- Stars/activity metrics

## 2. Implementation Patterns
- Common architectural patterns observed
- Code structure and organization
- Key design decisions

## 3. Code Quality Insights
- Best practices observed
- Common mistakes to avoid
- Code examples (with attribution)

## 4. Technical Trade-offs
- Different approaches and their pros/cons
- Performance considerations
- Complexity vs. functionality

## 5. Key Takeaways
- Most important technical insights
- Recommended approaches
- Things to watch out for

Include code snippets where helpful (with proper attribution).""",
        agent=agent,
        context=context
    )


def create_architecture_design_task(agent: Agent, topic: str, context: list) -> Task:
    """
    Create the architecture design task.

    Args:
        agent: The Architecture Analyst Agent
        topic: Investigation topic
        context: Previous task outputs for context

    Returns:
        Configured Task instance
    """
    return Task(
        description=f"""Design an optimal MCP tool architecture for: {topic}

Based on the research and technical analysis, create a comprehensive architecture design that:
1. **Synthesizes Findings**: Combine insights from research and code analysis
2. **Proposes Architecture**: Design a production-ready MCP tool architecture
3. **Justifies Decisions**: Explain why each architectural choice was made
4. **Addresses Trade-offs**: Discuss alternatives and why they were not chosen
5. **Provides Roadmap**: Outline implementation phases

Consider:
- Scalability and performance
- Maintainability and developer experience
- Security and reliability
- Cost and operational complexity
- Future extensibility

Your architecture should be practical and implementable.""",
        expected_output="""An architecture design document in markdown format with:

# Architecture Design: MCP Tool for {topic}

## 1. Executive Summary
- Problem statement
- Proposed solution (1-2 paragraphs)
- Key architectural decisions

## 2. System Architecture
- High-level architecture diagram (ASCII art)
- Component breakdown
- Data flow
- MCP integration points

## 3. Key Components
For each major component:
- Purpose and responsibilities
- Technology choices
- Implementation approach

## 4. Design Decisions
For each major decision:
- What was decided
- Why (rationale)
- What alternatives were considered
- Trade-offs

## 5. Integration Architecture
- How components interact
- MCP client-server setup
- LLM integration approach

## 6. Non-Functional Considerations
- Scalability approach
- Security measures
- Performance optimization
- Error handling and resilience

## 7. Implementation Roadmap
- Phase 1: MVP
- Phase 2: Enhanced features
- Phase 3: Production hardening

## 8. Risks and Mitigations
- Potential risks
- Mitigation strategies""",
        agent=agent,
        context=context
    )


def create_documentation_task(agent: Agent, topic: str, context: list) -> Task:
    """
    Create the final documentation task.

    Args:
        agent: The Technical Writer Agent
        topic: Investigation topic
        context: Previous task outputs for context

    Returns:
        Configured Task instance
    """
    return Task(
        description=f"""Create comprehensive technical documentation for the MCP tool architecture for: {topic}

Synthesize all previous findings into a clear, actionable final report that:
1. **Summarizes**: Key findings from research, analysis, and architecture design
2. **Documents**: The proposed architecture in detail
3. **Guides**: Provides implementation guidance
4. **Exemplifies**: Includes concrete code examples
5. **Recommends**: Clear next steps for implementation

The documentation should be:
- Clear and well-structured
- Actionable (developers can use it to build the tool)
- Complete (covers all aspects)
- Professional (suitable for technical review)

Target audience: Senior engineers and architects who will implement this.""",
        expected_output="""A comprehensive final report in markdown format with:

# MCP Tool Architecture Investigation: {topic}

## Executive Summary
- Problem and opportunity
- Recommended solution
- Key benefits
- Implementation timeline

## 1. Background
- What is MCP
- Why MCP for {topic}
- Current landscape

## 2. Research Findings
- Key insights from MCP ecosystem
- Existing tools and patterns
- Best practices

## 3. Technical Analysis
- Code patterns analyzed
- Implementation approaches
- Trade-offs identified

## 4. Proposed Architecture
- System design
- Component details
- Integration approach
- ASCII diagrams where helpful

## 5. Implementation Guide
- Step-by-step approach
- Technology stack
- Code structure
- Example code snippets

## 6. Code Examples
```python
# Example MCP server setup
# ... (complete, runnable examples)
```

## 7. Deployment & Operations
- Deployment approach
- Monitoring and observability
- Scaling considerations

## 8. Risks & Mitigations
- Identified risks
- Mitigation strategies

## 9. Next Steps
- Immediate actions
- Phase 1 deliverables
- Success metrics

## 10. Resources
- Official documentation
- Example repositories
- Further reading

---

The report should be complete, professional, and immediately actionable.""",
        agent=agent,
        context=context
    )
