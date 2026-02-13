import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class CategoriesService:
    """Servicio para manejar operaciones de categorías en la base de datos PostgreSQL."""

    @staticmethod
    def get_all_categories():
        try:
            conn = CategoriesService.get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            select_query = "SELECT id, name, slug, \"order\" FROM categories ORDER BY \"order\" ASC, id ASC;"
            cur.execute(select_query)
            categories = cur.fetchall()
            cur.close()
            conn.close()
            return categories
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")

    @staticmethod
    def get_connection():
        return psycopg2.connect(Config.POSTGRES_URI)

    @staticmethod
    def create_category(name, slug, order):
        try:
            conn = CategoriesService.get_connection()
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
            conn.close()
            return category_id
        except psycopg2.IntegrityError as _e:
            raise Exception("El nombre o slug ya existe")
        except psycopg2.Error as e:
            raise Exception(f"Error en la base de datos: {str(e)}")
