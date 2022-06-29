import streamlit as st
from functions import SecondPageFuncs

st.set_page_config(layout='wide', page_title='Best Manufacturer', page_icon="🏭")
st.title("Which manufacturer got good average rating?")
st.write(
    """
    In business, trust is a very big thing. We always want to buy products of 
    a specific company on whom we can trust. Let's see who is lucky here.
    """
)

spf = SecondPageFuncs()

figure_1 = spf.best_manufacturer()
figure_2 = spf.bean_provider()
figure_3 = spf.choco_tastes()
figure_4 = spf.cocoa_percentage()

col_0_0, col_0_1 = st.columns([1, 1])
col_1_0, col_1_1 = st.columns([1, 1])

col_0_0.plotly_chart(figure_1, use_container_width=True)
col_0_1.plotly_chart(figure_2, use_container_width=True)
col_1_0.plotly_chart(figure_3, use_container_width=True)
col_1_1.plotly_chart(figure_4, use_container_width=True)
# st.dataframe(spf.soma_choco_dataframe())

st.markdown(
    """
    From the above results, we can see that:
     - **Soma ChocoMaker** got the highest average ratings 
       among all of the manufacturer **(Top Left)**. If you search in google by typing "soma chocolate canada", 
       you can see that it also got a good google reviews too. 
     - If we try to find the country of bean origin for soma chocomaker, you can see a name "Blend", which is not 
       a country. It just means that the chocolate bars are made of different cocoa beans. And, maximum chocolate bars 
       of soma chocomaker are made by blending different cocoa beans **(Top Right)**. 
     - The most memorable taste of chocolate bars made by soma chocomaker is **Creamy** **(Bottom Left)**. 
     - The chocolate bars of Soma Chocomaker mostly consisting of 70% cocoa **(Bottom Right)**.
    """
)