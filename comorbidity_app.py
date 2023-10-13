import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import random

# -----------------------Filter presentation-------------------------------
st.sidebar.image('logo_efrei.png')
st.sidebar.markdown("<h1>Data Visualization Project 2023</h1>", unsafe_allow_html=True)
st.sidebar.write("#datavz2023efrei")
st.sidebar.markdown("<h2>Author : Chloé GATTINO </h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h2>Professor : Mano MATHEW </h2>", unsafe_allow_html=True)


# Like for Linkedin and github
st.sidebar.markdown("<h3> To contact me :", unsafe_allow_html=True)
linkedin_icon = "🔗"
linkedin_text = f"{linkedin_icon} [Visit my LinkedIn profile](https://www.linkedin.com/in/chlo%C3%A9-gattino-link9113/)"
st.sidebar.markdown(linkedin_text, unsafe_allow_html=True)

github_icon = "📁"
st.sidebar.markdown("<h4> To see my lastest work :", unsafe_allow_html=True)
github_link = f"{github_icon}[Visit my GitHub](https://github.com/chlo-gto91)"
st.sidebar.markdown(github_link, unsafe_allow_html=True)

# to provide feedback on the usefulness of the information
st.sidebar.title("Your opinion is important : ")
avis_utilisateur = st.sidebar.slider("Was this article useful to you?", 0, 5, 2)

echelle_avis = {
    0: "Not useful at all",
    1: "Not very useful",
    2: "Neutral",
    3: "Useful",
    4: "Very useful",
    5: "Extremely useful",
}
avis_texte = echelle_avis[avis_utilisateur]
st.sidebar.write(f"Your opinion : {avis_texte}")

# Info about data
st.sidebar.title("About data ")
data_link = "[Go through data](https://www.data.gouv.fr/ods/preview/data.ameli.fr/comorbidites)"
st.sidebar.markdown(data_link, unsafe_allow_html=True)
st.sidebar.write('Updating of data from 2015 to 2021, France')

# --------------------------Web main page  ----------------------------------------

# Data cleaning and preprocessing
df = pd.read_csv("comorbidites_data.csv", delimiter=';')
missing_values = df.isnull().sum()
df_sans_valeurs_manquantes = df.dropna()


# To introduce the subject 
st.markdown("<h1 style='text-align: center;'>Analysis of comorbidity in France between 2015 and 2023</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>How can comorbidity be a problem and must be analyzed to better anticipate it ?</h2>", unsafe_allow_html=True)

st.title("I - Introduction")
st.write('Welcome to this comorbidity analysis where the aim is to better understand the relationships between pathologies, preventing certain diseases, improving health care, or even contributing to medical research. Comorbidity is not a rare phenomenon but it is very important to understand this situation because sometimes, comorbidity can be dangerous and must be anticipated.')
st.write('Definition : Comorbidity is a common phenomenon defined by the simultaneous presence of two or more medical conditions or diseases in the same person.')


# Interaction to give examples of comorbidity
st.markdown("<h3>Context</h3>", unsafe_allow_html=True)
st.write("Guess what are the 8 main causes of Comorbidity ?", unsafe_allow_html=True)
causes_user = []
nouvelle_cause = st.text_input("Write a cause ")

if st.button("Add your cause"):
    if nouvelle_cause:
        causes_user.append(nouvelle_cause)
        st.success(f"'{nouvelle_cause}' was added to the list.")

st.markdown("User-entered causes:")
for cause in causes_user:
    st.write(f"- {cause}")

if st.button("Click on me to show the 8 real causes"):
    vraies_causes = ["Aging of the population", "Interaction between diseases", "Longer life expectancy", "Impact of treatment (side effects or increase the risk of developing other health problems)", "Common risk factors (smoking, chronic stress...)", "Health behaviors (Individuals with certain medical conditions may be more likely to adopt harmful health behaviors)", "Exposure to environmental factors", "Socio-economic inequalities"]
    st.subheader("Real causes of comorbidity:")
    for cause in vraies_causes:
        st.write(f"- {cause}")

st.write('Now that you know more about the subject, let s start analyzing the data from our dataset for co-morbidity in France since 2015')


#------------------------------Analysis ----------------------------------

#---------------------I - Data visualisation--------------------------------

st.title("II - Data visualization : Analysis")
st.markdown("<h3> Preprocessing </h3>", unsafe_allow_html=True)

st.write('You can press the button below to see part of our dataset')
if st.checkbox('Take a look at the data : '):
    st.image('data.png')
      
st.write('Our dataset contains : 31283 rows x 16 columns')
st.write('Now that you have read the data, we will begin our analysis.')


# fist graph : linechart
st.markdown("<h3>Exploratory data analysis </h3>", unsafe_allow_html=True)
st.write("<h4>How has the comorbidity evolved since 2015 ?</h4>", unsafe_allow_html=True)

df_grouped = df.groupby('annee')['ncomorb'].sum().reset_index()
fig, ax = plt.subplots()   
ax.plot(df_grouped['annee'], df_grouped['ncomorb'], marker='o', linestyle='-')
ax.set_xlabel('Year')
ax.set_ylabel('Ncomorb')
ax.set_title('Evolution of comorbidity over the years')
st.pyplot(fig)

with st.expander("Explanation : "):
    st.write('Through this graph above, we can observe that there is an increase in the number of comorbidities between 2015 and 2023 in France. We can explain this phenomenon mainly by the aging of the population.')

# second graph : bar_chart
st.write("<h4>How is the data regarding priority levels distributed?</h4>", unsafe_allow_html=True)
niveau_prioritaire_counts = df['niveau_prioritaire'].value_counts()
st.bar_chart(niveau_prioritaire_counts, use_container_width=True)
with st.expander("Explanation : "):
    st.write('This bar_chart shows the dispersion of the data : Niveau prioritaire, which is the categorizing information or cases based on their urgency and importance. In our case, it is levels 2 and 3 which are the most frequent.')


# Fird graph : bar_chart
st.write("<h4>Relationship between Proportion of Comorbidity and Number of Cases ?</h4>", unsafe_allow_html=True)
st.scatter_chart(data=df, x='proportion_comorb', y='ncomorb')
with st.expander("Explanation : "):
    st.write('We can see that the points appear to follow an upward trajectory on this scatter plot showing the relationship between the proportion of comorbidity (column : proportion_comorb) and the number of cases (column : ncomorb). This shows that there is a strong relationship between these two data')


#--------------------------Analysis per year----------------------------------------------

st.write("<h4>What is the most common group of pathologies per year ?</h4>", unsafe_allow_html=True)

# for year selection
sorted_years = sorted(df['annee'].unique())
st.write("<h4>Analysis per year</h4>", unsafe_allow_html=True)
selected_year = st.selectbox("Select a year", sorted_years)

# Add this section for debugging
filtered_data = df[df['annee'] == selected_year]
st.write(f"Filtered Data for {selected_year}:")
st.write(filtered_data)

patho_grouped = filtered_data.groupby('patho_niv1').size().reset_index(name='count')

# Find the most common pathology group 1
most_common_patho = patho_grouped.loc[patho_grouped['count'].idxmax()]
most_common_patho_name = most_common_patho['patho_niv1']
most_common_patho_count = most_common_patho['count']

st.subheader(f"Analysis of the most frequent Pathology Group 1 in {selected_year}")
st.write(f"Selected Year: {selected_year}")
st.write(f"The most common Pathology Group 1 is: {most_common_patho_name}")
st.write(f"Number of occurrences: {most_common_patho_count}")

st.bar_chart(patho_grouped.set_index('patho_niv1'))

# -- Quiz button 1--
st.subheader('Quiz moment! Which pathology 1 is most associated with recurrence in this context of morbidity?')
options = ['Cancer', 'Sida', 'Diabète']
correct_answer = 'Cancer'
selected_option = st.radio("Select an answer:", options)

if selected_option:
    if st.button("Check", key="quiz_button1", on_click=None):
        if selected_option == correct_answer:
            st.write('<div style="color: green;">Right answer! Cancer is, in fact, the most associated recurrent pathology in this context of morbidity.</div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="color: red;">Incorrect answer. The correct answer is: {correct_answer}.</div>', unsafe_allow_html=True)

with st.expander("Explanation : "):
    st.write('<div style="color: black;">Indeed, thanks to our analysis, we were able to learn that it is cancer which is the pathology 1 most present in this study of comorbidity, all years combined. Then, heart disease is the second most common pathology, and in third place, inflammatory or rare disease or HIV or AIDS.</div>', unsafe_allow_html=True)


# Find the most common pathology group 2
patho_grouped = filtered_data.groupby('patho_niv2').size().reset_index(name='count')

most_common_patho = patho_grouped.loc[patho_grouped['count'].idxmax()]
most_common_patho_name = most_common_patho['patho_niv2']
most_common_patho_count = most_common_patho['count']

st.subheader(f"Analysis of the most frequent Pathology Group 2 in {selected_year}")
st.write(f"Selected Year: {selected_year}")
st.write(f"The most common Pathology Group 2 is: {most_common_patho_name}")
st.write(f"Number of occurrences: {most_common_patho_count}")

st.bar_chart(patho_grouped.set_index('patho_niv2'))
with st.expander("Explanation : "):
    st.write('For each years, the first most common pathology 2 is Chronic inflammatory diseases, and second, rare sickness ')

# -- Quiz button 2--
st.subheader('Quiz moment! Which pathology 2 is most associated with recurrence in this context of morbidity?')
options = ['Paraplégie', 'Maladies inflammatoires chroniques', 'Cancer de la prostate']
correct_answer = 'Maladies inflammatoires chroniques'
selected_option = st.radio("Select an answer:", options)

if selected_option:
    if st.button("Check it", key="quiz_button", on_click=None):
        if selected_option == correct_answer:
            st.write('<div style="color: green;">Right answer! Maladies inflammatoires chroniques is, in fact, the most associated recurrent pathology 2 in this context of morbidity.</div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="color: red;">Incorrect answer. The correct answer is: {correct_answer}.</div>', unsafe_allow_html=True)

with st.expander("Explanation : "):
    st.write('Indeed, thanks to our analysis, we were able to learn that it is chronic inflammatory diseases which is the pathology 2 most present in this study of comorbidity, all years combined. Then, Rare diseases is the second most common pathology')

# Find the most common pathology group 3
patho_grouped = filtered_data.groupby('patho_niv3').size().reset_index(name='count')

most_common_patho = patho_grouped.loc[patho_grouped['count'].idxmax()]
most_common_patho_name = most_common_patho['patho_niv3']
most_common_patho_count = most_common_patho['count']

st.subheader(f"Analysis of the most frequent Pathology Group 3 in {selected_year}")
st.write(f"Selected Year: {selected_year}")
st.write(f"The most common Pathology Group 3 is: {most_common_patho_name}")
st.write(f"Number of occurrences: {most_common_patho_count}")

st.bar_chart(patho_grouped.set_index('patho_niv3'))

# -- Quiz button 3--
st.subheader('Quiz moment! Which pathology 3 is most associated with recurrence in this context of morbidity?')
options = ['Mucoviscidose', 'Hospitalisations ponctuelles', 'Cancer du sein']
correct_answer = 'Hospitalisations ponctuelles'
selected_option = st.radio("Select the answer:", options)

if selected_option:
    if st.button("Check the result", key="quiz_button3", on_click=None):
        if selected_option == correct_answer:
            st.write('<div style="color: green;">Right answer! Hospitalisations ponctuelles is, in fact, the most associated recurrent pathology in this context of morbidity.</div>', unsafe_allow_html=True)
        else:
            st.write(f'<div style="color: red;">Incorrect answer. The correct answer is: {correct_answer}.</div>', unsafe_allow_html=True)

with st.expander("Explanation : "):
    st.write('<div style="color: black;">Indeed, thanks to our analysis, we were able to learn that it is Hospitalisations ponctuelles which is the pathology 3 most present in this study of comorbidity, all years combined.</div>', unsafe_allow_html=True)


# drop-down menu to analyze the pathologies associated with each other
st.subheader('How are the pathologies associated ? ')

selected_patho_niv1 = st.selectbox("Select a level 1 pathology", df['patho_niv1'].unique())
patho_niv1_df = df[df['patho_niv1'] == selected_patho_niv1]
selected_patho_niv2 = st.selectbox("Select a level 2 pathology", patho_niv1_df['patho_niv2'].unique())
patho_niv2_df = patho_niv1_df[patho_niv1_df['patho_niv2'] == selected_patho_niv2]
selected_patho_niv3 = st.selectbox("Select a level 3 pathology", patho_niv2_df['patho_niv3'].unique())

st.write(f"Selected level 1 pathology : {selected_patho_niv1}")
st.write(f"Selected level 2 pathology : {selected_patho_niv2}")
st.write(f"Selected level 3 pathology : {selected_patho_niv3}")

# graph for labels
st.subheader('How has the proportion of comorbidities associated with a disease evolved over the years?')
annees = df['annee'].unique()

# Sélectionnez les libellés de comorbidité uniques dans les données
libelles_comorbidite = df['libelle_comorbidite'].unique()

selected_libelle_comorbidite = st.selectbox("Select a comorbidity label", libelles_comorbidite)
filtered_data = df[df['libelle_comorbidite'] == selected_libelle_comorbidite]

fig, ax = plt.subplots()
sns.set(style="whitegrid")
ax = sns.lineplot(x='annee', y='proportion_comorb', data=filtered_data, marker='o')
ax.set_title(f'Evolution of the presence of "{selected_libelle_comorbidite}" by year')
ax.set_xlabel("Year")
ax.set_ylabel("Proportion of comorbidity")
ax.set_yticklabels([])
st.pyplot(fig)


#------------------------------Conclusion----------------------------------
st.title('III - Conclusion :')
st.write('I have conducted an analysis of comorbidity in France since 2015. This analysis has highlighted a concerning trend: comorbidity is increasingly prevalent in the French population. Comorbidity refers to the coexistence of multiple diseases or conditions in an individual and can have a significant impact on the quality of life of patients, as well as on the healthcare system in terms of costs and resources. One of the major findings of this analysis is that cancer plays a substantial role in the rise of comorbidity in France. Cancer is a complex and insidious disease, capable of triggering other cancers due to factors such as immune system suppression, genetic alterations, and side effects of treatments. Additionally, cancer patients are often at an increased risk of developing other conditions, such as cardiovascular diseases, diabetes, and mental health disorders. ')
st.write("<h4>Are there any possible solutions to control this phenomenon?</h4>", unsafe_allow_html=True)
with st.expander("Solutions  : "):
    st.write('To reduce comorbidity in France, several solutions should be considered:')
    solutions = ["Cancer Prevention: Implement more effective cancer prevention and screening programs.", 
                "Improved Cancer Patient Management: Focus on better care for cancer patients by providing psychological support, regular medical follow-up to prevent recurrences, and rehabilitation programs after treatment."
                , "Research and Development of Targeted Treatments: Invest in oncology research to develop more targeted and less toxic treatments, thus reducing side effects that can contribute to comorbidity."
                , "Integration of Healthcare: Encourage an integrated healthcare approach, fostering collaboration among healthcare professionals and care coordination for patients with comorbidities."
                , "Public Education: Raise awareness among the public about the importance of managing chronic diseases, prevention, and regular medical check-ups, emphasizing the risks associated with comorbidity."]
    for sol in solutions:
        st.write(f"- {sol}")         

