# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Se importa la función col para FRUIT_NAME
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# st.text(smoothiefroot_response.json())

# Write directly to the app
st.title("Personaliza Tu Smoothie :cup_with_straw:")
st.write(
  """Escoge las frutas que quieras en tu Smothie personalizado!
  """
)

# Add a Name Box for Smoothie Orders
# st.write("Tu fruta favorita es:", option)
name_on_order = st.text_input("Nombre en el Smoothie:")

if name_on_order:
    name_on_order = name_on_order.strip().capitalize()
else:
    name_on_order = ""

st.write("El nombre en tu Smoothie será:", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the snowpark Dataframe to a pandas Dataframe so we can use the loc function
pd_df= my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect('Escoge hasta 5 ingredientes:', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # In order to convert the list to a string, e need to first create a variable and
    # w then make sure Python thinks it contains a string.
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
  
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)

        

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',' """ + name_on_order + """')"""
    
    #Se quitan los espacios
    my_insert_stmt = my_insert_stmt.strip().replace(" ", "_")
    st.write(my_insert_stmt)
  
    time_to_insert = st.button('Realizar pedido')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Tu Smoothie ha sido pedido!', icon="✅")

