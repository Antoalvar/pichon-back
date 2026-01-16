import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from config import Config


class PichonDBService:
    """Servicio para manejar operaciones con la base de datos PostgreSQL."""

    @staticmethod
    def get_connection():
        """
        Establece una conexión a PostgreSQL.
        
        Returns:
            psycopg2.connection: Conexión a la base de datos
        """
        return psycopg2.connect(Config.POSTGRES_URI)

    @staticmethod
    def get_all_index():
        """
        Obtiene todos los registros de la tabla index.
        
        Returns:
            list: Lista de registros (diccionarios)
        """
        try:
            conn = PichonDBService.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            select_query = "SELECT * FROM index"
            cur.execute(select_query)

            records = cur.fetchall()

            cur.close()
            conn.close()

            return records

        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")

    @staticmethod
    def insert_index(entry_id, img, title, abstract, categories_str, prod):
        """
        Inserta un nuevo registro en la tabla index.
        
        Args:
            entry_id (str): ID único del registro
            img (str): URL de la imagen
            title (str): Título
            abstract (str): Resumen
            categories_str (str): Categorías (separadas por comas)
            prod (bool): Indica si está en producción
        
        Raises:
            Exception: Si ocurre un error en la base de datos
        """
        try:
            conn = PichonDBService.get_connection()
            cur = conn.cursor()

            insert_query = """
                INSERT INTO index (id, img, title, abstract, categories, prod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cur.execute(insert_query, (entry_id, img, title, abstract, categories_str, prod))
            conn.commit()

            cur.close()
            conn.close()

        except psycopg2.IntegrityError as e:
            raise Exception("El ID ya existe")
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")


class IndexService:
    """Servicio de negocio para operaciones de index."""

    @staticmethod
    def get_all_indexes():
        """
        Obtiene todos los índices y formatea las categorías.
        
        Returns:
            list: Lista de índices formateados
        """
        records = PichonDBService.get_all_index()
        result = []

        for record in records:
            record_dict = dict(record)
            # Convertir string de categorías a lista
            if record_dict.get('categories'):
                record_dict['categories'] = record_dict['categories'].split(',')
            result.append(record_dict)

        return result

    @staticmethod
    def create_index(img, title, abstract, categories, prod, entry_id=None):
        """
        Crea un nuevo índice con validación y generación de ID si es necesario.
        
        Args:
            img (str): URL de la imagen
            title (str): Título
            abstract (str): Resumen
            categories (list): Lista de categorías
            prod (bool): Indicador de producción
            entry_id (str, optional): ID personalizado. Si no se proporciona, se genera uno.
        
        Returns:
            str: ID del registro creado
        """
        entry_id = entry_id or str(uuid.uuid4())
        categories_str = ','.join(categories) if isinstance(categories, list) else categories

        PichonDBService.insert_index(entry_id, img, title, abstract, categories_str, prod)

        return entry_id
