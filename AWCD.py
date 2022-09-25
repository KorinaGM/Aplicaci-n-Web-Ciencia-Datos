import pandas as pd 
import streamlit as st
import plotly.express as px 
import plotly.graph_objs as go 

import numpy as np 

#https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Análisis Desempeño - Socialize your Knowledge",
                   page_icon="https://img.freepik.com/premium-vector/sk-logo-design_614408-1406.jpg?w=2000",
                   layout="wide")

df = pd.read_csv('./Employee Data.csv')
df = df.iloc[:, [1,2,3,5,6,7,8,9,10,11,16,17,18,19,20]]


col1,col2, col3 = st.columns([1,1,10])
col1.image("https://img.freepik.com/premium-vector/sk-logo-design_614408-1406.jpg?w=2000", width=140)
col3.title ("Análisis Desempeño - Socialize your Knowledge")    
 
with st.container():           
    st.write("A continuación se presenta un alálisis del desempeño de los colaboradores de Socialize your Knowledge. " \
           + "Con la finalidad de ser consultados por los colaboradores de manera práctica y sencilla, " \
           + "en cualquier momento o lugar; de modo que los involucrados puedan estar atentos a sus fortalezas y " \
           + "áreas de oportunidad y así lograr mejorar su rendimiento alzanzando una mayor calidad de servicios.")

    
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        gender = st.multiselect("Seleccione Genero:",
                                options=df.sort_values(by="gender").gender.unique(),
                                default=df.sort_values(by="gender").gender.unique())
    with col2:
        pd = st.multiselect("Seleccione Puntuaje de Desempeño:",
                            options=df.sort_values(by="performance_score_desc").performance_score_desc.unique(),
                            default=df.sort_values(by="performance_score_desc").performance_score_desc.unique())
    with col3:
        ms = st.multiselect("Seleccione Estado Civil:",
                            options=df.sort_values(by="marital_status").marital_status.unique(),
                            default=df.sort_values(by="marital_status").marital_status.unique())                        
    df_selection = df.query("gender == @gender & performance_score_desc == @pd & marital_status == @ms")                    
    st.markdown("##")

    total_employes = int(df_selection["name_employee"].count())

    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Número de Empleados:")
        st.subheader(total_employes)                
        
    # ------ PUNTUAJES DE DESEMPEÑO -----
    fig1 = px.histogram(df_selection,x="performance_score_desc",
                        title="<b>Puntuajes De Des empeño</b>",                        
                        #color_discrete_sequence=["#0083B8"]*len(df_selection.performance_score.unique()),
                        template="plotly_white",
                        text_auto=True)

    fig1.update_layout(xaxis_title="Puntuaje Desempeño",
                       yaxis_title="Número Empleados")
    
    # ----- Promedio Horas trabajadas por genero. -----
    promedio_ht_genero = (df_selection.groupby(by=["gender"]).mean()[["average_work_hours"]].sort_values(by="gender"))
    fig2=px.bar(promedio_ht_genero,
                x=promedio_ht_genero.index,
                y="average_work_hours",
                orientation="v",
                title="<b>Promedio Horas Trabajadas Por Genero</b>",
                color_discrete_sequence=["#0083B8"]*len(promedio_ht_genero),
                template="plotly_white",
                text_auto=True)
    fig2.update_layout(xaxis_title="Genero",
                       yaxis_title="Promedio Horas Trabajadas")

    # ----- Salarios Por Edades. -----
    salario_edad = (df_selection.groupby(by=["age"]).sum()[["salary"]].sort_values(by="age"))
    fig3=px.bar(salario_edad,
                x=salario_edad.index,
                y="salary",
                orientation="v",
                title="<b>Salarios Por Edades</b>",
                color_discrete_sequence=["#0083B8"]*len(salario_edad),
                template="plotly_white",
                text_auto=True)
    fig3.update_layout(xaxis_title="Edad",
                                   yaxis_title="Salarios")

    # ----- Promedio Horas trabajadas por Puntuaje Desempeño. -----
    promedio_ht_pd = (df_selection.groupby(by=["performance_score_desc"]).mean()[["average_work_hours"]].sort_values(by="performance_score_desc"))
    fig4=px.bar(promedio_ht_pd,
                x=promedio_ht_pd.index,
                y="average_work_hours",
                orientation="v",
                title="<b>Promedio Horas Trabajadas Por Puntuaje De Desempeño</b>",
                color_discrete_sequence=["#0083B8"]*len(promedio_ht_pd),
                template="plotly_white",
                text_auto=True)
    fig4.update_layout(xaxis_title="Puntuajes Desempeño",
                       yaxis_title="Promedio Horas Trabajadas")

    col1, col2 = st.columns(2)    
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)        
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

with st.container():       
    st.subheader("Conclusiónes")    
    st.text("En el análisis anterior se puede observar las siguientes conlusiónes: \n" \
            + "1. El mayor núumero de empleado cumple plenamente con el desempeño que presenta en sus actividades y deberes. \n" \
            + "2. Las mujeres trabajan en promedio alrededor de 26 horas más que los empleados hombres. \n" \
            + "   Siendo mujeres casadas las que aportan el mayor número de horas a dicho promedio. \n"\
            + "3. El top 3 de edades con mejor salario son los empleados 35,38 y 42; \n"\
            + "   mientras que empleados con 60,62 y 68 años reciben los salarios más bajos.\n" \
            + "4. Los empleados que necesitan mejorar su desempeño, \n" \
            + "   trabajan en promedio alrededor de 81 horas mas que la mayoria de los empleados que cumplen con dicho desempeño. \n" \
            + "   y 62 horas más que los empleados que exceden dicho desempeño.")