---
name: context-compression
description: "Compresses context to fit within model token limits while preserving the most critical information for the task at hand."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Compression

Context compression is the process of reducing the size of textual context provided to a language model while retaining the information most essential to the task. As conversations grow longer and retrieved documents grow larger, compression becomes critical for staying within token limits and keeping inference costs manageable without sacrificing answer quality.

## Workflow

1. **Measure the Token Budget**: Determine the model's total context window and subtract the tokens reserved for instructions and output.
2. **Score Information Density**: Analyze raw context and assign density scores based on task-relevant facts.
3. **Select a Compression Strategy**: Choose between extractive/abstractive summarization, key-point extraction, or selective pruning.
4. **Apply Compression**: Execute the chosen strategy.
5. **Validate Information Retention**: Ensure no critical facts (entities, numbers, conclusions) were lost.
6. **Assemble the Final Context**: Insert the compressed text into the prompt.

## Techniques

- **Extractive Summarization**: Selects top-n important sentences verbatim. Best for precision.
- **Abstractive Summarization**: Rewrites content concisely. Risks subtle inaccuracies.
- **Key-Point Extraction**: Reduces text to facts/entities. High compression (>90%), loses narrative flow.
- **Selective Pruning**: Removes filler, boilerplate, and repetitions.
- **Token Budget Management**: Dynamically allocate budget across multiple context sources.

## Best Practices

- **Compress progressively**: Start with light pruning.
- **Preserve numbers and names**: Quantitative data is critical.
- **Tag compressed context**: Inform the model that context has been summarized.
- **Prefer extractive for code**: Avoid paraphrasing technical snippets.
- **Recency bias**: Keep the last 2-3 turns of conversation verbatim.
