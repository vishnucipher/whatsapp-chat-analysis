import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
import seaborn as sns
import streamlit as st
import re
import mod1


#page configuration
st.set_page_config (page_title='Whatsapp Chat Analysis📊',page_icon='what.ico',layout="wide",initial_sidebar_state="expanded")

#Removing the streamlit Hamburger and Footer
st.markdown("""<style>
.css-164nlkn.egzxvld1
{
visibility:hidden;
}""",unsafe_allow_html=True)





def preprocessing(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    #messages
    messages=re.split(pattern,data)[1:]

    #dates
    dates=re.findall(pattern,data)

    dic={'Dates':dates,'user_messages':messages}
    dataset=pd.DataFrame(dic)

    #modification
    dataset['Dates']=dataset.Dates.str.replace(' - ','')

    #converting Datetime to datatime type
    dataset['Dates']=pd.to_datetime(dataset['Dates'])

    #users and messages are seaparating from the text
    users=[]
    messages=[]
    for message in dataset['user_messages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
        
    #columns for users and messages
    dataset['users']=users
    dataset['messages']=messages

    dataset.drop(columns=['user_messages'],inplace=True)

    #clarity on date and time 
    dataset['year']=dataset['Dates'].dt.year
    dataset['month']=dataset['Dates'].dt.month_name()
    dataset['month_num']=dataset['Dates'].dt.month
    dataset['day']=dataset['Dates'].dt.day
    dataset['hour']=dataset['Dates'].dt.hour
    dataset['minute']=dataset['Dates'].dt.minute 
    dataset['only_date']=dataset['Dates'].dt.date
    dataset['day_name']=dataset['Dates'].dt.day_name()
    period=[]
    for hour in dataset['hour']:
        if hour==23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))

    dataset['period']=period
    return dataset

col1,col2=st.columns([2,1],gap='small')
with col1:
    st.markdown('# WHATSAPP CHAT ANALYSIS')
    st.text('This is whatsapp chat analysis')
with col2:
    st.image('chat-pic.png',width=200)
st.error('This website is only applicable for 24hours format whatsapp chat', icon="🚨")
file=st.file_uploader('Please Upload TXT File',type=['txt'])

if file is not None:
    don=file.getvalue()
    data=don.decode('utf-8')
    dataset=preprocessing(data)
    st.dataframe(dataset)
   
  
    #users list
    list_users=list(dataset.users.unique())
    list_users.remove('group notification')
    list_users.sort()
    list_users.insert(0,'Overall')


    user_selection=st.sidebar.selectbox('**SELECT USERES**',options=list_users)
    if st.sidebar.button('show analysis'):
        num_messages,words,media_messag,num_links=mod1.total_messages(user_selection,dataset)
        
        st.markdown('---')
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Monthly timeline dataframe')
            timeline=mod1.monthly_timeline(user_selection,dataset)
            st.dataframe(timeline)
        with col2:
            st.subheader('Monthly Timeline')
            fig=pt.figure(figsize=(5,5),facecolor='#808080')
            ax=pt.gca()
            ax.set_facecolor('#808080')
            pt.plot(timeline.time,timeline.messages,color='#800000')
            pt.grid(axis='both')
            pt.xticks(rotation=90)
            spacing = 0.10
            fig.subplots_adjust(bottom=spacing)
            st.write(fig)
        
        st.markdown('---')
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Datewise Messages DataFrame')
            daily=mod1.daily_timeline(user_selection,dataset)
            st.dataframe(daily)


        with col2:
            st.subheader('Datewise  Graph')
            fig=pt.figure(figsize=(5,5),facecolor='#808080')
            ax=pt.gca()
            ax.set_facecolor('#808080')
            pt.plot(daily.only_date,daily.messages,color='#800080')
            pt.grid(axis='both')
            pt.xticks(rotation=90)
            spacing = 0.10
            fig.subplots_adjust(bottom=spacing)
            st.write(fig)
        st.markdown('---')
        st.subheader(' Activity Map')
        col1,col2=st.columns(2)
        
        with col1:
            st.markdown('#### Busy Months')
            month=mod1.month_activity(user_selection,dataset)
            fig=pt.figure(figsize=(5,5),facecolor='#808080')
            ax=pt.gca()
            ax.set_facecolor('#808080')
            pt.bar(month.index,month.values,color=['r','b','k','y','brown','green','#990011','#FEE715','#101820','#F96167','#317773','#00FFFF'])
            #pt.legend(labels=list(week.index))
            pt.grid(axis='both')
            pt.xticks(rotation=90)
            st.write(fig)
        
            
            
        with col2:
            st.markdown('#### Busy Days ')
            week=mod1.week(user_selection,dataset)
            fig=pt.figure(figsize=(5,5),facecolor='#808080')
            ax=pt.gca()
            ax.set_facecolor('#808080')
            pt.bar(week.index,week.values,color=['green','#990011','#FEE715','#101820','#F96167','#317773','#00FFFF'])
            #pt.legend(labels=list(week.index))
            pt.grid(axis='both')
            pt.xticks(rotation=90)
            st.write(fig)
            #st.bar_chart(week.reset_index())

        st.markdown('---')

        st.subheader(user_selection+' Heatmap')
        pivot=mod1.heatmap(user_selection,dataset)
        fig=pt.figure(figsize=(5,5),facecolor='#808080')
        sns.heatmap(pivot)
        st.write(fig)
        
        st.markdown('---')

    
        #creating the columns
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.markdown('#### Total Messages')
    
            st.subheader(num_messages)

        with col2:
            st.markdown('### Total words')
            st.subheader(words)
        with col3:
            st.markdown('### Media')
            st.subheader(media_messag)
        with col4:
            st.markdown('### Links shared')
            st.subheader(num_links)
        #timeline

        st.markdown('---')

#finding busy
        if user_selection=='Overall':
            x,per_df=mod1.busy(dataset)
            st.markdown('#### Busy members in chart')
            col1,col2=st.columns(2)
            with col1:
                fig=pt.figure(figsize=(5,5),facecolor='#808080')
                pt.bar(x.index,x.values,color=['r','g','y','b','k'])
                ax=pt.gca()
                ax.set_facecolor('#808080')
                pt.xlabel('users')
                pt.ylabel('send messages values')
                pt.xticks(rotation=90)
                pt.grid(axis='both')
                pt.show()
                st.write(fig)
            with col2:
                st.dataframe(per_df)

        st.markdown('---')

        #most common word
        most_common_words=mod1.common_words(user_selection,dataset)
        col1,col2=st.columns(2)
        with col1:
            st.markdown('#### Most common words'+' used by '+user_selection)
            st.dataframe(most_common_words)
        with col2:
            st.markdown('#### Most common word chart')
            
            fig=pt.figure(figsize=(5,9),facecolor='#808080')
            pt.bar(most_common_words[0],most_common_words[1],color='#000080')
            ax=pt.gca()
            ax.set_facecolor('#808080')
            pt.xlabel('most common words')
            pt.ylabel('count of words')
            pt.xticks(rotation=90)
            st.write(fig)
        
        st.markdown('---')
        #emoji analysis
        col1,col2=st.columns(2)
        with col1:
            st.markdown('#### Most used emojies'+' '+user_selection)
            emojis=mod1.emojis(user_selection,dataset)
            st.dataframe(emojis)
        with col2:
            st.markdown('#### Pie Chart')
            fig=pt.figure(figsize=(5,5),facecolor='#808080')
            pt.title('Emojis in pie chart')
            pt.pie(emojis[1],labels=emojis[0],autopct='%1.1f%%')
            ax=pt.figure()
            ax.set_facecolor('#808080')
            pt.legend(title='Emojis')
            st.write(fig)
        st.markdown('---')

