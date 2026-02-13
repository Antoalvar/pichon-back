import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from config import Config

class PostsService:
    """Servicio para manejar operaciones de posts en la base de datos PostgreSQL."""

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
            conn = PostsService.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            select_query = """
            SELECT
                p.id,
                p.title,
                p.abstract,
                p.thumbnail_url,
                p.published_at,
                c.name AS category_name
            FROM posts p
            JOIN categories c ON p.category_id = c.id
            WHERE p.is_published = true
            ORDER BY p.published_at DESC;
        """
            cur.execute(select_query)
            records = cur.fetchall()
            cur.close()
            conn.close()
            return records
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            raise Exception(f"Error en la base de datos Pichón: {str(e)}")

    @staticmethod
    def create_post(title, abstract, img, categories, prod, body, post_id=None):
        """
        Crea un nuevo post con todos los campos necesarios.
        Args:
            title (str): Título
            abstract (str): Resumen
            img (str): URL de la imagen
            categories (list): Lista de categorías
            prod (bool): Indicador de producción
            body (str): Contenido HTML del post
            post_id (str, optional): ID personalizado. Si no se proporciona, se genera uno.
        Returns:
            str: ID del post creado
        """
        post_id = post_id or str(uuid.uuid4())
        try:
            conn = PostsService.get_connection()
            cur = conn.cursor()
            insert_query = """
                INSERT INTO posts (id, title, abstract, thumbnail_url, categories, is_published, body)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                post_id,
                title,
                abstract,
                img,
                categories,
                prod,
                body
            ))
            conn.commit()
            cur.close()
            conn.close()
            return post_id
        except psycopg2.IntegrityError as _e:
            raise Exception("El ID ya existe")
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
