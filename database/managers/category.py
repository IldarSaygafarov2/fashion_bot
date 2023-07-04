from .base import Manager


class CategoryManager(Manager):
    def add_category(self, category_name: str) -> None:
        sql = """insert into category(name) values (?);"""
        self.manager(sql, category_name, commit=True)

    def update_category(self, new_category_name: str, category_id: int) -> None:
        sql = "update category set name = ? where category_id = ?;"
        return self.manager(sql, new_category_name, category_id, commit=True)

    def get_categories(self) -> list[tuple]:
        sql = """select name from category;"""
        return self.manager(sql, fetchall=True)

    def format_categories(self) -> list[str]:
        categories = self.get_categories()
        return [category[0] for category in categories]

    def get_category_id(self, category_name: str) -> int:
        sql = "select category_id from category where name = ?;"
        return self.manager(sql, category_name, fetchone=True)[0]  # (1,)

    def get_category_name(self, category_id: int) -> str:
        sql = "select name from category where category_id = ?;"
        return self.manager(sql, category_id, fetchone=True)[0]  # (1,)

    def delete_category(self, category_name: str) -> None:
        sql = "delete from category where name = ?;"
        self.manager(sql, category_name, commit=True)