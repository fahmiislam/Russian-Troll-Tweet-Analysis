import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

def hide_current_axis(*args, **kwargs):
    """hides the current axis"""
    plt.gca().set_visible(False)

if __name__ == '__main__':

    # only run lines 15-30 if 'df_with_sentiment.csv' does not exist (if you are running the program for the first time)
    df = pd.read_csv('all_tweets.csv').drop(columns=['harvested_date', 'new_june_2018'])
    df = df[df.account_category != 'account_category']   # filter out erroneous rows in the data

    df = df.astype({'external_author_id': np.float64,
                    'following':          np.int64,
                    'followers':          np.int64,
                    'retweet':            np.int64,
                    'content':            'str',
                    'account_category':   'str'})

    # sentiment analysis of tweets
    df['polarity'] = df.content.apply(lambda x: TextBlob(x).sentiment.polarity)
    df['subjectivity'] = df.content.apply(lambda x: TextBlob(x).sentiment.subjectivity)

    # save to csv if coming back to the file later and to avoid running sentiment analysis again
    df.to_csv('df_with_sentiment.csv', index=False)
    df = pd.read_csv('df_with_sentiment.csv')

    df_eng = df[(df.region == 'United States') & (df.language == "English")]   # isolate just the English tweets, as sentiment analysis is not optimal on non-English tweets
    # df_eng = df_eng[(df_eng.polarity != 0)                                   # filter out tweets with no polarity, not used in this analysis

    # filter out account categories not analysed in the Linvill & Warren paper
    df_plot = df_eng.loc[(df_eng.account_category != 'NonEnglish')  & \
                         (df_eng.account_category != 'Unknown')     & \
                         (df_eng.account_category != 'Commercial')]   \
                    .copy()

    MIN_FOLLOWERS = 10000           # somewhat arbitrary minimum follower count, 10,000 in this case to only analyse successful troll accounts
    MAX_FOLLOWERS = float('inf')    # maximum number of followers to include in the analysis, may be specified later

    # group by external_author_id in order to avoid repeat analysis of the same account
    df_plot = df_plot.loc[(df_plot.followers > MIN_FOLLOWERS) & (df_plot.followers < MAX_FOLLOWERS)] \
                     .groupby('external_author_id').agg({'account_category': 'first',
                                                         'following':        np.mean,
                                                         'followers':        np.mean,
                                                         'updates':          np.mean,
                                                         'retweet':          np.mean,
                                                         'polarity':         np.mean,
                                                         'subjectivity':     np.mean}).reset_index()

    # columns to not be included in the correlation matrix
    col_to_drop = ['external_author_id', 'updates']

    df_corr = df_plot.drop(columns=col_to_drop).copy().corr()
    mask = np.tril(np.ones_like(df_corr, dtype=bool))

    # working with the PairGrid to manually change labels is a pain, so changing it in the df
    df_plot.rename({'following':    'Following',
                    'followers':    'Followers',
                    'polarity':     'Polarity',
                    'subjectivity': 'Subjectivity',
                    'retweet':      'Retweet'}, axis='columns', inplace=True)

    # plot the data
    fig=plt.figure(figsize=(12,12))
    plt.rcParams.update({'font.size': 14})

    # pairgrid on the lower half of the figure
    pg = sns.PairGrid(df_plot.drop(columns=col_to_drop), hue='account_category', diag_sharey=False)
    pg.map_upper(hide_current_axis)
    hp = pg.map_diag(sns.histplot)
    pg.map_offdiag(sns.scatterplot, alpha=0.5)

    pg.add_legend(title='', adjust_subtitles=True, bbox_to_anchor=(0.51, -0.119, .5, .5), 
                fontsize=14)
    plt.text(.44, 16.2, 'Account Category   ', fontsize=18, weight='medium')

    # creating axes to designate the position of the heatmap and colorbar
    (xmin, _), (_, ymax) = pg.axes[0, 0].get_position().get_points()
    (_, ymin), (xmax, _) = pg.axes[-1, -1].get_position().get_points()
    ax1 = pg.fig.add_axes([xmin - 0.005, ymin - 0.005, xmax - xmin, ymax - ymin], facecolor='none')
    ax2 = pg.fig.add_axes([0.88, 0.266, 0.04, 0.678], facecolor='none')

    # heatmap on the upper half of the figure
    x_labels = ['', 'Followers', 'Retweet', 'Polarity', 'Subjectivity']
    y_labels = ['Following', 'Followers', 'Retweet', 'Polarity', '']
    cmap = sns.diverging_palette(0, 210, 100, 60, as_cmap=True)

    hm = sns.heatmap(df_corr, mask=mask, cmap=cmap, vmax=0.75, vmin=-0.25, square=True,
                     linewidths=5, annot=True, annot_kws={'size': 22}, ax=ax1,
                     cbar=True, cbar_ax=ax2,
                     yticklabels=y_labels, xticklabels=x_labels)

    hm.tick_params(left=False, right=False, top=False, bottom=False,
                   labelleft=False, labelright=True, labeltop=True, labelbottom=False,
                   labelsize=16)
    hm.set_yticklabels(hm.get_yticklabels(), va='center')
    
    cbar = hm.collections[0].colorbar
    cbar.set_ticks([-0.25, 0, 0.25, 0.5, 0.75])
    cbar.set_ticklabels(['-0.25', '0', '0.25', '0.5', '0.75'])
    cbar.ax.tick_params(labelsize=16)
    cbar.outline.set_linewidth(0)
    cbar.outline.set_edgecolor('white')

    plt.suptitle('Relationships Between Different Aspects of Russian Troll Tweets and Their Accounts',
                fontsize=22, y=1.02, ha='center', va='center')

    # plt.savefig('tweet_analysis.png', bbox_inches='tight', facecolor='w', dpi=800)

    plt.show()
