# Reddit Sentiment and Bitcoin Price Correlation

## Contributors
- Ben Cooper (bc37) - responsible for data collection, data cleaning, preliminary analysis, and writing portions of the final report including the summary, data sections, and references.
- Steven Sanduski (ss206) - sentiment analysis, data merging and analysis, visualizations, findings, and writing about findings, future work, challenges, and reproducibility.

## Summary
The goal of this project is to ascertain whether social media sentiment surrounding Bitcoin has a measurable correlation with short-term Bitcoin price jumps. Cryptocurrency markets are widely considered as highly volatile and susceptible to public opinion, where Reddit serves as one of the most active platforms for investors and enthusiasts to discuss their public opinions on. By combining these two unique datasets (Reddit posts from r/Bitcoin and historical Bitcoin price data from Yahoo Finance), this project attempts to quantitavely assess whether a Reddit posts can predict or coincide with near-term Bitcoin price changes through data cleaning, data analysis, sentiment analysis, and hypothesis testing.

Our motivation for this project stems from our shared interest in financial markets and analyzing potential trends that can be used to predict markets. There is also growing support for the notion that social media activity influences financial markets such as in the case of GameStop's stock revival. Bitcoin, in constrast, lacks the fundamental financial statements that analysts often use to gauge prices, making it potentially more sensitive to investor sentiment. We felt Reddit’s r/Bitcoin subreddit, with its massive and highly engaged user base, thus served as a relevant and accurate proxy for the broader cryptocurrency public.

The project is guided by two specific research questions. The first is asks if the average weekly sentiment score for r/Bitcoin posts correlate with Bitcoin’s closing price changes throughout the next 1-3 weeks? The second asks do posts with upvote scores above the 75th percentile have a stronger correlation with future Bitcoin price movements than lower-engagement posts? These were questions that we refined and adjusted based off initial feedback to narrow in our broader initial framings to specific questions that can be answered through quantitative analysis.

To answer these questions, Reddit post data was collected from their archive API covering January 2024 through January 2026, yielding approximately 3,000 posts. Bitcoin weekly price data for the same period was retrieved via the yfinance library using Yahoo Finance as the underlying source, producing over 100 weekly price observations. After cleaning both datasets, sentiment analysis was applied to each post title to generate a compound sentiment score ranging from -1 (most negative) to +1 (most positive). Weekly average sentiment scores were then computed and merged with the corresponding weekly Bitcoin price metrics to form an integrated dataset suitable for correlation analysis.

Using linear regression, we found no statistically significant relationship between weekly r/Bitcoin sentiment and Bitcoin's price movement at any level of post engagement. For RQ1, sentiment showed a near-zero correlation with next-week price change (r = -0.0976, p = 0.3244), and for RQ2, splitting by upvote score above the 75th percentile produced a slightly stronger but still non-significant result (r = -0.2167, p = 0.2982), suggesting that Reddit sentiment alone does not reliably predict short-term Bitcoin price movement in this dataset.

## Data Profile
**First Dataset: Reddit r/Bitcoin Posts**
The first of our datasets consists of posts acquired from the r/Bitcoin subreddit on Reddit. The API on Reddit takes a few days to access the data, so instead we used The Arctic Shift Reddit Archive API (https://arctic-shift.photon-reddit.com/api/posts/search), a free and openly accessible archive that does not require API key approval, making it the best alternative to official Reddit API's lengthy individual access process. Data was then accessed using a weekly loop that spanned January 1st 2024 to January 1st 2026, pulling 30 posts a week:

all_posts = []

start_date = datetime(2024, 1, 1)

end_date = datetime(2026, 1, 1)

posts_per_week = 30

current = start_date

while current < end_date:

next_week = current + timedelta(weeks = 1)

params = {

"subreddit": "Bitcoin",

"after": current.strftime("%Y-%m-%d"),

"before": next_week.strftime("%Y-%m-%d"),

"limit": posts_per_week,

"sort": "asc"

}

response = requests.get("https://arctic-shift.photon-reddit.com/api/posts/search", params = params)

batch = response.json().get('data') or []

if batch:

all_posts.extend(batch)

current = next_week

time.sleep(0.5)

This approach collects posts week by week across the full two-year window, yielding approximately 3,000 posts total. The raw data is stored in the project repository as reddit_bitcoin_raw-2.csv and the cleaned/merged version with bitcoin prices as reddit_btc_merged.csv.  
The dataset is structured as a flat table where each row represents a single Reddit post. The columns, directly imported from the Arctic Shift API, are: id (unique post identifier), title (the post headline, used as the primary text for sentiment analysis), selftext (the full body text of the post), score (the net upvote count), upvote_ratio (the proportion of votes that were upvotes, as a float between 0 and 1), num_comments (the number of comments the post received), subreddit (always "Bitcoin" for this dataset), and timestamp (the UTC datetime of post creation, converted from the created_utc field).
In terms of ethical and legal considerations, all data in this dataset consists of publicly posted content from a public subreddit, accessed through a public archive with no authentication required. This project restricts its analysis to the title field and aggregate engagement metrics rather than individual-level content, avoiding any focus on specific users or personal information. No private messages, user profiles, or restricted subreddit content were accessed. Researchers using Reddit data should remain aware of the platform's terms of service, which prohibit certain commercial uses of scraped data — this project is strictly non-commercial and academic in nature.
This dataset directly supports both research questions. The title field is the input for VADER sentiment scoring, while the score field allows segmentation of posts by engagement level, which is necessary for answering the second research question about whether high-upvote posts correlate more strongly with price movements.

**Second Dataset: Bitcoin Historical Price**
The second dataset contains historical weekly price and volume data for Bitcoin (BTC-USD) sourced from Yahoo Finance via the yfinance Python library. Data was retrieved for the same time window as the Reddit dataset: January 1, 2024 through January 1, 2026, using a weekly interval, producing approximately 104 weekly observations:

df_price = yf.download("BTC-USD", start="2024-01-01", end="2026-01-01", interval="1wk")

The raw data is stored as crypto_prices_raw-2.csv and the cleaned/merged version (again) as reddit_btc_merged.csv in the project repository. After cleaning and column renaming, the dataset is structured as a time-series table where each row represents one week of Bitcoin price data. The columns are: date (the week start date, normalized to Monday to align with the Reddit data), open (the opening price in USD for that week), high (the weekly high price in USD), low (the weekly low price in USD), close (the closing price in USD for that week), volume (average daily trading volume for the week in USD), price_change (the difference between the weekly close and open), and price_pct_change (the percentage change from open to close for that week). The close price is the primary metric used for correlation analysis, as it represents the final agreed-upon market price and is the standard measure used in financial research.
Yahoo Finance data was accessed via yfinance and is freely available for non-commercial and research purposes. One of our considerations was that yfinance is an unofficial third-party wrapper, meaning the underlying data source could change its structure or terms of service at any time. Thus, the dataset should be treated as a snapshot in time of the data at that exact moment and could potentially change down the road. There are no significant ethical constraints associated with this dataset, as it reflects publicly traded market prices and contains no personal information.

## Data Quality
We conducted a thorough quality assessment based on our practice in class and labs before any cleaning or analysis was performed. We examined both datasets for duplicate records, missing values, and data type inconsistencies, and also considered higher-level concerns about reliability, representativeness, and cross-dataset alignment.

For the Reddit dataset, no duplicate post IDs were found, which confirmed that each record represented a unique submission. The core fields used in analysis: title, score, upvote_ratio, num_comments, and timestamp, were fully populated with no null values. The main quality issue identified was the presence of removed and deleted posts, where content fields were filled with '[removed]' or '[deleted]' rather than actual text. These records are technically present in the dataset but represent posts that no longer exist on the platform, and should be removed from the working dataset prior to analysis. Although our sentiment analysis relied exclusively on the title field rather than the body text, keeping records like these would introduce posts that may have been mistakes or faulty, which would explain why they were deleted in the first place. Ultimately, since we had enough data for our analysis, we felt like deleting them to preserve quality was the best alternative. In addition to deleted/removed posts, the title field itself presented other data quality concerns. Reddit post titles tend to be short, informal, and often intentionally vague to be humorous, which places limits on how accurately the VADER sentiment analyzer can score them. This is because VADER was designed primarily on social media text, but it still depends on having enough linguistic content (something they specifically outline on their website) to assign a meaningful polarity score. A title like "Thoughts?" or "This is big" (which are real titles) carries almost no sentiment despite representing a real post that may have generated substantial community engagement. However, this isn't a flaw that can be corrected exactly through data cleaning, it's more of a structural limitation of Reddit titles as a sentiment source, and it is worth keeping in mind when interpreting the sentiment scores produced by this analysis. It is also something to keep in mind for future work, relying on the more in-depth material to determine sentiment scores.

For the Bitcoin price dataset, no duplicate rows or missing values were found across any columns. All columns were confirmed to be the correct types, and the date column was stored in datetime format, requiring no conversion before use. The weekly data sourced from Yahoo Finance via the yfinance library is generally considered reliable for academic and research purposes. That said,  yfinance is an unofficial third-party that accesses Yahoo Finance's internal API, and it is worth noting that its not actually Yahoo Finance's actualy product. Instead, it is a "formally supported data product". Therefore, the data also should be treated as more of a reliable snapshot, rather than a guaranteed permanent, validated source. For this project, the data was consistent and complete, and we couldn't identify any substantive content-level quality issues through our analysis and research of Yahoo Finance data.

Finally, there was a more broader quality concern that cuts across both datasets and relates to more of their alignment with one another. The Reddit data was normalized on a Monday-calendar based week to match the structure of the weekly price data. However, Reddit posts are timestamped in UTC and Bitcoin trades continuously across global markets in multiple time zones, which is something that makes it so volatile and such a hot topic, you can trade it at anytime as opposed to regular stock trading hours. This means a post submitted late on a Sunday evening in one time zone could technically fall into a different trading week, which depends on our specific configurations with the weekly boundaries and where the trader is located. This results in small but real timing inconsistencies at the edges of each weekly window. While this is unlikely to meaningfully distort patterns across the full date range of the dataset, it is a legitimate timing limitations, but the analysis depends on accurate week-time alignment between Reddit sentiment and price movement. Still, at any week with a strong or weak sentiment-price relationship, it may be worth examining with this in mind before drawing firm conclusions.

## Data Cleaning
**Reddit Dataset (df_bitcoin_clean)**
Our primary quality issue with the Reddit dataset was the presence of removed and deleted post information. Of the 3,150 posts collected, 820 had a selftext value of '[removed]' and 12 had '[deleted]', meaning that some of the content was no longer accessible. Because our sentiment analysis was performed on post titles rather than body text, we chose to exclude them to ensure consistency and avoid any issues with empty or placeholder text surfacing in specific columns. After filtering, the cleaned dataset was reduced to 2,318 posts.
We also ran a duplicate check on the post id field. No duplicate IDs were found, confirming that the Arctic Shift API returned unique posts within each weekly sample. The reset_index(drop=True) call was applied after filtering to ensure a clean integer index on the resulting dataframe.
Next, we parsed the created_utc field into a proper datetime column (timestamp). We then derived a week_start column that began on the Monday of each post's week by subtracting the day-of-week offset. This was essential for making sure that both the reddit data and bitcoin data were alligned on the weekly level. The .dt.normalize() call ensured all week_start values were midnight timestamps with no time component, preventing any merge mismatches caused by intra-day offsets.

**Bitcoin Price Dataset (df_price_clean)**
The raw price data downloaded from yfinance using a weekly interval provided one row per week.  Each trading day was assigned a week_start (Monday) using the same day-of-week subtraction logic applied to the Reddit data. We then grouped by week_start and computed the open as the first trading day's open price, the close as the last trading day's close price, the high and low as the week's extreme values, and the volume as the mean daily volume across the week. This approach ensured that weekly price movement was measured from the actual start to the actual end of each trading week rather than from one week's close to the next.  From these values we derived two new columns: price_change and price_pct_change. These became our primary dependent variables for analysis. The price data had no missing values and no duplicates.

**Sentiment Scoring and Weekly Aggregation**
VADER sentiment analysis was applied to each post's title using the compound score, which ranges from -1, which is the most negative, to +1, which is the most positive. Posts were then labeled using standard thresholds: compound >= 0.05 as positive, <= -0.05 as negative, and between those values as neutral. Across the 2,318 cleaned posts, 1,344 were neutral (58.0%), 621 were positive (26.8%), and 353 were negative (15.2%).
Individual posts were then aggregated to the weekly level using the same week_start key. For each week we computed the post_count, avg_score (Reddit upvote score), avg_upvote_ratio, avg_comments, avg_sentiment (mean VADER compound score), positive_ratio, and negative_ratio. This produced a weekly Reddit dataframe with 105 rows which represented one per week across the two-year window.

**Merging**
The weekly Reddit and weekly price dataframes were merged on the date column using an inner join. The inner join retained only weeks present in both datasets, which in practice was all 105 weeks, yielding a final merged dataframe (df_merged) with 105 rows and 15 columns. No data was lost in the merge.

## Findings
**RQ1: Does Weekly Reddit Sentiment Predict Next-Week Bitcoin Price Movement?**
The short answer is no, at least not in any way we could measure. We ran a linear regression between average weekly sentiment from r/Bitcoin and the following week's Bitcoin price percent change. The result was essentially flat — r = -0.0976, p = 0.3244 — which is both weak and nowhere near statistically significant.
What's interesting is that the correlation is slightly negative, meaning weeks with more positive sentiment on Reddit were very loosely associated with price dropping the week after. That's counterintuitive if you'd expect bullish posts to lead to price increases, but the effect is so small it's probably just coincedence. The dual-axis chart (fig3) backs this up visually, as there's no consistent pattern where sentiment peaks lead to price movement the following week. And the scatter plot (fig4), which specifically plots this week's sentiment against next week's price change, is basically a cloud with no discernible slope in either direction.

**RQ2: Do High-Upvote Posts Carry More Signal?**
We split the data by whether a week's average post score was above the 75th percentile (a score of 94) and ran the same regression on each group. High-upvote weeks showed a modestly larger correlation (r = -0.2167, p = 0.2982) than low-upvote weeks (r = -0.0367, p = 0.7481), but neither came close to significance. The high-upvote group also only had 25 observations, which makes it really hard to read anything into a correlation that size, and with that few data points, a moderate r-value can show up by chance pretty easily.
Both groups showed a negative direction, which aligns with RQ1 but is still counterintuitive given that fig2 shows sentiment was generally positive throughout the period. One possible explanation is that the community tends to post more enthusiastically right as prices peak but again, we can't say that confidently with these numbers.

**Overall**
Neither test produced a significant result, and honestly that's a finding in itself. Bitcoin's price over this period (fig1) is highly volatile and clearly driven by forces well beyond what people are posting on Reddit — macro news, ETF activity, regulatory developments, and broader market sentiment all play a role. On top of that, VADER scoring only post titles, which means a lot of nuance gets lost.  A title like "Is Bitcoin dead?" scores close to neutral even though it's clearly not. With more posts per week, longer body text, or a model trained on crypto-specific language, the results might look different, but for this dataset, sentiment alone doesn't predict price.

## Future Work
**Lessons Learned**
One of the bigger realizations from this project was how much the quality of your analysis depends on decisions you make early in data collection. Collecting only 30 posts per week felt reasonable at the start, but by the end we realized that we needed a lot more, especially when you filter out removed and deleted posts and end up with as few as 15–20 usable posts in some weeks. Those weekly sentiment averages are based on a pretty small sample of what was actually being said on the subreddit that week. We also learned that temporal alignment between datasets isn't something you can just figure out at the merge step. The Reddit data and Bitcoin price data have different native differences, and getting them to line up cleanly on a shared weekly key required some finetuning of both pipelines. Catching that earlier would have saved a lot of rework. Finally, using VADER on post titles alone has real limits for this kind of analysis. Titles on r/Bitcoin tend to be short and often ambiguous. Titles like "Is this the top?" or "Thoughts?" score close to neutral even when the post itself is clearly bearish or bullish. The signal just isn't rich enough in 5–10 words.

**Pontential Future Work**
In the future, there could be more posts per week. The most straightforward improvement would be increasing the weekly collection limit from 30 to something like 100–200, or removing the cap entirely and collecting all posts above a minimum score threshold. More posts per week means more reliable weekly sentiment estimates and less week-to-week noise. The collection loop runs fine in Colab but would benefit from checkpointing at larger volumes so a session timeout doesn't require starting over.

We could also have a longer time window. Two years gives 105 weekly observations, which is enough to run correlations but not really enough to detect weak effects reliably, especially when splitting into subgroups. Extending to 4–5 years, or switching to daily granularity with daily sentiment aggregation, would substantially increase statistical power.

One thing to note for future work is that VADER was designed for general social media and doesn't understand crypto-specific language. Words like "dump," or "to the moon" carry strong directional meaning in this community but get scored generically. A model fine-tuned on financial or crypto text would likely produce more meaningful scores and could be loaded in Colab without much additional setup.

## Challenges
Getting the weekly alignment right was a huge challenge for us. The most technically frustrating part of the project was making sure the Reddit data and Bitcoin price data were actually aligned on the same week boundaries. The Reddit posts have precise UTC timestamps, while the yfinance weekly download uses its own internal aggregation logic, and getting both to agree on what "week of January 8th" meant took more work than expected. Our solution was to normalize everything to a Monday week_start key which worked cleanly but required rethinking both pipelines mid-project.
We also had to deal with removed and deleted posts. About 26% of the posts we collected had their body content removed or deleted. This is just a reality of working with historical Reddit data and there's no way to recover that text after the fact. We filtered those posts out for consistency, but it meant losing a meaningful chunk of our dataset, particularly in some weeks where the removal rate was higher than average.
We also had a problem with API rate limits and Colab session constraints. The Arctic Shift API requires a delay between requests to avoid hitting rate limits, so collecting all 104 weeks of data took around 60–90 seconds per run. In Colab this is manageable, but Colab sessions can time out or disconnect during long-running cells, which means the entire collection loop might need to be re-run from scratch if the runtime resets.
Small subgroup sizes for RQ2. When we split df_merged into high and low-upvote groups for RQ2, the high-upvote group only had 25 rows. Running a correlation on 25 data points isn't that much which is why it made the RQ2 analysis feel more illustrative than conclusive, and it's something we'd want to address before drawing stronger claims.
VADER also had limits on short titles. A surprising number of r/Bitcoin post titles are short, vague, or question-based. VADER scores most of these as neutral, which is technically correct but not very informative. When a large portion of your posts score near zero, your weekly average sentiment ends up compressed toward neutral regardless of what the community was actually feeling. That's a fundamental limitation of the title-only approach.

## Reproducing
All the code for this project is in one .py file.  It can be found here: https://github.com/BenCoop16/IS-477/blob/main/is477_proj_updated.py.  Be sure to run this piece of code first and upload the .py file:
from google.colab import files
files.upload()
You should then be good to run the next line of code, which is the following: !python is477_proj_updated.py
If this doesn't work, then we have also left the .ipynd file in case or errors.

**What's in the Repository**
is477_proj_updated.py — our main file
is477_proj_updated.ipynb — our backup file
requirements.txt — all dependencies and versions
reddit_bitcoin_raw.csv — raw Reddit posts (3,150 rows)
reddit_bitcoin_clean.csv — cleaned posts after filtering (2,318 rows)
crypto_prices_clean.csv — weekly Bitcoin price data (105 rows)
Output figures: fig1 through fig4 as PNG files

If any CSVs are too large for GitHub (>50MB), they'll be in a shared Illinois Box folder linked at the top of the README. Just download them and drop them in the same folder as the notebook
Colab handles almost everything automatically. The only extra install is at the top of the notebook:
!pip install vaderSentiment
If you're running locally instead, just do pip install -r requirements.txt. Key packages are pandas, numpy, matplotlib, scipy, yfinance, and vaderSentiment.

**Licenses**
Reddit data was pulled via the Arctic Shift API for academic use. Bitcoin price data comes from Yahoo Finance via yfinance.

**Running the Notebook**
Click the "Open in Colab" badge at the top of the notebook in GitHub, then just run the cells in order. The whole thing takes about 2–3 minutes, most of which is the Reddit data collection loop waiting between API requests. Everything else runs quickly.

If your Colab session disconnects, you'll need to re-run from the top since nothing persists between sessions. The CSV files saved mid-notebook can be downloaded from the Colab file browser on the left sidebar before closing. If your final numbers differ slightly from ours, it's likely because the Arctic Shift API doesn't guarantee the exact same posts on every run, but the conclusions should still hold.

## References:
- Arctic Shift. (2024). Arctic Shift Reddit Archive API. Retrieved from https://arctic-shift.photon-reddit.com/api/posts/search
- Aroussi, R. (2019). yfinance: Yahoo! Finance market data downloader [Python library]. Retrieved from https://pypi.org/project/yfinance/
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55
- Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. Proceedings of the Eighth International AAAI Conference on Weblogs and Social Media.
- McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 51–56.
- Reddit, Inc. (2024). r/Bitcoin subreddit [Public forum data archived via Arctic Shift]. Retrieved from https://www.reddit.com/r/Bitcoin/
- Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. Nature Methods, 17, 261–272. https://doi.org/10.1038/s41592-019-0686-2
- Yahoo Finance. (2024). Bitcoin USD (BTC-USD) historical data [Dataset]. Retrieved via yfinance Python library.

