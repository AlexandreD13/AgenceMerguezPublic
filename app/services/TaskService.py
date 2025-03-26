from agence.celery import app
from app.domain.get_destination_request import GetDestinationsRequests
from app.services.DealScannerService import DealScannerService


class TaskService:
    __scanner = DealScannerService()

    def generate_scan_task(self, request: GetDestinationsRequests, user: str, schedule=None):
        @app.task(name="tasks.scan.test.1")
        def scan():
            self.__scanner.scan(request, user)

        scan.apply_async((x, y), task_id=f'task_{x}_{y}', countdown=schedule)


if __name__ == '__main__':
    service = TaskService()
    service.generate_scan_task(
        GetDestinationsRequests(airport_code="YUL", destination="Japan"),
        "replaceme@exmaple.com"
    )
