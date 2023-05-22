import emoji
from collections import Counter
from urlextract import URLExtract
import pandas as pd
extract=URLExtract()
def total_messages(user_selection,dataset):
    if user_selection !='Overall':
        dataset=dataset[dataset['users']==user_selection]
    #no of messages
    messages_number=dataset.shape[0]
    #number of words
    words=[]
    for i in dataset['messages']:
        
        words.extend(i.split())
    #count of media messages
    media_messag=dataset[dataset['messages']=='<Media omitted>\n'].shape[0]
    #count of links shared in  chart
    
    links=[]
    for message in dataset['messages']:
        links.extend(extract.find_urls(message))
    
    return messages_number,len(words),media_messag,len(links)
    


#finding the top5 memmbers busy in this chat
def busy(dataset):
    dt=dataset['users'].value_counts(ascending=False).head()
    dataset=round((dataset['users'].value_counts()/dataset.shape[0])*100,2).reset_index().rename(columns={'index':'user_names','users':'percent'})

    return dt,dataset

#common words top 20
def common_words(user_selection,dataset):
    if user_selection !='Overall':
        dataset=dataset[dataset['users']==user_selection]
    temp=dataset[dataset['users']!='group notification']
    temp=temp[temp['messages']!='<Media omitted>\n']
    #common word list
    common_words=[]
    for message in temp['messages']:
        common_words.extend(message.split())


    set=pd.DataFrame(Counter(common_words).most_common(20))
    

    return set



#common emojis
def emojis(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    emojis=[]
    for i in dataset['messages']:
        emojis.extend([emo for emo in i if emo in emoji.UNICODE_EMOJI['en']])

    emojis_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojis_df


def monthly_timeline(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    timeline=dataset.groupby(['year','month_num','month'])['messages'].count().reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline.month[i]+'- '+str(timeline.year[i]))
    timeline['time']=time
    return timeline 

def daily_timeline(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    daily_timeline=dataset.groupby(['only_date'])['messages'].count().reset_index()
    
    return daily_timeline

def week(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    return dataset['day_name'].value_counts()

def month_activity(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    return dataset.month.value_counts()

def heatmap(user_selection,dataset):
    if user_selection!='Overall':
        dataset=dataset[dataset['users']==user_selection]
    table=dataset.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return table