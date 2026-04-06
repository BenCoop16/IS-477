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

