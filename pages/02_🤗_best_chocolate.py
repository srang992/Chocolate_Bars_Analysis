import streamlit as st
from functions import FirstPageFuncs

st.set_page_config(layout='wide', page_title='Best Chocolate', page_icon='🤗')
st.title("Which chocolate has good average rating and what is the characteristic of that chocolate?")
st.write(
    """
    Here we find out that which chocolate bar got the best average rating among all of them. We also
    find out why this chocolate is so popular. 
    """
)

col_0_0, col_0_1 = st.columns([1.25, 1])
col_1_0, col_1_1 = st.columns([1, 1])

fpf = FirstPageFuncs()
figure_1 = fpf.best_chocolates()
figure_2 = fpf.most_common_company_location()
figure_3 = fpf.most_commonly_used_ingredients()
figure_4 = fpf.most_memorable_taste()

col_0_0.plotly_chart(figure_1, use_container_width=True)
col_0_1.plotly_chart(figure_2, use_container_width=True)
col_1_0.plotly_chart(figure_3, use_container_width=True)
col_1_1.plotly_chart(figure_4, use_container_width=True)

st.markdown(
    """
    From the above results, we can clearly see that the chocolate named **Kokoa Kamili** got the highest average rating
    (Top Left). This chocolate mostly manufactured in **U.S.A.**(Top Right) and the most commonly used ingredients are
    **Beans, Sugar and Cocoa Butter**. Sometimes, **Cocoa Butter** is not used (Bottom Left). This chocolate is mostly 
    popular for it's **fruity** taste (Bottom Right).
    """
)
