import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

region_dict = {
    1: "Черкаська", 2: "Чернігівська", 3: "Чернівецька", 4: "АР Крим", 5: "Дніпропетровська",
    6: "Донецька", 7: "Івано-Франківська", 8: "Харківська", 9: "Херсонська", 10: "Хмельницька",
    11: "Київська", 12: "м. Київ", 13: "Кіровоградська", 14: "Луганська", 15: "Львівська",
    16: "Миколаївська", 17: "Одеська", 18: "Полтавська", 19: "Рівненська", 20: "м. Севастополь",
    21: "Сумська", 22: "Тернопільська", 23: "Закарпатська", 24: "Вінницька", 25: "Волинська",
    26: "Запорізька", 27: "Житомирська"
}

default_settings = {
    'min_week': 1, 'max_week': 52,
    'min_year': 1982, 'max_year': 2024,
    'week_range': (1, 52), 'year_range': (1982, 2024),
    'sort_asc': True, 'sort_desc': False,
    'index_name': 'vci', 'region_name': 'Черкаська'
}

df_data = pd.read_csv('data/lab_3.csv', index_col=False)

for key, val in default_settings.items():
    if key not in st.session_state:
        st.session_state[key] = val

def toggle_sorting_flags(current_flag):
    other_flags = ['sort_asc', 'sort_desc']
    other_flags.remove(current_flag)
    if st.session_state[current_flag]:
        st.session_state[other_flags[0]] = False

def filter_dataframe(min_year, max_year, min_week, max_week, index_name, region_name, sort_asc, sort_desc):
    region_code = [k for k, v in region_dict.items() if v == region_name][0]
    filtered_df = df_data[(df_data['year'] >= min_year) & (df_data['year'] <= max_year) &
                          (df_data['week'] >= min_week) & (df_data['week'] <= max_week) &
                          (df_data['oblast'] == region_code)][['year', 'week', index_name]]

    other_df = df_data[(df_data['year'] >= min_year) & (df_data['year'] <= max_year) &
                       (df_data['week'] >= min_week) & (df_data['week'] <= max_week)][['year', 'week', index_name, 'oblast']]

    fig_line, ax_line = plt.subplots(figsize=(10, 4))
    fig_bar, ax_bar = plt.subplots(figsize=(10, 4))

    sns.lineplot(data=filtered_df, x="year", y=index_name, ax=ax_line, label='Selected Region')
    sns.barplot(data=other_df, x='oblast', y=index_name, ax=ax_bar, ci=None)


    if sort_asc and not sort_desc:
        table = filtered_df.sort_values(by=[index_name])
    elif not sort_asc and sort_desc:
        table = filtered_df.sort_values(by=[index_name], ascending=False)
    else:
        table = filtered_df
    return table, fig_line, fig_bar

st.markdown("""
<style>
    .block-container {
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

col_sidebar, _, col_main = st.columns([5, 1, 10])

with col_sidebar:
    dropdown1, dropdown2 = col_sidebar.columns([2, 3])
    dropdown1.selectbox('Select Index', ('vci', 'tci', 'vhi'), key='index_name')
    dropdown2.selectbox('Select Region', region_dict.values(), key='region_name')

    st.markdown("<hr><b>Select Years</b>", unsafe_allow_html=True)
    year_slider = st.slider(" ", 1982, 2024, key='year_range')
    st.session_state['min_year'], st.session_state['max_year'] = year_slider

    st.markdown("<hr><b>Select Weeks</b>", unsafe_allow_html=True)
    week_slider = st.slider(" ", 1, 52, key='week_range')
    st.session_state['min_week'], st.session_state['max_week'] = week_slider


    st.markdown("<hr><b>Select Sorting Order</b>", unsafe_allow_html=True)
    st.checkbox('Ascending', key='sort_asc', on_change=toggle_sorting_flags, args=('sort_asc',))
    st.checkbox('Descending', key='sort_desc', on_change=toggle_sorting_flags, args=('sort_desc',))

    def reset_filters():
        for key in default_settings:
            st.session_state.pop(key, None)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Reset Filters", on_click=reset_filters)

with col_main:
    subcol1, subcol2, subcol3 = col_main.columns(3)
    tab_table, tab_chart, tab_compare = st.tabs(["Table", "Chart", "Comparison"])

    table, fig_line, fig_bar = filter_dataframe(
        st.session_state['min_year'], st.session_state['max_year'],
        st.session_state['min_week'], st.session_state['max_week'],
        st.session_state['index_name'], st.session_state['region_name'],
        st.session_state['sort_asc'], st.session_state['sort_desc']
    )

    with tab_table:
        st.write(table)

    with tab_chart:
        st.pyplot(fig_line)

    with tab_compare:
        st.pyplot(fig_bar)