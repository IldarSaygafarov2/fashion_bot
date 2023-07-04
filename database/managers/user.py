from typing import Optional

from .base import Manager


class UserManager(Manager):
    def is_user_exists(self, telegram_id: int) -> Optional[tuple]:
        sql = """SELECT user_id FROM users WHERE telegram_id = ?;"""
        user_id = self.manager(sql, telegram_id, fetchone=True)
        if not user_id:
            return
        return user_id

    def add_user(self, username: str, phone_number: str, telegram_id: int) -> None:
        sql = """
            INSERT INTO users(username, phone_number, telegram_id) VALUES (?, ?, ?)
            ON CONFLICT (telegram_id) DO NOTHING;
        """
        self.manager(sql, username, phone_number, telegram_id, commit=True)
        print(f"User: {username} added successfully")