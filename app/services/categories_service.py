import psycopg2
from psycopg2.extras import RealDictCursor
from app.db import get_connection, release_connection

class CategoriesService:
    """Servicio para manejar operaciones de categorías en la base de datos PostgreSQL."""


    @staticmethod
    def get_all_categories():
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            select_query = "SELECT id, name, slug, \"order\" FROM categories ORDER BY \"order\" ASC, id ASC;"
            cur.execute(select_query)
            categories = cur.fetchall()
            cur.close()
            return categories
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
        finally:
            release_connection(conn)

    @staticmethod
    def create_category(name, slug, order):
        conn = get_connection()
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO categories (name, slug, "order")
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            cur.execute(insert_query, (name, slug, order))
            category_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return category_id
        except psycopg2.IntegrityError as _e:
            raise Exception("El nombre o slug ya existe")
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
        finally:
            release_connection(conn)

    @staticmethod
    def delete_category(category_id):
        """
        Elimina una categoría por su ID.
        Args:
            category_id (str): ID de la categoría a eliminar
        Returns:
            bool: True si se eliminó, False si no existía
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            delete_query = "DELETE FROM categories WHERE id = %s"
            cur.execute(delete_query, (category_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            cur.close()
            return deleted
        except psycopg2.Error as e:
            raise Exception(f"Error al eliminar la categoría: {str(e)}")
        finally:
            release_connection(conn)
