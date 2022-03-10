from threading import Thread

import convertapi
from decouple import config


class PDFMergerUtil:
    @staticmethod
    def merge(file_paths: list, save_dir: str):
        def func():
            convertapi.api_secret = config('PDF_MERGER_SECRET_KEY')
            convertapi.convert('merge', {
                "Files": file_paths
            }, from_format='pdf').save_files(save_dir)

        new_thread = Thread(target=func)
        new_thread.start()
        new_thread.join()


if __name__ == '__main__':
    PDFMergerUtil.merge(['BQACAgQAAxkBAANcYipGk3SyuW-qyFToUaVtRfQI86sAAuYKAAKfK1FRBiALx7U0EyMjBA.pdf',
                         'BQACAgQAAxkBAANeYipGobidxp2ZVTZQe9wHfMnB7x8AAucKAAKfK1FROgfTrmW7JIsjBA.pdf'],
                        'merged_test.pdf'
                        )
