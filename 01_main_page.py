import streamlit as st

st.set_page_config(page_title="Main Page", page_icon="🍫")
st.title("Finding the Best Chocolate 🍫")
st.write("""Here I am going to represent my findings by analyzing a 
           dataset containing rating of over 2500 plain dark chocolate 
           bars collected from different countries. The dataset is collected from 
           [here](http://flavorsofcacao.com/chocolate_database.html). """)

st.markdown(
    """
    ### 💾 The Data:
    **Column Name**|**Description**
    -----|-----
    |ref| id number of the review|
    |Company (Manufacturer)| Name of the bar manufacturer|
    |Company Location| Location of the manufacturer|
    |Review Date| From 2006 to 2021|
    |Country of Bean Origin| Country of origin of the cacao beans|
    |Specific Bean Origin or Bar Name| Name of the chocolate bar|
    |Cocoa Percentage| Cocoa content of the bar (%)|
    |Ingredients| B (Beans), S (Sugar), S* (Sweetener other than sugar or beet sugar), C(Cocoa Butter), (V) Vanilla, (L) Lecithin, (Sa) Salt
    |Most Memorable Characteristics| Summary of most memorable characteristics of the chocolate bar
    |Ratings| 1.0-1.9 Unpleasant, 2.0-2.9 Disappointing, 3.0-3.49 Recommended, 3.5-3.9 Highly Recommended, 4.0-5.0 Outstanding
    """
)
st.text("")
st.markdown(
    """
        ### 💪 Challenge:
        ##### Here I am creating a report to summarizing my research including:
         - What is the average rating by country of origin?
         - How many bars were reviewed for each of those countries?
         - Which chocolate got the good average rating?
         - Which manufacturer got good average rating?
         - How does cocoa content relate to rating? What is the average cocoa content for
           bars with higher ratings (above 3.5)?
         -  My research indicates that some consumers want to avoid bars with lecithin.
            Compare the average rating of bars with and without lecithin (L in the ingredients). 
    """
)
