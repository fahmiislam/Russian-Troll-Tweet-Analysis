import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from imageio import imread

def hide_current_axis(*args, **kwargs):
    """Hides the current axis"""
    plt.gca().set_visible(False)

if __name__ == '__main__':

    # df = pd.read_csv('all_tweets.csv', low_memory=False)
    # df.drop(columns=['harvested_date', 'new_june_2018'], inplace=True)
    # df = df[df.account_category != 'account_category']

    # df = df.astype({'external_author_id': np.float64,
    #                 'following':          np.int64,
    #                 'followers':          np.int64,
    #                 'retweet':            np.int64,
    #                 'content':            'str',
    #                 'account_category':   'str'})
    
    # df = df[(df.region == 'United States') & (df.language == "English")]
    
    # df['polarity'], df['subjectivity'] = (df.content.apply(lambda x: TextBlob(x).sentiment.polarity)), \
    #                                      (df.content.apply(lambda x: TextBlob(x).sentiment.subjectivity))
    
    df = pd.read_csv('df_with_sentiment.csv')

    df_plot = df.loc[(df.account_category != 'NonEnglish')  & \
                    (df.account_category != 'Unknown')     & \
                    (df.account_category != 'Commercial')]   \
                .copy().reset_index(drop=True)
    
    
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
    
    # create figure and set default font size
    fig = plt.figure(figsize=(12,12))
    plt.rcParams.update({'font.size': 14})

    # create pairgrid object
    pg = sns.PairGrid(df_plot.drop(columns=col_to_drop), hue='account_category', diag_sharey=False)

    # create new axis for heatmap and colorbar
    (xmin, _), (_, ymax) = pg.axes[0, 0].get_position().get_points()
    (_, ymin), (xmax, _) = pg.axes[-1, -1].get_position().get_points()
    ax1 = pg.fig.add_axes([xmin - 0.052, ymin + 0.01, xmax - xmin + 0.003, ymax - ymin + 0.003], facecolor='none')
    ax2 = pg.fig.add_axes([0.91, 0.275, 0.04, 0.678], facecolor='none')

    # create heatmap labels and colormap
    ax1_labels = ['', 'Followers', 'Retweet', 'Polarity', 'Subjectivity']
    ax2_labels = ['Following', 'Followers', 'Retweet', 'Polarity', '']
    cmap = sns.diverging_palette(0, 210, 100, 60, as_cmap=True)

    # create and edit heatmap and colorbar
    hm = sns.heatmap(df_corr, mask=mask, cmap=cmap, vmax=0.75, vmin=-0.25, square=True,
                    linewidths=0, annot=True, annot_kws={'size': 22}, ax=ax1,
                    cbar=True, cbar_ax=ax2,
                    yticklabels=ax2_labels, xticklabels=ax1_labels)

    hm.tick_params(left=False, right=False, top=False, bottom=False,
                labelleft=False, labelright=True, labeltop=True, labelbottom=False,
                labelsize=16)
    hm.set_yticklabels(hm.get_yticklabels(), va='center')

    cbar = hm.collections[0].colorbar
    cbar.set_ticks([-0.25, 0, 0.25, 0.5, 0.75])
    cbar.ax.tick_params(labelsize=16)
    cbar.outline.set_linewidth(0)
    cbar.outline.set_edgecolor('white')

    # configure pairgrid object
    pg.map_upper(hide_current_axis)
    pg.map_diag(sns.kdeplot, legend=False, shade=True, alpha=0.5, linewidth=1, thresh=0)
    pg.map_lower(sns.scatterplot, alpha=0.5)

    # add a legend and legend title
    pg.add_legend(title='', adjust_subtitles=True, bbox_to_anchor=(0.53, -0.119, .5, .5),
                fontsize=14)
    plt.text(.56, 9.5, 'Account Category    ', fontsize=18, weight='medium')

    # add linewidths to the heatmap manually
    x_pos = [0.39, -0.06, -0.512, -0.962]
    y_pos = [65.464, 52.6, 39.81, 27.05]
    line_count = [23, 17, 12, 7]
    for i in range(4):
        plt.text(x_pos[i], 64.9, '_' * line_count[i], fontsize=60, weight='heavy', 
                c='white', va='top', rotation=90)
        plt.text(0.55, y_pos[i], '_' * line_count[i], fontsize=60, weight='heavy', 
                c='white', ha='right')

    # configure and edit labels
    label_pads = [31.5, 10, 23, 23, 31.5]
    axis_labels = ['Following', 'Followers', 'Retweet', 'Polarity', 'Subjectivity']

    for idx, ax in enumerate(pg.axes.flat[0:21:5]):
        ax.set_ylabel(axis_labels[idx], labelpad=label_pads[idx], fontsize=16)

    for idx, ax in enumerate(pg.axes.flat[20:25]):
        ax.set_xlabel(axis_labels[idx], fontsize=16)

    for ax in pg.axes.flat[1:21:5]:
        ax.set_xticks([0, 50000])

    plt.suptitle('Relationships Between Different Aspects of Successful Russian Troll Accounts and Their Tweets',
                fontsize=22, y=1.038, ha='center', va='center')

    # plt.savefig('tweet_characteristics.png', bbox_inches='tight', facecolor='w', dpi=200)
    # plt.savefig('tweet_characteristics.png', bbox_inches='tight', facecolor='w', dpi=800)

    plt.show()


    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)

    sns.boxplot(data=df_plot, x='followers', y='account_category', orient='h', 
                palette='tab10', width=0.5, 
                medianprops={'linewidth': 2.25,
                            'color': 'k',
                            'alpha': 1},
                flierprops={'marker': 'o', 
                            'markeredgecolor': 'black',
                            'markersize': 10, 
                            'alpha': 0.5})
                    
    ax.set_xlabel('Followers', labelpad=10, fontsize=16)
    ax.set_ylabel('Account Category', labelpad=10, fontsize=16)
    ax.xaxis.set_tick_params(length=0, labelsize=16)
    ax.yaxis.set_tick_params(length=0)
    ax.grid(axis='x', linestyle='--', linewidth=0.5, color='k', alpha=0.5)
    ax.set_title('Distribution of Followers by Account Category', fontsize=20, x=0.4, y=1.05)

    # plt.savefig('followers_by_category.png', bbox_inches='tight', facecolor='w', dpi=200)
    # plt.savefig('followers_by_category.png', bbox_inches='tight', facecolor='w', dpi=800)

    plt.show()

    df_right = df_plot[df_plot['account_category'] == 'RightTroll'].copy().reset_index(drop=True)

    df_right_corr = df_right.drop(columns=col_to_drop).copy().corr()
    mask_right = np.triu(np.triu(df_right_corr)[1:, :-1])

    plt.figure(figsize=(16, 12))

    cmap = sns.diverging_palette(0, 210, 100, 60, as_cmap=True)

    hm = sns.heatmap(df_right_corr.iloc[1:,:-1], mask=mask_right, cmap=cmap, square=True, fmt='.2f',
                    linewidths=5, annot=True, cbar=True, vmin=-1, vmax=1, annot_kws={'size': 22, 'weight': 'bold'})
                    
    ax = plt.gca()
    ax.xaxis.set_tick_params(length=0)
    ax.yaxis.set_tick_params(length=0)
    ax.set_xticklabels(labels=[x.get_text().title() for x in ax.get_xticklabels()], fontsize=16)
    ax.set_yticklabels(labels=[y.get_text().title() for y in ax.get_yticklabels()], fontsize=16)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=16)

    plt.text(x=3.14, y=1.5,
            s='Correlations Between\nDifferent Aspects\nof RightTroll Accounts',
            fontsize='22', ha='center', va='center', weight='bold')

    # plt.savefig('right_heatmap.png', bbox_inches='tight', facecolor='w', dpi=200)
    # plt.savefig('right_heatmap.png', bbox_inches='tight', facecolor='w', dpi=800)

    plt.show()


    df_words = df.content[df.followers > 10000].copy().reset_index(drop=True)

    all_words = df_words.str.cat(sep=' ').lower()
    tt = TweetTokenizer()
    tweet_tokens = TweetTokenizer().tokenize(all_words)
    STOPWORDS.update(['>>', '<<', 'new', 'say', 'says', 'make', 'year', 'will'])

    only_words = [token for token in tweet_tokens if not token.startswith('#') \
                and not token.startswith('@') and not token.startswith('http')]

    only_words_str = " ".join(only_words)
    twitter_mask = imread('twitter_mask.png')

    wordcloud = WordCloud(colormap='viridis', mask=twitter_mask, contour_width=2, contour_color='blue',
                        background_color='white', min_word_length=2, stopwords=STOPWORDS).generate(only_words_str)

    plt.figure(figsize=(16, 12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # plt.savefig('tweet_wordcloud.png', bbox_inches='tight', facecolor='w', dpi=200)
    # plt.savefig('tweet_wordcloud.png', bbox_inches='tight', facecolor='w', dpi=800)

    plt.show()
