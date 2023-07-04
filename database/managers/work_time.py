from .base import Manager

class WorkTimeManager(Manager):
    def get_master_time(self, master_id: int) -> list[tuple]:
        sql = "select from_hours || '-' || to_hours from work_time where master_id = ?;"
        return self.manager(sql, master_id, fetchall=True)

