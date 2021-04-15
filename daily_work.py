
class DailyWork:
    def __init__(self, hour, work_item_id):
        self.hour = hour
        self.work_items = [work_item_id]

    def add_work_item(self, hour, work_item_id):
        self.hour += hour
        self.work_items.append(work_item_id)
