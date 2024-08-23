SYSTEM_PROMPT = """
You are an expect python coder and debugger.
Allowed imports: pandas as pd, matplotlib.pyplot as plt, numpy as np, datetime
"""

DATAFRAME_PROMPT_PREFIX = """
You are working with {n_dataframes} pandas dataframe in Python.
Their names, the file name from which they were imported and a few rows from them are provided below in order.
"""

DATAFRAME_PROMPT = """
The dataframe number {i}: It is imported from file: {filename}.
The name of the dataframe in the global environment is df{num} .
The first few rows of the dataframe are as follows:
{df_head}
"""
USER_PROMPT_SUFFIX = """
{previous_conversation_history}

Based on the above information about the dataframes, answer the following user query. When addressing queries related to supplier consolidation and tail spend analysis, follow these guidelines:

1. Tail Spend Analysis:
   a. List suppliers and their total spend.
   b. Order suppliers from highest to lowest total spend.
   c. Determine the cutoff point (typically 80% of total spend).
   d. Identify main suppliers (those within the 80% spend) and tail spend suppliers (those in the remaining 20%).
   e. Calculate total tail spend.

2. Supplier Consolidation:
   a. Calculate a SupplierScore for each supplier using the formula:
      SupplierScore = (0.25 * Rating) + (0.15 / AvgDeliveryTime) + (0.1 * ReliabilityScore) + (0.5 * (TotalSpend / CumulativeSpend))
   b. Normalize SupplierScore to a 1-10 range using min-max scaling.
   c. For category-wide consolidation:
      - Rank suppliers based on their SupplierScore within each category.
      - Select the top 3-5 suppliers with the highest SupplierScore as consolidated suppliers for that category.
   d. For item-level consolidation:
      - Rank suppliers for each item based on their SupplierScore.
      - Select the top supplier for each item.

3. Reporting:
   a. For tail spend analysis, report:
      - List of main suppliers and their total spend
      - List of tail spend suppliers and their total spend
      - Total tail spend amount and percentage
   b. For consolidation, report:
      - List of consolidated suppliers (either by category or by item, as requested)
      - Their SupplierScores
      - Potential savings or benefits of consolidation

4. Additional Considerations:
   - Consider geographical distribution of suppliers for risk assessment.
   - Analyze the impact of consolidation on supply chain resilience.
   - Suggest strategies for managing relationships with non-consolidated suppliers.

When answering queries, provide a step-by-step explanation of your analysis process, include relevant code snippets, and summarize key findings and recommendations.

Query: {query}
"""

USER_PROMPT_SUFFIX_DEBUGGING = """
For the query: {query}, the following python code was generated
{python_code}
This yielded the following error:
{error}

Your task is to correct the code and explain the changes made.
"""

USER_PROMPT_SUFFIX_DEBUGGING = """
For the query: {query},
the following python code was generated
{python_code}
This yielded the following error.
{error}

Your task is to correct the code.
"""