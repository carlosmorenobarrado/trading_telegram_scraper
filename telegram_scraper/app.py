import asyncio
import logging
import json # Importar la librería json
from datetime import datetime, timezone
from telethon.sync import TelegramClient
from telethon.tl.types import Channel, InputPeerChannel
from telethon.tl.functions.channels import GetForumTopicsRequest
import psycopg2
DB_HOST = "192.168.1.237"
DB_NAME = "criptodb"
DB_USER = "admincar"
DB_PASSWORD = "1234car"
DB_PORT = "5432"
SSL_MODE = 'require' 
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        #sslmode=SSL_MODE, 
    )
    cur = conn.cursor()
    print(f"Intentando conectar a PostgreSQL en {DB_HOST}:{DB_PORT}...")
    
except psycopg2.Error as e:
    print(f"Error al conectar o interactuar con la base de datos: {e}")
# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DE TELEGRAM (¡Tus credenciales!) ---
API_ID = 25407010
API_HASH = '9e8c88514b9a18a9a0c9b408b667f2fd'
PHONE_NUMBER = '+34616187287'
SESSION_NAME = 'my_telegram_session' # Manteniendo el nombre de sesión solicitado

# --- CONFIGURACIÓN DEL GRUPO Y TEMA ESPECÍFICOS ---
TARGET_GROUP_ID = -1002383848783 # ¡Asegúrate de que este ID es el correcto para tu supergrupo!
TARGET_TOPIC_NAME = "IDEAS CORTO PLAZO/AT"

# Función auxiliar para serializar objetos datetime y bytes a JSON
def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code.
    Converts datetime objects to ISO format strings and bytes to hex.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.hex()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# --- Función Asíncrona Principal ---
async def get_and_save_latest_topic_messages(num_messages_to_fetch=15):
    """
    Conecta a Telegram, encuentra el topic especificado y obtiene los últimos N mensajes.
    Guarda cada mensaje en un archivo JSON individual en la misma carpeta.
    No interactúa con la base de datos. Diseñado para usar en un notebook.
    """
    topic_id = None
    group_entity = None
    messages_data_list = [] 

    # Conjunto para evitar procesar IDs duplicados si el iterador los entrega más de una vez
    processed_ids_in_run = set()

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        try:
            logging.info("Iniciando cliente de Telegram...")
            await client.start(phone=PHONE_NUMBER)
            logging.info("Cliente de Telegram conectado exitosamente.")

            # --- 1. Obtener la entidad del grupo principal ---
            try:
                group_entity = await client.get_entity(TARGET_GROUP_ID)
                if not isinstance(group_entity, Channel):
                    logging.error(f"El ID {TARGET_GROUP_ID} no corresponde a un Canal/Supergrupo. Tipo de entidad: {type(group_entity)}. Verifica el ID.")
                    return # No devolver nada si hay error
                logging.info(f"Entidad del grupo principal obtenida: {getattr(group_entity, 'title', 'N/A')} (ID: {group_entity.id}).")
            except Exception as e:
                logging.error(f"¡Error! No se pudo obtener la entidad del grupo principal {TARGET_GROUP_ID}: {e}. Asegúrate de que el ID del grupo es correcto y eres miembro de él.")
                return

            # --- 2. Buscar el ID del topic ---
            try:
                input_channel_for_topics = InputPeerChannel(group_entity.id, group_entity.access_hash)
                topics_result = await client(GetForumTopicsRequest(
                    channel=input_channel_for_topics,
                    offset_date=0, offset_id=0, offset_topic=0, limit=200
                ))
                for topic in topics_result.topics:
                    if topic.title == TARGET_TOPIC_NAME:
                        topic_id = topic.id
                        logging.info(f"ID encontrado para el topic a filtrar '{TARGET_TOPIC_NAME}': {topic_id}")
                        break

                if topic_id is None:
                    logging.error(f"El topic '{TARGET_TOPIC_NAME}' no se encontró en el grupo. No se puede obtener mensajes.")
                    return
            except Exception as e:
                logging.error(f"Error al buscar el topic '{TARGET_TOPIC_NAME}': {e}. No se puede obtener mensajes.")
                return

            # --- 3. Obtener los últimos N mensajes del topic y guardar ---
            logging.info(f"Obteniendo los últimos {num_messages_to_fetch} mensajes del topic '{TARGET_TOPIC_NAME}' (ID: {topic_id})...")

            async for message in client.iter_messages(
                entity=group_entity,
                limit=num_messages_to_fetch, # Limitamos directamente aquí a 15 mensajes
                reverse=False, # Los más recientes primero
                reply_to=topic_id
            ):
                message_raw_data = message.to_dict()
                message_raw_data['filtered_topic_id'] = topic_id
                if 'message' in message_raw_data.keys():
                    id = message_raw_data['id']
                    message_date = message_raw_data['date']
                    message_text = message_raw_data['message']
                    edit_date = message_raw_data['edit_date']
                    insert_sql = """
                                INSERT INTO bolsazone.messages (message_id, date, message_text, edit_date, ts_insert, ts_update)
                                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, null)
                                ON CONFLICT (message_id) DO UPDATE SET
                                    message_id = EXCLUDED.message_id,
                                    date = EXCLUDED.date,
                                    message_text = EXCLUDED.message_text,
                                    edit_date = EXCLUDED.edit_date,
                                    ts_update = CURRENT_TIMESTAMP; 
                                """
                    cur.execute(insert_sql, (id, message_date, message_text, edit_date))
                    conn.commit()
                else:
                    continue
            logging.info(f"Proceso de obtención y guardado de mensajes finalizado.")

        except Exception as e:
            logging.critical(f"¡Error crítico en la ejecución del script!: {e}")
        finally:
            pass 

    return messages_data_list

#NOTEBOOK 
#await get_and_save_latest_topic_messages(num_messages_to_fetch=300)
#if 'conn' in locals() and conn:
#    conn.close()

if __name__ == "__main__":
    try:
        asyncio.run(get_and_save_latest_topic_messages(num_messages_to_fetch=5))
    except RuntimeError as re:
        if "cannot run an event loop while another loop is running" in str(re):
            logging.error("Ya hay un bucle de eventos de asyncio ejecutándose. Esto puede pasar en entornos como IPython/Jupyter si el bucle no se cerró correctamente.")
        else:
            raise re # Vuelve a lanzar el error si es algo diferente
    except Exception as e:
        logging.critical(f"Error al iniciar el bucle asíncrono: {e}")
    finally:
        # Cerrar la conexión a la base de datos al finalizar todo el script
        if cur:
            cur.close()
            logging.info("Cursor de DB cerrado.")
        if conn:
            conn.close()
            logging.info("Conexión a la base de datos cerrada.")