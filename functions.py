import streamlit as st
import psycopg2
import pickle
import pandas as pd
import warnings
import itertools
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings('ignore')


@st.experimental_memo(persist='disk')
def get_data():
    with open("heroku_database_credentials.pickle", "rb") as cred:
        credential = pickle.load(cred)

    conn = psycopg2.connect(
        database=credential['Database'],
        host=credential['Host'],
        user=credential['User'],
        port=credential['Port'],
        password=credential['Password']
    )

    query = "SELECT * FROM chocolate_database"
    choco_data = pd.read_sql(query, conn)

    column_names = {"ref": "reference_no",
                    "Company (Manufacturer)": "manufacturer",
                    "Company Location": "company_loc",
                    "Review Date": "review_date",
                    "Country of Bean Origin": "bean_origin",
                    "Specific Bean Origin or Bar Name": "bar_name",
                    "Cocoa Percent": "cocoa_percent",
                    "Ingredients": "ingredients",
                    "Most Memorable Characteristics": "taste",
                    "Rating": "rating"}

    choco_data.rename(columns=column_names, inplace=True)

    choco_data['cocoa_percent'] = choco_data['cocoa_percent'].str.strip('%')
    choco_data['cocoa_percent'] = choco_data['cocoa_percent'].astype('float')

    return choco_data


def count_df(data, data_col):
    choco_count = data[data_col].value_counts().rename_axis(data_col).reset_index(name='count')
    choco_data_with_counts = pd.merge(left=data, right=choco_count, left_on=data_col, right_on=data_col)
    return choco_data_with_counts


def number_indicator(val, title_text, row_num, col_num):
    return go.Indicator(mode='number', value=val,
                        number={'valueformat': '0,f'},
                        title={'text': title_text},
                        domain={'row': row_num, 'column': col_num})


def sort_sliced_dict(main_dict, is_reverse=True, item_count=None):
    sorted_dict = {k: v for k, v in sorted(main_dict.items(), key=lambda item: item[1], reverse=is_reverse)}
    if item_count is not None:
        sorted_dict = dict(itertools.islice(sorted_dict.items(), item_count))
    return sorted_dict


class FirstPageFuncs:

    def __init__(self):
        self.choco_data = get_data()

    def best_chocolates(self):
        choco_data_with_count = count_df(self.choco_data, 'bar_name')
        choco_data_mod = choco_data_with_count[choco_data_with_count['count'] >= 10]
        avg_rating_by_bar = choco_data_mod.groupby('bar_name')['rating'].mean()
        avg_rating_by_bar_df = avg_rating_by_bar.rename_axis('bar_name').reset_index(name='rating')
        avg_rating_by_bar_df_sorted = avg_rating_by_bar_df.sort_values(by='rating', ascending=False).head(10)

        fig = px.bar(avg_rating_by_bar_df_sorted, x='bar_name', y='rating', log_y=True,
                     title='Most Popular Chocolate Bar',
                     color_continuous_scale='viridis',
                     color='rating')
        return fig

    def most_common_company_location(self):
        choco_data = get_data()
        company_loc_list = list(self.choco_data[choco_data['bar_name'].isin(['Kokoa Kamili'])]['company_loc'])
        company_loc_dict = {i: company_loc_list.count(i) for i in company_loc_list}

        fig = px.pie(values=list(company_loc_dict.values()), names=list(company_loc_dict.keys()),
                     title='Most Common Location of Manufacturer',
                     color_discrete_sequence=px.colors.sequential.Aggrnyl)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12)

        return fig

    def most_commonly_used_ingredients(self):
        choco_data_copy = self.choco_data.copy()
        choco_data_copy['ingredients'] = choco_data_copy['ingredients'].str.strip(' ')
        choco_data_copy['num_ingredients'] = choco_data_copy['ingredients'].str.split('-', expand=True)[0]
        choco_data_copy['main_ingredients'] = choco_data_copy['ingredients'].str.split('-', expand=True)[1]
        kamili_ingredients = list(
            choco_data_copy[choco_data_copy['bar_name'].isin(['Kokoa Kamili'])]['main_ingredients'])
        kamili_ingredient_dict = {}

        for ingredient in kamili_ingredients:
            if ingredient in kamili_ingredient_dict:
                kamili_ingredient_dict[ingredient] += 1
            else:
                kamili_ingredient_dict[ingredient] = 1

        fig = px.pie(values=list(kamili_ingredient_dict.values()), names=list(kamili_ingredient_dict.keys()),
                     title='Most Commonly used Ingredients in Kokoa Kamili',
                     color_discrete_sequence=px.colors.sequential.Aggrnyl)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return fig

    def most_memorable_taste(self):
        taste_encode = self.choco_data[self.choco_data['bar_name'].isin(['Kokoa Kamili'])]['taste'].str.get_dummies(
            sep=', ')
        taste_encode['nuts'] = taste_encode['nut'] + taste_encode['nuts']
        taste_encode['rich_cocoa'] = taste_encode['rich'] + taste_encode['rich cocoa'] + taste_encode['rich cooa']

        taste_encode.drop(['nut', 'rich', 'rich cooa'], axis=1, inplace=True)

        tastes = list(taste_encode.columns)
        taste_dict = {}

        for taste in tastes:
            taste_dict[taste] = sum(taste_encode[taste])

        taste_dict = sort_sliced_dict(taste_dict, item_count=8)

        fig = go.Figure(data=[go.Pie(labels=list(taste_dict.keys()), values=list(taste_dict.values()),
                                     pull=[0.1, 0, 0, 0])])
        fig.update_traces(textinfo='percent+label', textposition='inside')
        fig.update_layout(uniformtext_minsize=12, title={'text': "Most Memorable Taste"})
        return fig


class SecondPageFuncs:
    def __init__(self):
        self.choco_data = get_data()

    def best_manufacturer(self):
        choco_data_with_sec_count = count_df(self.choco_data, 'manufacturer')
        choco_data_mod2 = choco_data_with_sec_count[choco_data_with_sec_count['count'] > 10]
        avg_rating_by_company = choco_data_mod2.groupby('manufacturer')['rating'].mean()
        avg_rating_by_company_df = avg_rating_by_company.rename_axis('Company').reset_index(name='Rating')
        avg_rating_by_company_df_sorted = avg_rating_by_company_df.sort_values(by='Rating', ascending=False).head(10)

        fig = px.bar(avg_rating_by_company_df_sorted, x='Company', y='Rating', log_y=True,
                     color_continuous_scale='inferno', color='Rating')
        fig.update_layout(title={'text': 'The Best Chocolate Manufacturer'})
        return fig

    def bean_provider(self):
        soma_choco_data = self.choco_data[self.choco_data['manufacturer'].isin(['Soma'])]
        bean_origins = list(soma_choco_data['bean_origin'])
        bean_dict = {i: bean_origins.count(i) for i in bean_origins}

        bean_dict = sort_sliced_dict(bean_dict, item_count=5)

        fig = px.bar(x=list(bean_dict.keys()), y=list(bean_dict.values()),
                     text=list(bean_dict.values()),
                     color_continuous_scale='inferno',
                     color=list(bean_dict.keys()))

        fig.update_traces(textposition='outside')
        fig.update_layout(title={'text': 'Beans providers for Soma ChocoMaker'},
                          xaxis={'title_text': 'Beans Origin'},
                          yaxis={'title_text': 'Count'})
        return fig

    def choco_tastes(self):
        soma_choco_data = self.soma_choco_dataframe()
        soma_choco_data['taste'] = soma_choco_data['taste'].str.replace(", ", "|")
        soma_choco_data['taste'] = soma_choco_data['taste'].str.replace(",", "|")
        taste_codo = soma_choco_data['taste'].str.get_dummies(sep='|')

        taste_codo['nutty'] = taste_codo['nut'] + taste_codo['nuts'] + taste_codo['nutty']
        taste_codo['woody'] = taste_codo['woodsy'] + taste_codo['woody']
        taste_codo['earthy'] = taste_codo['earth'] + taste_codo['earthy']

        taste_codo.drop(['nut', 'nuts', 'woodsy', 'earth'], axis=1, inplace=True)

        tasty_dict = {}
        tasty_list = list(taste_codo.columns)

        for taste in tasty_list:
            tasty_dict[taste] = sum(taste_codo[taste])

        tasty_dict = sort_sliced_dict(tasty_dict, item_count=7)

        fig = px.bar(x=list(tasty_dict.keys()), y=list(tasty_dict.values()),
                     color_continuous_scale='viridis',
                     color=list(tasty_dict.keys()))
        fig.update_layout(title={'text': 'Most Memorable Taste of Chocolates made by Soma Chocomaker'},
                          xaxis={'title_text': 'Tastes'},
                          yaxis={'title_text': 'Count'})

        return fig

    def cocoa_percentage(self):
        soma_choco_data = self.soma_choco_dataframe()
        cocoa_list = list(soma_choco_data['cocoa_percent'])
        cocoa_percent_dict = {}

        for cocoa_percent in cocoa_list:
            if str(cocoa_percent) in cocoa_percent_dict:
                cocoa_percent_dict[str(cocoa_percent)] += 1
            else:
                cocoa_percent_dict[str(cocoa_percent)] = 1

        cocoa_percent_dict = sort_sliced_dict(cocoa_percent_dict, item_count=5)

        fig = px.pie(names=list(cocoa_percent_dict.keys()), values=list(cocoa_percent_dict.values()),
                     color_discrete_sequence=px.colors.sequential.Agsunset)

        fig.update_layout(title={'text': 'Mostly used Cocoa Percentage in chocolates made by Soma ChocoMaker'})

        return fig

    def soma_choco_dataframe(self):
        return self.choco_data[self.choco_data['manufacturer'].isin(['Soma'])]


class ThirdPageFuncs:

    def __init__(self):
        self.choco_data = get_data()

    def lecithin_ignorance(self):
        self.choco_data['ingredients'] = self.choco_data['ingredients'].str.strip(' ')
        self.choco_data['num_ingredients'] = self.choco_data['ingredients'].str.split('-', expand=True)[0]
        self.choco_data['main_ingredients'] = self.choco_data['ingredients'].str.split('-', expand=True)[1]

        self.choco_data['main_ingredients'] = self.choco_data['main_ingredients'].str.strip(' ')
        ingre_encode = self.choco_data['main_ingredients'].str.get_dummies(sep=',')

        choco_data_lecithin = pd.concat([self.choco_data, ingre_encode['L']], axis=1)
        choco_data_lecithin.rename(columns={'L': 'ingredient_L'}, inplace=True)

        choco_has_lecithin = choco_data_lecithin[choco_data_lecithin['ingredient_L'] == 1]
        choco_has_no_lecithin = choco_data_lecithin[choco_data_lecithin['ingredient_L'] == 0]

        rating_by_choco_has_lecithin = choco_has_lecithin['rating'].mean()
        rating_by_choco_has_no_lecithin = choco_has_no_lecithin['rating'].mean()

        fig = go.Figure()
        fig.add_trace(number_indicator(val=rating_by_choco_has_lecithin,
                                       title_text="Average Rating of Bars having Lecithin",
                                       row_num=0, col_num=0))
        fig.add_trace(number_indicator(val=rating_by_choco_has_no_lecithin,
                                       title_text="Average Rating of Bars having no Lecithin",
                                       row_num=0, col_num=1))

        fig.update_layout(grid={'rows': 1, 'columns': 2, 'pattern': 'independent'})
        return fig

    def rating_by_bean_origin(self):
        rating_by_bean_origin = self.choco_data.groupby('bean_origin')['rating'].mean()
        rating_by_bean_origin = rating_by_bean_origin.rename_axis('bean_origin').reset_index()

        sorted_rating_by_bean_origin = rating_by_bean_origin.sort_values(by='rating', ascending=False).head(10)
        fig = px.bar(sorted_rating_by_bean_origin,
                     x='bean_origin', y='rating',
                     log_y=True,
                     title='Average Rating by Bean Origin',
                     color_continuous_scale='viridis',
                     color='rating')
        return fig

    def num_of_chocos_in_country(self):
        choco_data_with_bean_origin_count = count_df(self.choco_data, 'bean_origin')
        bean_origin_count_gt30 = choco_data_with_bean_origin_count['count'] >= 30
        choco_data_with_bean_origin_count = choco_data_with_bean_origin_count[bean_origin_count_gt30]

        bean_origin_dict = {}

        for origin in choco_data_with_bean_origin_count['bean_origin']:
            if origin in bean_origin_dict:
                bean_origin_dict[origin] += 1
            else:
                bean_origin_dict[origin] = 1

        fig = px.pie(names=list(bean_origin_dict.keys()),
                     values=list(bean_origin_dict.values()),
                     color_discrete_sequence=px.colors.sequential.YlOrRd,
                     template="plotly",
                     hole=0.4,
                     title='bars reviewed for each of bean origin')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        return fig
