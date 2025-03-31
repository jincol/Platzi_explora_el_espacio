# 🚀 Proyecto Airflow: Platzi Explora el Espacio

Este proyecto es parte del curso de Airflow en Platzi. Simula el acceso a un satélite educativo lanzado por Platzi y la recolección de datos tanto del satélite como de la API pública de SpaceX. Además, envía una alerta por correo al finalizar el flujo.

## 📦 Estructura del Proyecto

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠️ Funcionalidades del DAG

1. Espera autorización de la NASA simulada con `BashOperator`.
2. Usa un `FileSensor` para verificar la creación del archivo de autorización.
3. Descarga eventos históricos de SpaceX desde su API pública.
4. Simula generación de datos de estudiantes usando `PythonOperator`.
5. Lee y muestra los datos generados.
6. Envía un correo de alerta a los equipos con información sobre la ejecución.

---

## 📧 Configuración del Correo (SMTP)

Para que el operador personalizado (`CustomerOperator`) pueda enviar correos desde Gmail:

### 1. Crear una conexión en Airflow UI

- Ir a: **Admin → Connections**
- Crear una nueva conexión:
  - **Conn Id:** `gmail_conn`
  - **Conn Type:** `SMTP`
  - **Host:** `smtp.gmail.com`
  - **Port:** `465`
  - **Login:** `tu_correo@gmail.com`
  - **Password:** [una contraseña de aplicación de Gmail](https://support.google.com/accounts/answer/185833)
  - **Use SSL:** ✅ (marcado)

### 2. Opcional: Configuración en `airflow.cfg` (si no usas Airflow UI)

Agrega lo siguiente al archivo `airflow.cfg` (o como variables de entorno):

```ini
[email]
email_backend = airflow.utils.email.send_email_smtp
smtp_host = smtp.gmail.com
smtp_starttls = False
smtp_ssl = True
smtp_user = tu_correo@gmail.com
smtp_password = tu_contraseña_de_aplicación
smtp_port = 465
smtp_mail_from = tu_correo@gmail.com
