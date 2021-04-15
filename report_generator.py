from docx import Document
import datetime
import calendar

TEMPLATE_FILE_NAME = 'template.docx'


class ReportGenerator:

    def create_monthly_report(self, path, work_items):
        template = Document(TEMPLATE_FILE_NAME)
        table = template.tables[0]
        now = datetime.datetime.now()
        _, days = calendar.monthrange(now.year, now.month)
       
        for day in range(1, days+1):
            
            date = datetime.datetime(now.year,now.month, day)

            if date.isoweekday() in range(1,6):
                key = date.strftime('%Y-%m-%d')

                if(key in work_items):
                    cells = table.add_row().cells
                    cells[0].text = key
                    cells[1].text = str(work_items[key].hour)
                    cells[2].text = ", ".join(map(str, work_items[key].work_items))

        template.save('report.docx')


