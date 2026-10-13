# 01-LLM-RAG-Benchmarking

## Overview

This project evaluates the performance and cost-efficiency of Large Language Models (LLMs) used within a Retrieval-Augmented Generation (RAG) pipeline for scientific question answering.

The study evaluates different combinations of LLMs for information retrieval and answer generation across two biological literature datasets: bee toxicology (MetaBeeAI) and primate welfare. Model configurations were compared using retrieval quality, answer quality, and inference cost to investigate whether higher-performing configurations justify their additional computational cost.

This work was completed as part of my MSc Artificial Intelligence in Biosciences dissertation at Queen Mary University of London.


## Objectives

The project investigated:

- How LLM choice affects retrieval and generated-answer quality in a scientific RAG pipeline.

- Whether different combinations of retrieval and answer models produce different levels of performance.

- The trade-off between model performance and inference cost.

- Whether model rankings remain consistent across different biological domains.

- Whether model performance varies between different scientific question types.


## RAG Pipeline

The system separates the question-answering process into two main stages:

1. Retrieval — An LLM evaluates text chunks extracted from scientific literature and identifies information relevant to the question.

2. Answer generation — A second LLM uses the retrieved context to generate the final answer.

The overall workflow is:

___________________________

Scientific Literature → Text Chunks → Retrieval Model → Relevant Context → Answer Model → Generated Answer → Evaluation
___________________________


## Datasets

### 1. MetaBeeAI — Bee Toxicology

The first benchmark evaluated scientific question answering using literature relating to bee toxicology.

Three question categories were examined:

- Bee species

- Pesticides

- Additional stressors

The additional-stressors questions also provided an abstention-style challenge, where relevant information may not be available in the source material.

Six LLMs with complete experimental coverage were compared, including models from OpenAI, Mistral, Google, and Meta.

The three models selected from this benchmark for further evaluation were:

1. GPT-4o-mini

2. Mistral-Large-2512

3. Gemini-3.1-Flash-Lite



### 2. Primate Welfare

The second benchmark tested whether findings from MetaBeeAI transferred to a different biological domain.

The dataset contained scientific literature addressing:

1. Study design

2. Study population

3. Animal welfare

The three selected LLMs were evaluated in a 3 × 3 retrieval–answer configuration, producing nine possible model pairings.



## Evaluation Metrics

Five complementary metrics were used to evaluate different stages of the RAG pipeline.

Pipeline component                    Metric                    Purpose

Retrieval                      Contextual Precision            Measures whether relevant information is prioritised within retrieved context

Retrieval                      Contextual Recall               Measures whether the required information was successfully retrieved

Generation                     Faithfulness                    Measures whether generated claims are supported by retrieved context

Generation                     G-Eval Accuracy                 Measures factual correctness against reference answers

Generation                     G-Eval Completeness             Measures whether the generated response contains the required information


A combined quality score was calculated to provide an overall measure of pipeline performance.
____________________
Combined Quality =
0.30 × Faithfulness
+ 0.15 × Contextual Precision
+ 0.15 × Contextual Recall
+ 0.20 × Completeness
+ 0.20 × Accuracy
_____________________

Inference costs were calculated separately for the retrieval and answer stages using token consumption and model-specific API pricing.


## Key Results

### MetaBeeAI Benchmark

GPT-4o achieved the highest overall combined quality among the six models evaluated.

Performance also varied substantially between question types. Bee-species questions produced the strongest overall performance, while additional-stressor questions were particularly challenging because they tested whether models could correctly recognise when relevant information was absent.

![MetaBeeAI Model Performance](figure/metabeeai/overall_metabeeai_performance.png)

### Primate Welfare Benchmark

Across the nine retrieval–answer combinations, Mistral-Large retrieval + Mistral-Large answer generation achieved the highest mean combined quality score of approximately 0.812.

However, near-optimal performance could be achieved at lower inference cost. GPT-4o-mini retrieval + Mistral-Large answer generation achieved a mean combined quality of approximately 0.806, representing about 99.3% of the best-performing configuration's quality while reducing mean pipeline cost by approximately 35.6%.

![Primate Welfare Cost Performance](figure/primate_welfare/overall_primate_welfare_performance.png)

This demonstrates that selecting different models for retrieval and answer generation can provide a more favourable cost–performance trade-off than simply using the highest-performing model for both stages.

## Cross-Domain Performance

The same-model configurations evaluated across both datasets maintained the same relative ranking between MetaBeeAI and Primate Welfare.

However, absolute performance was lower on the Primate Welfare dataset for all three models.

These results suggest that relative model performance may transfer between biological domains, while absolute performance remains dependent on the characteristics of the scientific literature and questions being evaluated.

## Statistical Analysis

The relationship between inference cost and combined quality was evaluated using Spearman's rank correlation and linear regression.

For the Primate Welfare benchmark, model cost showed a strong positive association with performance:


Spearman's ρ = 0.900

p < 0.001

R² = 0.785


The relationship was weaker in the MetaBeeAI benchmark, suggesting that increasing model cost does not produce the same performance gains across every dataset.

## Key Takeaways

This project demonstrates that RAG performance depends on the interaction between retrieval and answer-generation models rather than solely on the choice of a single LLM.

The experiments also highlight an important practical trade-off: the configuration producing the highest absolute quality is not necessarily the most attractive choice when inference cost is considered. Near-optimal performance can sometimes be achieved using a less expensive retrieval model paired with a stronger answer-generation model.

More broadly, the cross-domain evaluation shows the importance of benchmarking RAG configurations on domain-specific scientific data rather than assuming that performance will transfer unchanged between domains.
