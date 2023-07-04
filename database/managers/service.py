from typing import Optional

from .base import Manager


class ServiceManager(Manager):
    def add_service(self, name: str, content: str, price: int, photo: str, category_id: int) -> None:
        sql = "insert into service(name, content, price, photo, category_id) values (?, ?, ?, ?, ?);"
        self.manager(sql, name, content, price, photo, category_id, commit=True)

    def get_services_name(self, category_id: Optional[int] = None) -> list[tuple]:
        if not category_id:
            sql = "select name from service;"
            return self.manager(sql, fetchall=True)

        sql = "select name from service where category_id = ?;"
        return self.manager(sql, category_id, fetchall=True)

    def get_service_name_by_id(self, service_id: int) -> tuple:
        sql = "select name from service where service_id = ?;"
        return self.manager(sql, service_id, fetchone=True)

    def get_service_id(self, service_name: str) -> tuple:
        sql = "select service_id from service where name = ?;"
        return self.manager(sql, service_name, fetchone=True)

    def get_service_data(self, service_name: str) -> tuple:
        service_id = self.get_service_id(service_name)[0]
        sql = "select content, price, photo from service where service_id = ?;"
        return self.manager(sql, service_id, fetchone=True)


class ServiceUpdateManager(Manager):
    def update_service_content(self, service_id: int, service_content: str) -> None:
        """Обновляем поле content в талице service"""
        sql = "UPDATE service SET content = ? WHERE service_id = ?"
        self.manager(sql, service_content, service_id, commit=True)

    def update_service_name(self, service_id: int, service_name: str) -> None:
        sql = "UPDATE service SET name = ? WHERE service_id = ?"
        self.manager(sql, service_name, service_id, commit=True)

    def update_service_price(self, service_id: int, service_price: int) -> None:
        sql = "UPDATE service SET price = ? WHERE service_id = ?"
        self.manager(sql, service_price, service_id, commit=True)

    def update_service_photo(self, service_id: int, service_photo: str) -> None:
        sql = "UPDATE service SET photo = ? WHERE service_id = ?"
        self.manager(sql, service_photo, service_id, commit=True)

    def update_service_category_id(self, service_id: int, category_id: int) -> None:
        sql = "UPDATE service SET category_id = ? WHERE service_id = ?"
        self.manager(sql, category_id, service_id, commit=True)

    def delete_service(self, service_name: str) -> None:
        sql = "DELETE FROM service WHERE name = ?"
        self.manager(sql, service_name, commit=True)