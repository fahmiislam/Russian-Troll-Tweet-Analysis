# Russian Troll Tweet Analysis

In this project, we will analyze Russian troll tweet data from the dataset provided by [fivethirtyeight](https://github.com/fivethirtyeight/russian-troll-tweets/).  
[Some analysis](http://pwarren.people.clemson.edu/Linvill_Warren_TrollFactory.pdf) of this data has already been completed and published by Linvill and Warren of Clemson university.

In this analysis, we will be trying to answer one primary question:  
**What characteristics of troll accounts and their tweets make them successful?**

In this case, we are equating success to the number of followers the troll account has, as a higher follower account will allow the troll to spread their message to a greater number of individuals. 

As we answer this question, we will be answering some secondary questions that will help guide our answer, such as:
* Which account category is most successful?
* What are some specific characteristics of the most successful account category?
* What type of language are the top troll accounts using?

---

### Background: 

We are analyzing the Russian troll tweet dataset in order to identify the specific attributes of successful troll accounts, in this case success being defined as being able to spread their message to a large number of other users. We are measuring the success by using the ‘followers’ column in the dataset, which displays the number of followers that a specific troll account has, and we are specifically analyzing troll accounts that had garnered greater than 10,000 followers. We are running a sentiment analysis of the tweets, which works optimally with English tweets, so we subset the data to only include tweets that were in English. We are also only analyzing the account categories discussed in the paper by Linvill and Warren (linked above), as the other account categories lack detailed information. In doing this, we are able to analyze which characteristics result in the most powerful or effective troll account, and perhaps a better idea of how to combat or even build effective troll accounts ourselves. 

There were 4 account categories that we found were successful:
* LeftTroll: Spread socially liberal tweets particularly focusing on topics relating to gender, sexuality, and race. Bashed mainstream Democratic candidates including Hillary Clinton while supporting Bernie Sanders prior to the 2016 election. 
* NewsFeed: Appeared as U.S. local news gatherers, sent links to local news stories and tweeted about local issues.
* HashtagGamer: Tweeted entirely regarding hashtag games on Twitter. 
* RightTroll: Spread right-wing messages and supported the candidacy of former President Trump. Also bashed the Democratic party as well as moderate Republicans.

---

<h2 align="center">What characteristics of troll accounts and their tweets make them successful??</h2>
<h3 align="center">
<b>Plot 1:</b> Relationships between different aspects of successful Russian troll accounts and their tweets
</h3>

![](tweet_characteristics.png)

This is a very rich plot and it reveals to us many aspects of the successful troll accounts and tweets. Starting off with the heatmap, we can analyze linear correlations between some of the features, and we can see how they relate to one another. We see that the strongest positive correlation is between 'Followers' and 'Following' which suggests that as the troll accounts followed more people, they would have more followers themselves, and therefore a larger reach. This principle is observable on many different social media, where bot accounts tend to send out follow requests en masse in the hopes that they will get more followers themselves, which establishes some sort of legitimacy and a greater reach.  
With the scatterplots and KDE plots, we can analyze any non-linear relationships and any grouping that occurs by group category. For example, we can see that the 'NewsFeed' accounts tend to send fairly neutral tweets in terms of polarity and subjectivity, while the political accounts of 'LeftTrolls' and 'RightTrolls' tend to send tweets that are more subjective and polar. 

---

<h2 align="center">Which account category is most successful?</h2>
<h3 align="center">
<b>Plot 2:</b> Boxplots showing distributions of followers by account category
</h3>

![](followers_by_category.png)

We can see that troll accounts classified as 'RightTrolls' have the greatest number of successful accounts on average, followed by the 'LeftTrolls'. Of course, while on average this is true, there is a signficant range of followers for the 'RightTroll' accounts, and some outliers for the 'NewsFeed' accounts are quite large as well. 

---

<h2 align="center">What are some specific characteristics of the most successful account category?</h2>
<h3 align="center">
<b>Plot 3:</b> Heatmap showing correlations between characteristics of successful RightTroll accounts
</h3>

![](right_heatmap.png)

We can see that the 'RightTrolls' have an even greater positive correlation between 'Following' and 'Followers', strongly implying that there is a linear relationship between the two variables. We can also observe that 'Polarity' seems to have a neutral correlation with the success of the 'RightTrolls', while 'Subjectivity' actually has a moderate negative correlation with the follower count. 

---

<h2 align="center">What type of language are the top troll accounts using?</h2>
<h3 align="center">
<b>Plot 4:</b> Wordcloud of the top words used by successful troll accounts. 
</h3>

![](tweet_wordcloud.png)

We can see that a big focus of tweets sent out or retweeted by the successful troll accounts was political. With 'trump' being the single most common word and 'obama' being up there too, there was a big focus on US presidents in their tweets. Beyond that, some divisive language was very common, such as 'death', 'murder', 'attack', 'shooting', and 'killed'. In general, this language could potentially serve to bring about quarreling and incite fear among those who read these tweets.  

---

### Conclusions:

When considering which characteristics of Russian troll accounts and tweets led to the greatest amount of success, we were able to reach a few specific conclusions. First off, being political in general may lead to greater success, as the RightTroll and LeftTroll accounts were the top two most successful account categories on average. We also observed a very strong positive correlation between follower count and following count for all successful accounts as well as the most successful account category, the RightTrolls. Also with the RightTrolls, we were able to see what type of language these accounts were using that may have led to their success, and we found that they were  often intentionally divisive and controversial, which may draw in specific audiencies to further their success. These conclusions would suggest that in order to maximize success, following many other users and being overtly political is a strong method. 

---

Bibliography:  

Linvill, D and Warren, P "Troll Factories: The Internet Research Agency and State-Sponsored Agenda Building" June 2018 http://pwarren.people.clemson.edu/Linvill_Warren_TrollFactory.pdf
