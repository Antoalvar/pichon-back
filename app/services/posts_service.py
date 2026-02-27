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
    def get_post_by_id(post_id):
        """
        Obtiene un post específico por su ID.
        Args:
            post_id (str): ID del post
        Returns:
            dict: Registro del post o None si no existe
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
                p.categories AS category_name,
                p.content
            FROM posts p
            WHERE p.id = %s;
        """
            cur.execute(select_query, (post_id,))
            record = cur.fetchone()
            cur.close()
            conn.close()
            return record
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
    def update_post(post_id, fields):
        """
        Actualiza parcialmente un post con los campos proporcionados.
        Args:
            post_id (str): ID del post a actualizar
            fields (dict): Diccionario con los campos a actualizar
        Returns:
            bool: True si se actualizó, False si no existía
        """
        if not fields:
            raise Exception("No se proporcionaron campos para actualizar")

        column_map = {
            "title": "title",
            "abstract": "abstract",
            "img": "thumbnail_url",
            "categories": "categories",
            "prod": "is_published",
            "content": "content",
        }

        set_clauses = []
        values = []

        for key, value in fields.items():
            if key not in column_map:
                raise Exception(f"Campo no permitido: '{key}'")
            set_clauses.append(f"{column_map[key]} = %s")
            values.append(value)

        if "title" in fields:
            set_clauses.append("slug = %s")
            values.append(fields["title"].lower().replace(" ", "-"))

        values.append(post_id)
        update_query = f"UPDATE posts SET {', '.join(set_clauses)} WHERE id = %s"

        try:
            conn = PostsService.get_connection()
            cur = conn.cursor()
            cur.execute(update_query, values)
            updated = cur.rowcount > 0
            conn.commit()
            cur.close()
            conn.close()
            return updated
        except psycopg2.Error as e:
            raise Exception(f"Error al actualizar el post: {str(e)}")

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
                deleted = cur.rowcount > 0
                conn.commit()
                cur.close()
                conn.close()
                return deleted
            except psycopg2.Error as e:
                raise Exception(f"Error al eliminar el post: {str(e)}")
    """Servicio para manejar operaciones de posts en la base de datos PostgreSQL."""
