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
                p.slug,
                p.abstract,
                p.thumbnail_url,
                p.published_at,
                p.categories AS category_name
            FROM posts p
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
    def create_post(title, abstract, img, categories, prod, content):
        """
        Crea un nuevo post con todos los campos necesarios.
        Args:
            title (str): Título
            abstract (str): Resumen
            img (str): URL de la imagen
            categories (list): Lista de categorías
            prod (bool): Indicador de producción
            content (str): Contenido HTML del post
        Returns:
            str: ID del post creado
        """
        from datetime import datetime
        published_at = datetime.utcnow()
        slug = title.lower().replace(' ', '-')
        post_id = str(uuid.uuid4())
        try:
            conn = PostsService.get_connection()
            cur = conn.cursor()
            insert_query = """
                INSERT INTO posts (id, title, slug, abstract, thumbnail_url, categories, is_published, published_at, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                post_id,
                title,
                slug,
                abstract,
                img,
                categories,
                prod,
                published_at,
                content
            ))
            conn.commit()
            cur.close()
            conn.close()
            return post_id
        except psycopg2.IntegrityError as _e:
            raise Exception(f"Error de integridad: {str(_e)}")
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")



    @staticmethod
    def delete_post(post_id):
            """
            Elimina un post por su ID.
            Args:
                post_id (str): ID del post a eliminar
            Returns:
                bool: True si se eliminó, False si no existía
            """
            try:
                conn = PostsService.get_connection()
                cur = conn.cursor()
                delete_query = "DELETE FROM posts WHERE id = %s"
                cur.execute(delete_query, (post_id,))
                conn.commit()
                cur.close()
                conn.close()
                return True
            except psycopg2.Error as e:
                raise Exception(f"Error al eliminar el post: {str(e)}")
    """Servicio para manejar operaciones de posts en la base de datos PostgreSQL."""
