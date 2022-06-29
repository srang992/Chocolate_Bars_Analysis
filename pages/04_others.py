import streamlit as st
from functions import ThirdPageFuncs

st.set_page_config(layout='wide', page_icon="📓")
st.title(
    """
    Comparison between Chocolates containing Lecithin and Chocolates not containing Lecithin
    """
)

st.markdown(
    """
    While researching about the ingredients used in dark chocolate bars, I noticed that some people try to 
    ignore the chocolates containing Lecithin as it has an allergic effect. Normally Lecithin is used to bind the
    chocolate ingredients like cocoa butter, sugar, milk together. Let's see if this ignorance is reflected in 
    the dataset.
    """
)

tpf = ThirdPageFuncs()

figure_1 = tpf.lecithin_ignorance()
figure_2 = tpf.rating_by_bean_origin()
figure_3 = tpf.num_of_chocos_in_country()

st.plotly_chart(figure_1, use_container_width=True)

st.markdown(
    """
    From the above result, we can easily see that the average rating for chocolate with lecithin is less than the 
    average rating for chocolate without lecithin.
    """
)

st.title("Average Rating by Bean Origin and the number of bars reviewed for each of those countries")
st.markdown("""Here I am going to show the average rating of chocolate bars 
               according to their bean origin country and the number of reviewed
               chocolate in each of them""")

col1, col2 = st.columns([1, 1])

col1.plotly_chart(figure_2, use_container_width=True)
col2.plotly_chart(figure_3, use_container_width=True)

