# Reddit Sentiment and Bitcoin Price Correlation

## Contributors
- Ben Cooper (bc37) - responsible for data collection, data cleaning, preliminary analysis, and writing portions of the final report including the summary, data sections, and references.
- Steven Sanduski (ss206) - sentiment analysis, data merging and analysis, visualizations, findings, and writing about findings, future work, challenges, and reproducibility.

## Summary: [500-600 words] Description of your project, motivation, research question(s), and any findings.
The goal of this project is to ascertain whether social media sentiment surrounding Bitcoin has a measurable correlation with short-term Bitcoin price jumps. Cryptocurrency markets are widely considered as highly volatile and susceptible to public opinion, which Reddit serves as one of the most active platforms for investors and enthusiasts to discuss their public opinions on. By combining these two unique datasets (Reddit posts from r/Bitcoin and historical Bitcoin price data from Yahoo Finance), this project attempts to quantitavely assess whether a Reddit posts can predict or coincide with near-term Bitcoin price changes through data cleaning, data analysis, sentiment analysis, and hypothesis testing.

Our motivation for this project stems from our shared interest in financial markets and analyzing potential trends that can be used to predict markets. There is also growing support for the notion that social media activity influences financial markets such as in the case of GameStop's stock revival. Bitcoin, in constrast, lacks the fundamental financial statements that analysts often use to gauge prices, making it potentially more sensitive to investor sentiment. We felt Reddit’s r/Bitcoin subreddit, with its massive and highly engaged user base, thus served as a relevant and accurate proxy for the broader cryptocurrency public.

The project is guided by two specific research questions. The first is asks if the average daily sentiment score for r/Bitcoin posts correlate with Bitcoin’s closing price change within a 1–3 day window? The second asks do posts with upvote scores above the 75th percentile have a stronger correlation with next-day Bitcoin price movements than lower-engagement posts? These were questions that we refined and adjusted based off initial feedback to narrow in our broader initial framings to specific questions that can be answered through quantitative analysis.

To answer these questions, Reddit post data was collected from their archive API covering January 2024 through January 2026, yielding approximately 2,000 posts. Bitcoin daily price data for the same period was retrieved via the yfinance library using Yahoo Finance as the underlying source, producing over 700 daily observations. After cleaning both datasets, VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis was applied to each post title to generate a compound sentiment score ranging from -1 (most negative) to +1 (most positive). Daily average sentiment scores were then computed and merged with the corresponding daily Bitcoin price metrics to form an integrated dataset suitable for correlation analysis.

[PLACEHOLDER – Findings summary to be added once correlation analysis and visualizations are complete. Update this paragraph with a 2–3 sentence summary of the key numeric results and whether the research questions were supported or refuted.]




## Data profile: [max2000 words] For each dataset used, describe its structure, content, and characteristics. Specify the location of the dataset files in your project repository. Discuss any ethical or legal constraints associated with the data and explain how the datasets relate to your questions
## Data quality: [500-1000 words] Summary of the quality assessment.
## Data cleaning: [max 1000 words] Summarize the data cleaning operations you performed and explain how each operation addressed specific data quality issues in your datasets.
## Findings: [~500 words] Description of any findings including numeric results and/or visualizations.
## Future work: [~500-1000 words] Brief discussion of any lessons learned and potential future work.
## Challenges: [~500 words] Discuss the main challenges you encountered while working on the project.
## Reproducing: Sequence of steps required for someone else to reproduce your results.
## References: Formatted citations for any papers, datasets, or software used in your project.
