import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.DataFrame()

st.title('Data Analysis')
st.header('1. Upload a dataset')

file = st.file_uploader('Choose your file in csv-format', type='csv')

if file is not None:
    df = pd.read_csv(file)
    st.subheader('Your dataset')
    st.dataframe(df)
else:
    st.write("File can't have such extension. Choose one with right format")

st.header('2. Choose the columns')
categorical = ['category', 'year']  # отдельно определяем категориальные, чтоб в дальнейшем подобрать нужный график

y1 = st.selectbox(label="Variable1 (as default second variable is 'film')", options=list(df.columns))

def with_no_percents(y): # функция для преобразования строк с процентами в числа
    return float(y.replace('%', ''))
def to_chart(y):
    if '%' in y:  # отбираем колонки с "%" для преобразования в число
        df[y] = df[y].apply(with_no_percents)
        st.bar_chart(data=df, x=y, y='film')
    elif y not in categorical:
        st.bar_chart(data=df,x='film', y=y)
    else:  # оставшиеся колонки - категориальные, поэтому на них дефолтная переменная 'film' не распространяется
        fig, ax = plt.subplots()
        ax.pie(df[y].value_counts(), labels=df[y].unique(), autopct='%1.1f%%')
        st.pyplot(fig)
to_chart(y1)

y2=st.selectbox(label="Variable2 (as default second variable is 'film')", options=list(df.columns))
to_chart(y2)

st.header('3. Select a statistical tool')
hip = st.selectbox(label='Test the hypothesis with...', options=['...','U-test', 't-test'])
if hip=='U-test':
    st.subheader('Are the differences between domestic and international gross statistically significant?')

    fig, axs = plt.subplots(figsize=(10,15), nrows=2, ncols=1)
    axs[0].set_xlabel('Domestic gross ($m)')
    axs[0].set_ylabel('Movie')
    axs[0].barh(df['film'], df['domestic gross ($m)'])

    axs[1].set_xlabel('International gross ($m)')
    axs[1].set_ylabel('Movie')
    axs[1].barh(df['film'], df['international gross ($m)'])

    st.pyplot(fig)

    u_stat, p_value = stats.mannwhitneyu(df['domestic gross ($m)'], df['international gross ($m)'])
    st.write('U-statistics =', u_stat)
    st.write('p-value =', p_value)

elif hip=='t-test':
    st.subheader("Is it true that there is a difference between success of Marvel's movies of 2018 and 2019?")

    fig, axs = plt.subplots(figsize=(10,15), nrows=2, ncols=1)
    axs[0].set_xlabel('box_office_2018')
    axs[0].set_ylabel('Movie')
    df['% budget recovered'] = df['% budget recovered'].apply(with_no_percents)  # т.к. нету колонки со сборами, но есть колонка с возвратностью бюджета в процентах
    box_office_2018 = df[df['year'] == 2018]["% budget recovered"] / 100 * df[df['year'] == 2018]["budget"]  # получим сборы самостоятельно
    axs[0].barh(df[df['year'] == 2018]['film'], box_office_2018)

    axs[1].set_xlabel('box_office_2019')
    axs[1].set_ylabel('Movie')
    box_office_2019 = df[df['year'] == 2019]["% budget recovered"] / 100 * df[df['year'] == 2019]["budget"] # сборы за 2019 год
    axs[1].barh(df[df['year'] == 2019]['film'], box_office_2019)

    st.pyplot(fig)

    t_stat, p_value = stats.ttest_ind(box_office_2018, box_office_2019)
    st.write('t-statistics =', t_stat)
    st.write('p-value =', p_value)

