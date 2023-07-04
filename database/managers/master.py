from .base import Manager


class MasterManager(Manager):
    """Class for working with master table"""

    def add_master(
        self, full_name: str, content: str, photo: str, price: int, service_id: int
    ) -> None:
        sql = """
            INSERT INTO master(full_name, content, photo, price, service_id)
            VALUES (?,?,?,?,?);
        """
        self.manager(sql, full_name, content, photo, price, service_id, commit=True)

    def get_all_masters(self) -> list[tuple]:
        sql = "SELECT full_name FROM master WHERE is_working = 1"
        return self.manager(sql, fetchall=True)

    def get_masters(self, service_id) -> list[tuple]:
        sql = "SELECT master_id, full_name, content, photo, price FROM master WHERE is_working = 1 AND service_id = ?;"
        return self.manager(sql, service_id, fetchall=True)

    def get_master_id(self, master_name: str) -> int:
        sql = "SELECT master_id FROM master WHERE full_name = ?;"
        return self.manager(sql, master_name, fetchone=True)[0]

    def delete_master(self, master_id: int) -> None:
        sql = "DELETE FROM master WHERE master_id = ?;"
        self.manager(sql, master_id, commit=True)

    def get_master_full_name(self, master_id) -> tuple:
        sql = "select full_name from master where master_id = ?;"
        return self.manager(sql, master_id, fetchone=True)


class MasterUpdateManager(Manager):
    """Class for updating columns in master table"""

    def update_master_content(self, master_id: int, new_content: str) -> None:
        sql = """
            --sql
            UPDATE master SET content = ? WHERE master_id = ?;
        """
        self.manager(sql, new_content, master_id, commit=True)

    def update_master_full_name(self, master_id: int, new_full_name: str) -> None:
        sql = """
            --sql
            UPDATE master SET full_name = ? WHERE master_id = ?;
        """
        self.manager(sql, new_full_name, master_id, commit=True)

    def update_master_photo(self, master_id: int, new_photo: str) -> None:
        sql = """
            --sql
            UPDATE master SET photo = ? WHERE master_id = ?;
        """
        self.manager(sql, new_photo, master_id, commit=True)

    def update_master_service(self, master_id: int, new_service_id: int) -> None:
        sql = """
            --sql
            UPDATE master SET service_id = ? WHERE master_id = ?;
        """
        self.manager(sql, new_service_id, master_id, commit=True)

    def update_master_price(self, master_id: int, new_price: int) -> None:
        sql = """
            --sql
            UPDATE master SET price = ? WHERE master_id = ?;
        """
        self.manager(sql, new_price, master_id, commit=True)
