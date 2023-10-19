import json
import time

from backend.settings import BASE_DIR


class ViewCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_run = time.time()

    def __call__(self, request):
        response = self.get_response(request)
        if time.time() - self.last_run > 3600:
            self.last_run = time.time()
            self.merge_json_file()
        return response

    @staticmethod
    def merge_json_file():
        with open(BASE_DIR / 'views_count.json', 'r') as f:
            json_data = json.load(f)

        for url_updated, url_recent in zip(json_data['updated'].keys(), json_data['recent'].keys()):
            json_data['updated'][url_updated] += json_data['recent'][url_recent]
            json_data['recent'][url_recent] = 0

        with open('views_count.json', 'w') as f:
            json.dump(json_data, f, indent=4)

        print('merged was succeed')
