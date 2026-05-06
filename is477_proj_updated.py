import requests
import pandas as pd
import time
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for script use
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import linregress

# ── Data Collection ───────────────────────────────────────────────────────────

all_posts = []

start_date = datetime(2024, 1, 1)
end_date   = datetime(2026, 1, 1)
posts_per_week = 30

current = start_date
while current < end_date:
    next_week = current + timedelta(weeks=1)

    params = {
        "subreddit": "Bitcoin",
        "after":     current.strftime("%Y-%m-%d"),
        "before":    next_week.strftime("%Y-%m-%d"),
        "limit":     posts_per_week,
        "sort":      "asc"
    }

    response = requests.get(
        "https://arctic-shift.photon-reddit.com/api/posts/search",
        params=params
    )
    batch = response.json().get('data') or []

    if batch:
        all_posts.extend(batch)

    print(f"Week of {current.date()}: {len(batch)} posts, total: {len(all_posts)}")
    current = next_week
    time.sleep(0.5)

df_bitcoin = pd.DataFrame(all_posts)[
    ['id', 'title', 'selftext', 'score', 'upvote_ratio', 'num_comments', 'created_utc', 'subreddit']
]
df_bitcoin['timestamp'] = pd.to_datetime(df_bitcoin['created_utc'], unit='s')
df_bitcoin.to_csv('reddit_bitcoin_raw.csv', index=False)
print(df_bitcoin.shape)

df_price = yf.download("BTC-USD", start="2024-01-01", end="2026-01-01", interval="1wk")

# ── Data Quality Check ────────────────────────────────────────────────────────

print("Duplicates:", df_bitcoin.duplicated(subset='id').sum())
print("\nMissing values:")
print(df_bitcoin.isnull().sum())
print("\nRemoved posts (selftext is [removed]):", (df_bitcoin['selftext'] == '[removed]').sum())
print("Deleted posts (selftext is [deleted]):", (df_bitcoin['selftext'] == '[deleted]').sum())

print("Duplicates:", df_price.duplicated().sum())
print("\nMissing values:")
print(df_price.isnull().sum())
print("\nPrice data types:")
print(df_price.dtypes)

# ── Data Cleaning ─────────────────────────────────────────────────────────────

df_bitcoin_clean = df_bitcoin[df_bitcoin['selftext'] != '[removed]']
df_bitcoin_clean = df_bitcoin_clean[df_bitcoin_clean['selftext'] != '[deleted]']
df_bitcoin_clean = df_bitcoin_clean.drop_duplicates(subset='id')
df_bitcoin_clean = df_bitcoin_clean.reset_index(drop=True)
print(df_bitcoin_clean.shape)

df_bitcoin_clean['timestamp'] = pd.to_datetime(df_bitcoin_clean['created_utc'], unit='s')
df_bitcoin_clean['week_start'] = (
    df_bitcoin_clean['timestamp']
    - pd.to_timedelta(df_bitcoin_clean['timestamp'].dt.dayofweek, unit='D')
).dt.normalize()

print('Reddit date range:')
print(df_bitcoin_clean['week_start'].min())
print(df_bitcoin_clean['week_start'].max())

df_price_clean = df_price.copy()
df_price_clean = df_price_clean.reset_index()
df_price_clean.columns = [
    c[0].lower() if isinstance(c, tuple) else c.lower()
    for c in df_price_clean.columns
]
df_price_clean.rename(columns={'price': 'date'}, inplace=True)
df_price_clean['date'] = pd.to_datetime(df_price_clean['date'])

# Normalize to Monday so it lines up with week_start in the Reddit data
df_price_clean['date'] = (
    df_price_clean['date']
    - pd.to_timedelta(df_price_clean['date'].dt.dayofweek, unit='D')
)

df_price_clean['price_change']     = df_price_clean['close'] - df_price_clean['open']
df_price_clean['price_pct_change'] = (
    df_price_clean['price_change'] / df_price_clean['open']
) * 100

df_price_clean.to_csv('crypto_prices_raw.csv', index=False)
print(df_price_clean.shape)
print(df_price_clean.head())
print('Weekly price rows:', len(df_price_clean))

df_bitcoin_clean.to_csv('reddit_bitcoin_clean.csv', index=False)
df_price_clean.to_csv('crypto_prices_clean.csv', index=False)
print("All files saved!")

# ── Sentiment Analysis ────────────────────────────────────────────────────────

analyzer = SentimentIntensityAnalyzer()
df_bitcoin_clean['sentiment'] = df_bitcoin_clean['title'].apply(
    lambda x: analyzer.polarity_scores(x)['compound']
)
print(df_bitcoin_clean[['title', 'sentiment']].head(10))

def label_sentiment(score):
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

df_bitcoin_clean['sentiment_label'] = df_bitcoin_clean['sentiment'].apply(label_sentiment)
print(df_bitcoin_clean['sentiment_label'].value_counts())

# ── Merge ─────────────────────────────────────────────────────────────────────

df_weekly_reddit = df_bitcoin_clean.groupby('week_start').agg(
    post_count       = ('id',              'count'),
    avg_score        = ('score',           'mean'),
    avg_upvote_ratio = ('upvote_ratio',    'mean'),
    avg_comments     = ('num_comments',    'mean'),
    avg_sentiment    = ('sentiment',       'mean'),
    positive_ratio   = ('sentiment_label', lambda x: (x == 'positive').sum() / len(x)),
    negative_ratio   = ('sentiment_label', lambda x: (x == 'negative').sum() / len(x)),
).reset_index()
df_weekly_reddit.rename(columns={'week_start': 'date'}, inplace=True)

print(df_weekly_reddit.shape)
print(df_weekly_reddit.head())

df_merged = pd.merge(df_weekly_reddit, df_price_clean, on='date', how='inner')
print(df_merged.shape)
print(df_merged.head())

# ── Visualizations ────────────────────────────────────────────────────────────

# Fig 1: BTC price over time
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df_price_clean['date'], df_price_clean['close'], color='#F7931A', linewidth=1.5)
ax.set_title('Bitcoin (BTC-USD) Closing Price: Jan 2024 – Jan 2026', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('fig1_btc_price.png', dpi=150)
plt.close()
print("Saved → fig1_btc_price.png")

# Fig 2: Sentiment over time
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df_bitcoin_clean['timestamp'], df_bitcoin_clean['sentiment'],
        color='steelblue', linewidth=0.8, alpha=0.4, label='Post Sentiment')
rolling = df_bitcoin_clean.set_index('timestamp')['sentiment'].rolling('7D').mean()
ax.plot(rolling.index, rolling.values, color='navy', linewidth=2, label='7-Day Rolling Avg')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax.set_title('Reddit Post Sentiment (r/Bitcoin): Jan 2024 – Jan 2026', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('VADER Compound Score')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('fig2_sentiment_over_time.png', dpi=150)
plt.close()
print("Saved → fig2_sentiment_over_time.png")

# Fig 3: Dual-axis price vs sentiment
fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(df_price_clean['date'], df_price_clean['close'], color='#F7931A', linewidth=1.5, label='BTC Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('BTC Closing Price (USD)', color='#F7931A')
ax1.tick_params(axis='y', labelcolor='#F7931A')

ax2 = ax1.twinx()
ax2.plot(df_merged['date'], df_merged['avg_sentiment'], color='steelblue', linewidth=1.5, alpha=0.8, label='Weekly Avg Sentiment')
ax2.axhline(0, color='gray', linestyle='--', linewidth=0.6)
ax2.set_ylabel('Avg Weekly Sentiment Score', color='steelblue')
ax2.tick_params(axis='y', labelcolor='steelblue')

ax1.set_title('Bitcoin Price vs. Weekly Reddit Sentiment Over Time', fontsize=14, fontweight='bold')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('fig3_price_vs_sentiment.png', dpi=150)
plt.close()
print("Saved → fig3_price_vs_sentiment.png")

# Fig 4: Scatter sentiment vs next-week price change
subset = df_merged[['avg_sentiment', 'price_pct_change']].copy()
subset['next_week_pct'] = subset['price_pct_change'].shift(-1)
subset = subset.dropna()

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(subset['avg_sentiment'], subset['next_week_pct'],
           alpha=0.4, edgecolors='k', linewidths=0.3, color='steelblue')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.7)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.7)
ax.set_title('Weekly Reddit Sentiment vs. BTC Price Change (Following Week)', fontsize=13, fontweight='bold')
ax.set_xlabel('Average Weekly Sentiment Score (VADER)')
ax.set_ylabel('BTC Price % Change (1 Week Later)')
plt.tight_layout()
plt.savefig('fig4_scatter_sentiment_vs_price.png', dpi=150)
plt.close()
print("Saved → fig4_scatter_sentiment_vs_price.png")

# ── Hypothesis Testing ────────────────────────────────────────────────────────

df_merged['next_week_pct'] = df_merged['price_pct_change'].shift(-1)
rq1_data = df_merged[['avg_sentiment', 'next_week_pct']].dropna()

slope, intercept, r, p, se = linregress(rq1_data['avg_sentiment'], rq1_data['next_week_pct'])
print('RQ1: Sentiment vs. Next Week Price Change')
print(f'  r = {r:.4f}, p = {p:.4f}')

q75 = df_merged['avg_score'].quantile(0.75)
high_upvote = df_merged[df_merged['avg_score'] > q75][['avg_sentiment', 'next_week_pct']].dropna()
slope, intercept, r_high, p_high, se = linregress(high_upvote['avg_sentiment'], high_upvote['next_week_pct'])
print('\nRQ2: High vs. Low Upvote Posts')
print(f'  High upvote posts: r = {r_high:.4f}, p = {p_high:.4f}')

low_upvote = df_merged[df_merged['avg_score'] <= q75][['avg_sentiment', 'next_week_pct']].dropna()
slope, intercept, r_low, p_low, se = linregress(low_upvote['avg_sentiment'], low_upvote['next_week_pct'])
print(f'  Low upvote posts:  r = {r_low:.4f}, p = {p_low:.4f}')
