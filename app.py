import streamlit as st
import pandas as pd
import requests
import pickle as pkl


#Read dataframe and similarity from pickle
job_list = pkl.load(open('QPJobRoleNew.pkl','rb'))
job = pd.DataFrame(job_list)
#job = job_list['QPJobRoleName'].values
similarity = pkl.load(open('similarityNew.pkl','rb'))


#Add function here
list_jobs =[]
list_qualif = []

#Qualification Filtering
select_Qual = 0
def showQuali():
    global select_Qual
    select_Qual = st.selectbox(
        'Choose the your qualification',
        (job['MinimumEducationQualificationExperience'].drop_duplicates()))
    req_df = job[job['MinimumEducationQualificationExperience'] == select_Qual]
    #st.write(job['MinimumEducationQualificationExperience'].values)


#Age Filtering
select_Age = 0
req_age_list = []

#NSQF filtering
select_NSQF = 0
req_NSQF_list =[]


#Qualification Filtering
select_Quali =''
req_Quali_list = []

#Age and NSQF both Filter simulteneously
req_Age_NSQF_list =[]

#Age and Qualification both Filter simulteneously
req_Age_Quali_list =[]


#NSQF and Qualification both filter simulteneously
req_NSQF_Quali_list = []

#Age , NSQF and Qualification all filter simulteneously
req_Age_NSQF_Quali_list = []


#Job Recommendation
def recommend(jobRole):
    jobIndex = job[job['QPJobRoleName'] == jobRole].index[0]
    distances = similarity[jobIndex]
    sugg_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:500]

    for i in sugg_list:
        list_jobs.append(job.iloc[i[0]].QPJobRoleName)
        list_qualif.append(job.iloc[i[0]].MinimumEducationQualificationExperience)




st.title('Recommendation')
select_Qpjobs = st.selectbox(
    'Choose the job which is suitable for you',
    (job['QPJobRoleName'].values))



# Sidebar for select box
with st.sidebar:


    st.title('Select the criteria :')
    Age = st.checkbox('Age')
    if Age:#== True:
        select_Age = st.selectbox(
            'Choose the your Age',
            (sorted(job['MinimumJobEntryAge'].drop_duplicates())))






    NSQF = st.checkbox('NSQF Level')
    if NSQF:
        select_NSQF = st.selectbox(
            'Choose the your NSQF Level',
            (sorted(job['NSQFLevel'].drop_duplicates())))


    Quali = st.checkbox('Qualification')
    if Quali:
        select_Quali = st.selectbox(
            'Choose the your NSQF Level',
            (sorted(job['MinimumEducationQualificationExperience'].drop_duplicates())))




if st.button('Search Related Courses'):
    recommend(select_Qpjobs)
    # Testing code from here


    if (select_Age!=0 and select_NSQF!=0 and select_Quali!=''):
        req_df = job.loc[(job['NSQFLevel'] == select_NSQF) & (job['MinimumEducationQualificationExperience'] == select_Quali)]
        req_Age_NSQF_Quali_list = req_df['QPJobRoleName'].tolist()
        #st.write(req_Age_NSQF_Quali_list)
        st.write('You selected Age = ',select_Age,'You selected NSQF =', select_NSQF, 'You selected Qualification = ', select_Quali)
        new_list = list(set(list_jobs).intersection(set(req_Age_NSQF_Quali_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            # st.write(new_list)
            count=0
            for i in list_jobs:
                if i in req_Age_NSQF_Quali_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break


    elif (select_Age!=0 and select_NSQF!=0):
        req_df = job.loc[(job['MinimumJobEntryAge']==select_Age) & (job['NSQFLevel']==select_NSQF)]
        req_Age_NSQF_list = req_df['QPJobRoleName'].tolist()
        st.write('You selected Age =',select_Age,'You selected NSQF = ',select_NSQF)
        new_list = list(set(list_jobs).intersection(set(req_Age_NSQF_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            count=0
            for i in list_jobs:
                if i in req_Age_NSQF_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break


    elif (select_Age!=0 and select_Quali!=''):
        req_df = job.loc[(job['MinimumJobEntryAge'] == select_Age) & (job['MinimumEducationQualificationExperience'] == select_Quali)]
        req_Age_Quali_list = req_df['QPJobRoleName'].tolist()
        st.write('You selected Age =', select_Age, 'You selected Qualification = ', select_Quali)
        new_list = list(set(list_jobs).intersection(set(req_Age_Quali_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            #st.write(new_list)
            count=0
            for i in list_jobs:
                if i in req_Age_Quali_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break



    elif (select_NSQF!=0 and select_Quali!=''):
        req_df = job.loc[(job['NSQFLevel'] == select_NSQF) & (job['MinimumEducationQualificationExperience'] == select_Quali)]
        req_NSQF_Quali_list = req_df['QPJobRoleName'].tolist()
        # st.write(req_NSQF_Quali_list)
        st.write('You selected NSQF =', select_NSQF, 'You selected Qualification = ', select_Quali)
        new_list = list(set(list_jobs).intersection(set(req_NSQF_Quali_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            # st.write(new_list)
            count=0
            for i in list_jobs:
                if i in req_NSQF_Quali_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break


    elif select_Age != 0:
        req_df = job.loc[job['MinimumJobEntryAge'] == select_Age]
        req_age_list = req_df['QPJobRoleName'].tolist()
        st.write('You selected Age =', select_Age)
        new_list = list(set(list_jobs).intersection(set(req_age_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            count = 0
            for i in list_jobs:
                if i in req_age_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break

    elif select_NSQF !=0:
        req_df = job.loc[job['NSQFLevel'] == select_NSQF]
        req_NSQF_list = req_df['QPJobRoleName'].tolist()
        st.write('You selected NSQF =', select_NSQF)
        new_list = list(set(list_jobs).intersection(set(req_NSQF_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            count=0
            for i in list_jobs:
                if i in req_NSQF_list:
                    st.write(i)
                    count += 1
                    if count == 5:
                        break


    elif select_Quali!='':
        req_df = job.loc[job['MinimumEducationQualificationExperience'] == select_Quali]
        req_Quali_list = req_df['QPJobRoleName'].tolist()
        st.write('You select Qualification =', select_Quali)
        new_list = list(set(list_jobs).intersection(set(req_Quali_list)))
        if new_list==[]:
            st.write('No result....')
        else:
            count = 0
            for i in list_jobs:
                if i in req_Quali_list:
                    st.write(i)
                    count+=1
                    if count==5:
                        break

    else:
        count = 0
        for (a, b) in zip(list_jobs, list_qualif):
            st.write(a)
            count += 1
            if count == 5:
                break


