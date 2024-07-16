# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you  want  in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The Name on Your Smoothie will be:",name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# converting snowflake dataframe to  the pandas dataframe 
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()



ingredients_list = st.multiselect(
    "choose up to 5 ingradients: ",my_dataframe
)

if ingredients_list:
   
    
    ingredients_string = ''
    for fruit_selected in ingredients_list:
        ingredients_string+=fruit_selected+" "
        st.subheader(fruit_selected +"Nutrition information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_selected)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")



    
        




