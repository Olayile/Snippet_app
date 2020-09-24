import streamlit as st
import sqlite3
import datetime


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

# def add_column():
#     c.execute("ALTER TABLE snippet_table ADD COLUMN collection TEXT")
#     con.commit()


##################################Layout template



def main():
    
    
    st.title("Snippet Search")
    st.sidebar.image('snip.jpeg', use_column_width= True)
    st.image('snip.jpeg', use_column_width= True)

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

        for i in distinct_collections:
            for x in range(0, (len(distinct_collections)-1)):
                

                full_selected_collection= select_all_for_collection(i[x])

                st.markdown(i[x])

                for i in full_selected_collection:
                    code= '''{}'''.format(i[1])
                    st.code(code, language= i[0])

                    st.markdown(i[2]) 

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




hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__=='__main__':
    main()