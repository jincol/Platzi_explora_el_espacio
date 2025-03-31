from airflow.models import BaseOperator  #La clase que permite crear custoom Operator
from airflow.utils.context import Context #
from airflow.hooks.base import BaseHook
import smtplib
from email.mime.text import MIMEText

class customer_operator (BaseOperator):

    def __init__(self,subject,mensaje,to_email,conn_id='gmail_default',**kwargs):
        super().__init__(**kwargs)
        self.subject=subject
        self.mensaje = mensaje
        self.to_email = to_email
        self.con_id = conn_id

    def execute(self,context):
        #Obtener configuracion de conexion de UI de airflow
        conn = BaseHook.get_connection(self.con_id)
        from_email = conn.login
        password = conn.password

        #renderizar asunto y mensaje con datos del contexto ed DAG
        render_subject = self.subject.format(**context)
        render_message = self.mensaje.format(**context)

        #crear correo 
        msg = MIMEText(render_message)
        msg["Subject"]  = render_subject
        msg["From"]  = from_email
        msg["To"]  = self.to_email

        #crear conexion gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password )
            server.sendmail(from_email, self.to_email, msg.as_string()) #msg.as_string() convierte el mensaje a string

        self.log.info(f"Correo enviado a {self.to_email} exitosamente.")