import convertapi
from decouple import config


class PDFMergerUtil:
    @staticmethod
    def merge(file_paths: list, save_dir: str):
        convertapi.api_secret = config('PDF_MERGER_SECRET_KEY')
        convertapi.convert('merge', {
            "Files": file_paths
        }, from_format='pdf').save_files(save_dir)
