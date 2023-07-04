import sqlite3
from typing import Any


class Manager:
    def __init__(self) -> None:
        self.database = sqlite3.connect("fashion.db")

    def manager(
        self,
        sql,
        *args,
        commit: bool = False,
        fetchone: bool = False,
        fetchall: bool = False,
    ) -> Any:
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            elif fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()
        return result

    def get_table_columns_names(self, table_name: str) -> list[str]:
        cursor = self.database.cursor()
        sql = f"select * from {table_name}"
        data = cursor.execute(sql).description
        return [item[0] for item in data]

    def format_table_columns_names(
        self, table_name: str, excluded_columns: list[str]
    ) -> list[str]:
        columns = self.get_table_columns_names(table_name)
        return [item for item in columns if item not in excluded_columns]


class TableCreator(Manager):
    def create_user_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100),
                phone_number VARCHAR(13),
                telegram_id BIGINT NOT NULL UNIQUE
            );
        """
        self.manager(sql, commit=True)
        print("Таблица создалась")

        # метод для создания таблиц категорий

    def create_category_table(self) -> None:
        sql = """
               CREATE TABLE IF NOT EXISTS category(
                   category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name VARCHAR(100)
               );
           """
        self.manager(sql, commit=True)
        print("Таблица создалась")

        # метод для создания таблиц услуг

    def create_service_table(self) -> None:
        sql = """
               CREATE TABLE IF NOT EXISTS service(
                   service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name VARCHAR(100),
                   content TEXT,
                   price INTEGER,
                   photo TEXT,
                   category_id INTEGER REFERENCES category(category_id)
               );
           """
        self.manager(sql, commit=True)
        print("Таблица создалась")

        # метод для создания таблиц мастеров

    def create_master_table(self) -> None:
        sql = """
               CREATE TABLE IF NOT EXISTS master(
                   master_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   full_name VARCHAR(80),
                   content VARCHAR(250),
                   photo TEXT,
                   price INTEGER,
                   is_working BOOL DEFAULT true,
                   service_id INTEGER REFERENCES service(service_id)
               );
           """
        self.manager(sql, commit=True)
        print("Таблица создалась")

        # метод для создания таблиц, времени работы мастеров

    def create_work_time_table(self) -> None:
        sql = """
               CREATE TABLE IF NOT EXISTS work_time(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   from_hours VARCHAR(5),
                   to_hours VARCHAR(5),
                   master_id INTEGER REFERENCES master(master_id)
               );
           """
        self.manager(sql, commit=True)
        print("Таблица создалась")

    def create_cart_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS cart(
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                total_price INTEGER DEFAULT 0,

                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            """
        self.manager(sql, commit=True)

    def create_cart_products_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS cart_products(
                cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cart_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                master_id INTEGER NOT NULL,

                day VARCHAR(30),
                added_time VARCHAR(30),
                price INTEGER,

                FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
                FOREIGN KEY (service_id) REFERENCES service(service_id),
                FOREIGN KEY (master_id) REFERENCES master(master_id),

                UNIQUE(cart_id, service_id)
            );
        """
        self.manager(sql, commit=True)

    def create_faq_table(self) -> None:
        sql = """
            --sql
            CREATE TABLE IF NOT EXISTS faq (
                faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT
            );
        """
        self.manager(sql, commit=True)
