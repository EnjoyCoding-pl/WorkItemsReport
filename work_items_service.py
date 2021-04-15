import datetime
from azure.devops.connection import Connection
from azure.devops.v5_1.work_item_tracking.models import Wiql
from msrest.authentication import BasicAuthentication
from daily_work import DailyWork
from decouple import config
import dateutil.parser

COMPLETED_WORK_FIELD = 'Microsoft.VSTS.Scheduling.CompletedWork'
CHANGED_DATE_FIELD = 'System.ChangedDate'


class WorkItemsService:

    def get_my_work_items(self):

        credentials = BasicAuthentication('', config('TOKEN'))
        connection = Connection(base_url=config('URL'), creds=credentials)
        work_items_client = connection.clients_v6_0.get_work_item_tracking_client()

        wiql_result = work_items_client.query_by_wiql(Wiql(
            "Select [System.Id] From WorkItems Where [System.WorkItemType] = 'Task' AND [System.ChangedDate] >= @StartOfMonth AND [Assigned to] = @Me"))

        result = {}

        for work_item in wiql_result.work_items:

            work_item_updates = work_items_client.get_updates(work_item.id)

            for work_item_update in work_item_updates:

                if work_item_update.fields is not None and COMPLETED_WORK_FIELD in work_item_update.fields:

                    values = work_item_update.fields["Microsoft.VSTS.Scheduling.CompletedWork"]

                    if values.new_value is not None and (values.old_value is None or values.new_value > values.old_value):

                        date = dateutil.parser.isoparse(
                            work_item_update.fields["System.ChangedDate"].new_value)
                        key = date.strftime('%Y-%m-%d')

                        print("Work Item: {}, old completed work value: {}, new completed work value: {}, change date: {}".format(
                            work_item.id, values.old_value, values.new_value, key))

                        if key not in result:
                            result[key] = DailyWork(
                                values.new_value - (values.old_value or 0), work_item.id)
                        else:
                            result[key].add_work_item(
                                values.new_value - (values.old_value or 0), work_item.id)

        return result
