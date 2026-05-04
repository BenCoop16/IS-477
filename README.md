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
**First Dataset: Reddit r/Bitcoin Posts**
The first of our datasets consists of posts acquired from the r/Bitcoin subreddit on Reddit. The API on Reddit takes a few days to access the data, so instead we used The Arctic Shift Reddit Archive API (https://arctic-shift.photon-reddit.com/api/posts/search), a free and openly accessible archive that does not require API key approval, making it the best alternative to official Reddit API's lengthy individual access process. We loaded the data using the code:
all_posts = []
batch_after = "2024-01-01"
batch_before = "2026-01-01"
url = "https://arctic-shift.photon-reddit.com/api/posts/search"

for i in range(20):
    params = {"subreddit": "Bitcoin", "after": batch_after, "before": batch_before, "limit": 100, "sort": "asc"}
    response = requests.get(url, params=params)
    posts = response.json()
    batch = posts['data']
    if not batch:
        print(f"No more data at batch {i}")
        break
    all_posts.extend(batch)
    batch_after = batch[-1]['created_utc']
    print(f"Batch {i+1}: {len(batch)} posts, total so far: {len(all_posts)}")
    time.sleep(1)

df_bitcoin = pd.DataFrame(all_posts)[['id', 'title', 'selftext', 'score', 'upvote_ratio', 'num_comments', 'created_utc', 'subreddit']]
df_bitcoin['timestamp'] = pd.to_datetime(df_bitcoin['created_utc'], unit='s')
print(df_bitcoin.shape)
This essentially solves the problem with Arctic Shift's batch limit of 100 Reddit posts at a time by doing a for loop of 20 instances to create a dataframe of 2000 individual subreddit posts from 2024 to 2026. In the end, it creates a dataframe with 2,000 rows of data that should mirror the csv file on github under the name "reddit_bitcoin_raw.csv". This data spans January 1, 2024 through January 1, 2026, with posts retrieved in batches of 100 per request (again, the maximum allowed by the Arctic Shift API). While the raw data is stored in the project repository as reddit_bitcoin_raw.csv, the cleaned version is storedn as reddit_bitcoin_clean.csv in the repository as well.
The dataset is structured as a flat table where each row represents a single Reddit post. The columns retained from the API response are: id (unique post identifier), title (the post headline, used as the primary text for sentiment analysis), selftext (the full body text of the post), score (the net upvote count, i.e. upvotes minus downvotes), upvote_ratio (the proportion of votes that were upvotes, as a float between 0 and 1), num_comments (the number of comments the post received), subreddit (always “bitcoin” for this dataset), and timestamp (the UTC datetime of post creation, converted from the Unix epoch field created_utc).
In terms of ethical and legal considerations, all data in this dataset is publicly posted content from a public subreddit and was accessed through a public archive with no authentication required. Reddit’s publicly accessible posts are generally considered suitable for academic and non-commercial research. However, the data does contain usernames and personally identifiable information in post text in some cases, which is why this project restricts its analysis to the title field and aggregate engagement metrics rather than individual-level content. No private messages, user profiles, or restricted subreddit content were accessed. Additionally, while the data is publicly available, researchers using Reddit data should remain cognizant of the platform’s terms of service, which prohibit certain commercial uses of scraped data.
This dataset directly supports both research questions. The title field is the input for VADER sentiment scoring, while the score and upvote_ratio fields allow segmentation of posts by engagement level, which is necessary for answering the second research question about whether high-upvote posts correlate more strongly with price movements.

**Second Dataset: Bitcoin Historical Price**
The second dataset contains historical daily price and volume data for Bitcoin (BTC-USD) sourced from Yahoo Finance via the yfinance Python library. Data was retrieved for the same time window as the Reddit dataset: January 1, 2024 through January 1, 2026. This produced over 700 daily observations. It was uploaded with the following code:

In the Github repository, the raw data is stored as crypto_prices_raw.csv and the cleaned version as crypto_prices_clean.csv in the project repository. The dataset is structured as a time-series table where each row represents one calendar day of bitcoin price fluctuations. After cleaning and renaming, the columns become: date (the trading date, changed/formatted to datetime format), open (the opening price in USD which is what price Bitcoin was at when the markets opened), high (the daily high price in USD), low (the daily low price in USD), close (the closing price in USD, which is the price of Bitcoin when markets closed), and volume (the total trading volume for the day in USD). The close price is the primary metric we used for the correlation analysis, as it represents the final agreed-upon market price for each day and is normally the accepted standard measure for financial research as it represents a financial asset's daily price fluctuations.
Yahoo Finance data accessed via yfinance is freely available for non-commercial and research purposes. The data itself reflects publicly traded market prices and is not subject to copyright in the same way as original creative works. There are no significant ethical constraints associated with this dataset. One consideration is that yfinance is an unofficial third-party wrapper, meaning the underlying data source (Yahoo Finance) could change its API structure or terms of service at any time, and the dataset should be treated as a snapshot of the data as it existed at collection time rather than a permanently stable source.
This dataset is the price-side component of the project. The daily close price and price-to-price change metrics are what the sentiment scores are ultimately compared against to evaluate correlation. The shared timestamp structure – both datasets cover the same two-year window with daily granularity – is what makes integration possible.



## Data quality: [500-1000 words] Summary of the quality assessment.
## Data cleaning: [max 1000 words] Summarize the data cleaning operations you performed and explain how each operation addressed specific data quality issues in your datasets.
## Findings: [~500 words] Description of any findings including numeric results and/or visualizations.
## Future work: [~500-1000 words] Brief discussion of any lessons learned and potential future work.
## Challenges: [~500 words] Discuss the main challenges you encountered while working on the project.
## Reproducing: Sequence of steps required for someone else to reproduce your results.

## References: Formatted citations for any papers, datasets, or software used in your project.
- Arctic Shift. (2024). Arctic Shift Reddit Archive API. Retrieved from https://arctic-shift.photon-reddit.com/api/posts/search
- Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. Proceedings of the Eighth International AAAI Conference on Weblogs and Social Media.
- McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 51–56. [pandas library]
- Ran, J. (2019). yfinance: Yahoo! Finance market data downloader [Python library]. Retrieved from https://pypi.org/project/yfinance/
Reddit. (2024). r/Bitcoin subreddit [Public forum data archived via Arctic Shift]. Reddit, Inc.
- Yahoo Finance. (2024). Bitcoin USD (BTC-USD) historical data [Dataset]. Retrieved via yfinance Python library.
