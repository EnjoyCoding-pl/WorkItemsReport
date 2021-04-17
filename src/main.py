from work_items_service import WorkItemsService
from report_generator import ReportGenerator

if __name__ == "__main__":
    service = WorkItemsService()
    work_items = service.get_my_work_items()
    generator = ReportGenerator()
    generator.create_monthly_report('.', work_items)
