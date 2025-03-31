from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
#CUSTOM OPERATOR
from custom_operator import customer_operator

def respuesta_sat (**kwargs):
    import pandas as pd

    data = pd.DataFrame({"student": ["Maria Cruz", "Daniel Crema","Elon Musk","Karol Castrejon","Freddy Vega"],
                         "timestamp": [kwargs['logical_date']]*5})
    data.to_csv(f"/tmp/platzi_data_{kwargs['ds_nodash']}.csv",  header=True)

def lectura_df(**kwargs):
    import pandas as pd

    path = f"/tmp/platzi_data_{kwargs['ds_nodash']}.csv"
    df = pd.read_csv(path)
    print(df)


default_args = {
    'owner': 'airflow', #Identificador de Ejecutor
    'email': ['jincolcha@gmail.com'], 
    'email_on_failure': True,  # Envio de Email en deteccion de fallas
    'email_on_retry': False, #Reintentos de Envios en caso de fallas
    'retries': 1  #Numero de reintentos
}

with DAG(
    dag_id= "dag_space",
    description = "Este Dag sera para el proyecto Platzi Space",
    default_args=default_args,
    schedule_interval="@daily",
    start_date= datetime(2025,3,1),
    end_date=datetime(2025,3,5),
    catchup = True ) as dag:

    #Autorizaciond de la nasa
    aut_naza = BashOperator(
        task_id="Autorizacion_Nasa",
        bash_command='sleep 5 && echo "OK" > /tmp/response_{{ds_nodash}}.txt')   

    #SENSOR
    sensor_verify = FileSensor(
        task_id="sensor_verify",
        filepath= "/tmp/response_{{ds_nodash}}.txt",
        poke_interval = 4,
        timeout=12,
        mode="reschedule"
    )

    #Obtiene los datos de SPACE X
    obtiene_datos = BashOperator(
        task_id="Obtener_datos",
        bash_command="curl -o /tmp/history.json -L 'https://api.spacexdata.com/v4/history'",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    #operatdor python simulando datos
    datos_simulation = PythonOperator(
        task_id = "simulacion_python",
        python_callable=respuesta_sat
    )


    #Custom Task de Envio de Email
    email = customer_operator(
        task_id="enviar_correo",
        subject="Ejecución del DAG en la fecha {ds}",
        mensaje="Hola equipo,\n\nLa ejecución para el DAG del día {ds} ha sido completada exitosamente.\n\nSaludos.",
        to_email="jincolcha@gmail.com",
        conn_id="gmail_conn",  # Este es el ID de tu conexión SMTP en Airflow UI
    )


    aut_naza >> sensor_verify >> obtiene_datos >> datos_simulation >> lectura_df_task>>email