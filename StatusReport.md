# Project Plan Updates
## 1 (Tasks)
###### The first task that we had was to finalize the project plan.  We did this by analyzing the feedback we got from our milestone 2 assignment.  This included more precise research questions, finding the names of our datasets, and making our timeline more exact with a better description of who would be doing them.  We were able to sit down and discuss exactly what we wanted our questions to answer and are finishing up what we want them to look like.  Furthermore, we were able to identify our datasets and update our timeline with exact responsibilities and the tasks to be completed.

###### The second task we had was to identify our datasets.  They have both been accessed and confirmed as usable for our intended tasks.  The raw data is stored in our repository.  The first data set is Reddit posts from r/Bitcoin and was collected through Arctic Shift Reddit Archive API.  There was no API key required and there are 2,000 posts from the beginning of 2024 to the beginning of 2026.  The second dataset is Bitcoin Historical Price Data and was collected through Yahoo finance.  There are over 700 observations throughout the same time period as the first data set.  All information in both datasets is timestamped, which is what we needed. 

###### The third task we had was to collect the data from both datasets.  We did this in a google collab notebook.  We gathered the Reddit data in groups in 100, as that was the most the API would let us do at once.  The Bitcoin price data was collected into one yfinance cell.  All of the data collected was saved into CSV files and put into the repository. 

###### The fourth task was to clean the data.  Ben is currently working on cleaning both datasets by removing any duplicate posts, looking for any posts with missing data, making sure the timestamps are all in the same timezones for comparison, looking for any outliers in the prices of Bitcoin, etc.  

###### Our fifth step was our sentiment analysis, which Steven is doing.  This hasn't been started yet, but the plan is to use a scoring system to score each Reddit post somewhere between -1 and 1.  By doing this, we can get an idea if the groups of posts had a generally positive or negative appearance.  This is how we can judge if a daily appearance would be connected in any way to the daily change in price of Bitcoin.  

###### Step six is data integration, which will be done by Steven.  This will be done by finally putting the information from the two datasets together and then creating a table where each row contains the daily appearance scores and the price metrics, which will make it easier to look for trends.  

###### Step seven is our analysis and visualization, where Ben will find the correlations between the daily scores and the Bitcoin price metrics.  We will decide how frequently we want to set the data periods and then calculate the scores from there.  Ben will then create the visualizations using the correlations.  

###### Our eigth step will be creating the final report for the whole project.  Ben is going to write the data profile, any ethical considerations we can think of, and the sections about the cleaning of our data.  Steven is going to write the about the findings and visualizations.  

## 2 (Timeline)
###### Finalize project plan (both of us): March 20, 2026
###### Identify datasets (both of us): April 1, 2026
###### Complete data collection (Ben): April 5, 2026
###### Complete data cleaning (Steven): April 11, 2026
###### Sentiment analysis (Ben): April 15, 2026
###### Data integration (Steven): April 20, 2026
###### Data analysis and visualizations (Ben): April 24, 2026
###### Final report and submission (both of us): May 4, 2026

## Changes to the Project Plan
###### So we did end up making a few changes to our Project Plan, especially as we progress throughout our coding file. For starters, the feedback we received on our Milestone 2 was that our research questions were too vague and needed specifics to actually answer, such as timeframes. Thus, we first changed our questions from how do posts affect crypto prices to “Does the average daily sentiment scores for r/Bitcoin posts correlate with Bitcoin's closing price change within a 1-3 day window?” and “Do posts with upvote scores above the 75th percentile have a stronger correlation with next-day Bitcoin price movements?”. These questions better articulate the goal of our project plan in more specific terms. The other feedback we received was that our timeline was too vague, so Steven spent more time updating our progress on all the various tasks we have and have left to be completed in the earlier section of our status report. 
###### Another section of our feedback, and the main change to our project, was the data. We never specified URLs or anything of that nature for the data which we planned to acquire from Reddit API and CoinGecko. However, the Reddit API proved difficult and lengthy to acquire as I needed to request my own individual API key for research purposes and that could’ve taken a few days. Instead, we switched to the “Arctic Shift” archive that includes the same data without API approval and also has free/open access (https://arctic-shift.photon-reddit.com/api/posts/search). This returns JSON responses and allows querying by Reddit subcategories and dates, albeit with a limitation of 100 posts per request which was a challenge I solved (and will talk about later on). For CoinGecko, it no longer has free access to its historical data. Instead, I used YahooFinance via yfinance which provided all the historical daily price and volume daily for bitcoin that we needed at no cost and without any API key.

## Challenges and Problems
###### The main problems of our progress thus far has been the data acquisition. The Reddit API approval delay forced me to switch over to Arctic Shift after the API access request was taking too long. This worked out well, but Arctic Shift has a limitation of 100 posts per request. As a result, I created a loop that did this 20 times over for the past 2 years so that we would have substantial Reddit data, enough to perform data analysis. I then had to combine all the data in one dataframe, but after all of that it created a nice CSV file that should work great. A similar thing happened with CoinGecko, but switching to yfinance was easy and worked really well.

## Ben Cooper’s Contributions Thus Far
###### The contributions I’ve made thus far are in creating all the files as I made the coding ipynb file, uploaded the csv’s of our data, and the status update file. I then also collected/acquired the data and transformed both datasets into workable csv files. I did some preliminary analysis and then cleaned the data to prepare them to be merged and for data analysis operations. Going forwards, I will be responsible for assisting with writing the final report and detailing the datasets such as their privacy restrictions, how trustworthy they are, and other details. But Steven will handle the data analysis, visualizations, sentiment analysis, and proving one way or another of the research questions.

## Steven Sanduski's Contributions Thus Far
###### The contributions I am currently working on is merging the two datasets and the sentiment analysis.  The sentiment analysis will help determine if a certain time period of Reddit posts can be seen as positive or negative towards Bitcoin.  This will then be used to compare with the price metrics.  After that, I will be able to merge the datasets together.  In the future, I will be working on the visualizations and the analysis of the merged data.  
