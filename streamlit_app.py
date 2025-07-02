# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Se importa la función col para FRUIT_NAME
from snowflake.snowpark.functions import col
import requests


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)


# Write directly to the app
st.title("Personaliza Tu Smoothie :cup_with_straw:")
st.write(
  """Escoge las frutas que quieras en tu Smothie personalizado!
  """
)

#option = st.selectbox(
#    "Cuál es tu fruta favorita?",
#    ("Fresas", "Plátano", "Duraznos"),
#)


# Add a Name Box for Smoothie Orders
# st.write("Tu fruta favorita es:", option)
name_on_order = st.text_input("Nombre en el Smoothie:")
st.write("El nombre en tu Smoothie será:", name_on_order)



# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect('Escoge hasta 5 ingredientes:', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # In order to convert the list to a string, e need to first create a variable and
    # w then make sure Python thinks it contains a string.
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',' """ + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Realizar pedido')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Tu Smoothie ha sido pedido!', icon="✅")
      
