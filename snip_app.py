import streamlit as st
import sqlite3
import datetime
import pandas as pd
import matplotlib as plt
import matplotlib
import plotly.express as px
matplotlib.use('Agg')


#################################db
con = sqlite3.connect('database.db')
c = con.cursor()

##################################functions
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS snippet_table(language TEXT, code TEXT, description TEXT)")


def add_table(language, code, description, date, collection):
    c.execute('INSERT INTO snippet_table(language, code, description, date, collection) VALUES (?,?,?,?,?)', (language, code, description, date, collection))
    con.commit()


def get_latest():
    c.execute('SELECT * FROM snippet_table ORDER BY date desc')
    data = c.fetchall()
    return data

# def get_language():
#     c.execute('SELECT DISTINCT language from snippet_table')
#     data = c.fetchall()
#     return data

def view_all_snippets():
    c.execute('SELECT * FROM snippet_table')
    data = c.fetchall()
    return data

def search_snip(criteria, term):
    c.execute('SELECT * FROM snippet_table WHERE "{}" LIKE "%{}%"'.format(criteria, term))
    data = c.fetchall()
    return data

def group_collections():
    c.execute('SELECT * FROM snippet_table GROUP BY collection')
    data = c.fetchall()
    return data
    

def select_collections():
    c.execute('SELECT DISTINCT collection from snippet_table')
    data = c.fetchall()
    return data

def select_all_for_collection(collection_choice):
    c.execute('SELECT * FROM snippet_table WHERE collection = "{}"'.format(collection_choice))
    data = c.fetchall()
    return data

def delete_snippet(snip):
    c.execute('DELETE FROM snippet_table WHERE description = "{}"'.format(snip))
    con.commit()


# def add_column():
#     c.execute("ALTER TABLE snippet_table ADD COLUMN collection TEXT")
#     con.commit()


##################################Layout template



def main():
    
    
    st.title("Snippet Search")
    st.sidebar.image('snip.jpeg', use_column_width= True)
    st.image('snip.jpeg', caption= 'Photo by Chris Ried on Unsplash', use_column_width= True)

    menu= ["Latest", "Collections", "Search", "Add", "Manage Snippets"]

    selected=st.sidebar.selectbox("Menu", menu)

    if selected == "Latest":
        st.subheader("Latest Snippets")

    ######################## Menu: Latest #############

        latest=get_latest()
        for i in latest:
            code= '''{}'''.format(i[1])
            st.code(code, language= i[0])

            st.markdown(i[2])


    ######################## Menu: Collection #############
   
    
    elif selected == "Collections":
        st.subheader("Snippet Collections")

        distinct_collections = select_collections()
        distinct_list=["all"]

        for i in distinct_collections:
            for x in range(0, (len(distinct_collections)-1)):
                

                full_selected_collection= select_all_for_collection(i[x])
                distinct_list.append(i[x])

                

                st.markdown(i[x])
                
                for i in full_selected_collection:

                    code= '''{}'''.format(i[1])
                    st.code(code, language= i[0])

                    st.markdown(i[2]) 

        select_collection = st.selectbox("Collections", distinct_list)
        
            




    ################## Search    ######################       
            


    elif selected == "Search":
        st.sidebar.subheader("Search for snippets")

        s_term = st.sidebar.text_input("Search")
        s_criteria = st.sidebar.radio("Pick a criteria", ("Language", "Code Snippet", "Description", "Year", "Collection"))

        if s_criteria == "Language":
            search_criteria = 'language'

        elif s_criteria == "Code Snippet":
            search_criteria = 'code'

        elif s_criteria == "Description":
            search_criteria = 'description'

        elif s_criteria == "Year":
            search_criteria = 'date'

        elif s_criteria == "Collection":
            search_criteria = 'collection'

        if st.sidebar.button('Start search'):
            search_results = search_snip(search_criteria, s_term)
            for i in search_results:
                code= '''{}'''.format(i[1])
                st.markdown(i[2])
                st.code(code, language= i[0])

                

    ######################## Menu: ADD #############

    elif selected == "Add":
        st.subheader("Add snippet")
        create_table()

        d_language = st.text_input("Language")
        d_code = st.text_area("Code Snippet")
        d_description = st.text_input("Description")
        d_collection = st.text_input("Add To Collection")
        d_date = datetime.date.today()

        if st.button('ADD'):
            

            add_table(d_language, d_code, d_description, d_date, d_collection)
            st.success("{} snippet saved" .format(d_language))

    
    ######################## Menu: Manage #############


    elif selected == "Manage Snippets":
        st.subheader('Manage Snippets')
        all_snips = view_all_snippets()
        

        all_snippet_code= [i[2] for i in view_all_snippets()]
        selected_code= st.selectbox("Select a code to delete", all_snippet_code)

        if st.button("Delete"):

            delete_snippet(selected_code)
            st.success("{} snippet deleted" .format(selected_code))

        if st.checkbox("Stats"):
            df= pd.DataFrame(all_snips, columns= ["Language", "Code Snippet", "Description", "Collection", "Date", "n"])
            st.dataframe(df)
            df['Snippet Length']= df["Code Snippet"].str.len()
            df_new = df.fillna(value=0)
        


            df_grouped = df_new.groupby(["Date"])["Description"].count().reset_index()
            df_grouped.replace(0, "2020-09-23", inplace=True)
            # st.dataframe(df_grouped)

            fig_daily = px.bar(x=df_grouped["Date"], y=df_grouped["Description"], title="Number of Daily Snippets Submitted")
            fig_daily.update_xaxes(type='category')
            fig_daily.update_layout(
    font_color="blue",
    title_font_color="red",
    xaxis_title="Date",
    yaxis_title="Total Submissions",
    legend_title_font_color="green"
)

            st.write(fig_daily)


            # Pie chart for programming languages

            df_language_grouped= df_new.groupby(["Language"])["Description"].count().reset_index()
            # st.dataframe(df_language_grouped)

            language_names= [i[0] for i in view_all_snippets()]

            fig_language = px.pie(values=df_language_grouped["Description"], names=df_language_grouped["Language"], title="Programming Languages submitted")
            fig_language.update_layout(
    font_color="blue",
    title_font_color="red",
    legend_title_font_color="green"
)

            st.write(fig_language)





            # fig.update_layout(
            # xaxis = dict(
            # tickmode = 'array',
            # tickvals = [1, 1.5, 2, 2.5, 3, 3.5]
            # dtick = 0.75
            #         )
            #    )

            

        # snippets_posted based on date line chart, to read the line chart (be able to interact with the plot )
        # 







hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__=='__main__':
    main()