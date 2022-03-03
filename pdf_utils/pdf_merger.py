import convertapi
from decouple import config


class PDFMergerUtil:
    @staticmethod
    def merge(file_paths: list, save_dir: str):
        convertapi.api_secret = config('PDF_MERGER_SECRET_KEY')
        convertapi.convert('merge', {
            "Files": file_paths
        }, from_format='pdf').save_files(save_dir)


if __name__ == '__main__':
    PDFMergerUtil.merge([
        'E:\Documentwork\sharif\Term10\SEL\Assigment1_SEL\pdfs\BS-95_v2.pdf',
        'E:\Documentwork\sharif\Term10\SEL\Assigment1_SEL\pdfs\The_other_question_can_and_should_robots_have_righ.pdf'
    ], "E:\Documentwork\sharif\Term10\SEL\Assigment1_SEL\pdfs\merged.pdf")
