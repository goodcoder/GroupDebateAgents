# Multi-Agent Planner-Critic Frameworks

The "Planner-Critic" (or Actor-Critic / Generator-Reviewer) pattern is a highly effective architecture in multi-agent systems. In this pattern, one agent (the Planner/Actor) drafts a plan or creates a solution, while another agent (the Critic/Reviewer) evaluates it, asks probing questions, and forces the first agent to iteratively refine the output.

Here are the top 10 multi-agent AI frameworks used today that support this pattern, with a brief introduction for each:

### 1. LangGraph (by LangChain)
LangGraph treats agents as nodes in a graph and is specifically designed to handle cyclical workflows. It is currently the most popular choice for building explicit Planner-Critic loops, as you can easily wire a "Drafting Node" to loop into a "Critique Node" until a specific quality condition is met to break the cycle.

### 2. Microsoft AutoGen
AutoGen facilitates multi-agent conversations out of the box. You can define a `PlannerAgent` with a prompt to generate strategies, and a `CriticAgent` instructed to find flaws and ask challenging questions. Utilizing its `GroupChat` feature, the agents will organically debate and refine the plan until a consensus is reached.

### 3. CrewAI
CrewAI focuses on role-playing agents (called a "crew") working together. It is very straightforward to assign one agent the role of `Strategic Planner` and another the role of `Strict Reviewer`. A `Manager` agent can oversee their dialogue, forcing the planner to answer the reviewer's questions before the task is marked complete.

### 4. MetaGPT
MetaGPT simulates an entire software company using Standard Operating Procedures (SOPs). It natively incorporates the Critic pattern by having dedicated roles like `Product Manager` (who plans) and `Reviewer` or `QA Engineer` (who critiques). The framework mandates that outputs pass the reviewer's checks before moving down the pipeline.

### 5. ChatDev
Similar to MetaGPT, ChatDev is an open-source framework where agents play distinct corporate roles. It inherently relies on a proposer-reviewer dynamic (e.g., `Programmer` proposes code, `Code Reviewer` challenges it), making it a great out-of-the-box solution for review-heavy workflows.

### 6. LlamaIndex (Workflows)
Originally a RAG framework, LlamaIndex now features robust Agentic Workflows. It allows you to build sophisticated asynchronous workflows where a Planning Agent generates a step-by-step query or action plan, and an Evaluator Agent reviews the plan's validity against the source data before execution.

### 7. Microsoft Semantic Kernel
Semantic Kernel natively features "Planners" that automatically orchestrate plugins to achieve a user's goal. Developers frequently wrap this planner with an evaluation step, using a secondary "Critic" prompt or agent to validate the generated plan's safety and logic before it is allowed to execute.

### 8. Agency Swarm
Agency Swarm is built around the concept of hierarchical agent agencies. You can create a "CEO" agent that acts as the critic/reviewer, overseeing a "Planner" agent. The framework heavily relies on tools and structured inter-agent communication, mimicking real-world managerial review processes.

### 9. Camel-AI
CAMEL (Communicative Agents for "Mind" Exploration of Large Language Model Society) is a framework focused on role-playing. It utilizes "inception prompting" to align two agents (e.g., an AI User and an AI Assistant) to collaborate on a task, which easily translates to an AI Planner proposing ideas and an AI Critic verifying them.

### 10. Swarms
Swarms is an enterprise-grade orchestration framework designed for massive multi-agent deployment. It supports a variety of architectures, including standard hierarchical structures where a Director agent criticizes and refines the execution plans of subordinate worker agents.
