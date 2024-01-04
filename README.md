Proyecto final del curso de data science de Codenotch (Diciembre 2023).
En este proyecto se ha realizado un estudio de las reservas hoteleras en dos hoteles en Portugal desde 01/07/2015 a 31/08/2017: uno tipo urbano en Lisboa y un resort en la región del Algarve. Los datos se han obtenido de Kaggle (https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand).
Nuestro principal objetivo era determinar si existe una correlacion entre las cancelaciones y los datos meteorológicos, los cuales se han obtenido en la API de meteorologia Visual Crossing (https://www.visualcrossing.com/).
Una vez realizado el análisis se plantea un modelo de machine learning para determinar si una reserva será cancelada o no. 
Hemos separado el set de datos en dos subsets (train y test), de manera que el los datos "train" van de 01/07/2015 a 30/06/2017 y los datos "test" de 01/07/2017 a 31/08/2017. 
Se ha utilizado el subset "train" (previmente balanceado) para entrenar un algoritmo de clasificacion XGBoost, obteniendo un "accuracy score" de 0.71 en el set de datos 'test'. 
Finalmente, se ha realizado una aplicacion de streamlit en la que se visualizan los datos mediante PowerBI y se pueden realizar inferencias para el modelo de machine learning. 

Rafael Castro Gálvez y Martí Foix Pérez
