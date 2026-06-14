# Prompt Engineering Rationale

## Design Philosophy
The system's prompts are engineered to guide the LLM through a structured, multi-step reasoning process. This approach, known as **Chain-of-Thought (CoT)**, improves the model's ability to identify complex architectural threats and maintain strict grounding.

## Prompt Structure

### 1. Analytical Process (Think Aloud)
The model is first instructed to perform an internal analysis of assets, data flows, and identity boundaries. This "mental mapping" ensures the model understands the system's architecture before it starts generating threats.

### 2. High-Recall Resource Catalog
By injecting specific checklists for common resources (e.g., S3, IAM), we provide the model with "domain-specific heuristics." This mitigates the model's tendency to forget subtle misconfigurations in favor of more obvious ones.

### 3. Strict Output Contract
The prompt enforces a rigid JSON schema and component naming convention. By requiring the model to use the exact Terraform identifier (`resource_type.resource_name`), we enable automated post-processing validation and eliminate a primary source of hallucinations.

### 4. Mandatory Minimums
To combat LLM "laziness," the prompt specifies mandatory minimum threat counts based on infrastructure complexity. This forces the model to stay engaged with the problem until a thorough analysis is complete.

## Evolution of the Multi-Source Prompt

| Version | Focus | Result |
| :--- | :--- | :--- |
| **v0.1.0** | Basic Grounding | ~4% Precision, high hallucinations. |
| **v0.2.0** | Heuristic Ranking | ~37% Precision, reduced noise. |
| **v0.3.0** | Matrix Reasoning | ~57% Precision, ~46% Recall. |
| **v0.4.0** | Catalog + CoT | **Target: 50%+ Precision, 50%+ Recall.** |

## Handling Non-Determinism
By setting the temperature to `0.0` and using structured instructions, we maximize the reproducibility of the threat models. This ensures that the tool is suitable for professional security auditing where consistency is paramount.
