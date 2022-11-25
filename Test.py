from unittest import TestCase, TestLoader, TextTestRunner
from main import Parser, InfoBlock, FileWriter
from datetime import datetime

now_year = datetime.now().year
now = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} 00:00:00"

datatime_test_dict = {
    "25 - 30 Ноября": f"{now_year}-11-25 00:00:00",
    "Открытая дата": str(now),
    "24 Ноября 2022 - 31 Января 2023": "2022-11-24 00:00:00",
    "27 Ноября - 30 Декабря": f"{now_year}-11-27 00:00:00",
    "13 Апреля": f"{now_year}-04-13 00:00:00",
    "26 Ноября, 19:00": f"{now_year}-11-26 19:00:00",
}

class ParserTest(TestCase):
    def setUp(self):
        self.parser = Parser()
        self.html = ""

class InfoBlockTest(TestCase):
    def setUp(self):
        self.info_block = InfoBlock('test', 'test/url', '24 января 1844')

    def test_init(self):
        self.assertEqual(self.info_block.title, 'test')
        self.assertEqual(self.info_block.link, 'test/url')
        self.assertEqual(type(self.info_block.date), datetime)

    def test_convert(self):
        for test_date in datatime_test_dict:
            with self.subTest(test_date=test_date):
                self.assertEqual(str(InfoBlock('test', 'test/url', test_date).date), datatime_test_dict[test_date])

class FileWriterTest(TestCase):
    def setUp(self):
        self.file_writer = FileWriter(file_name='test', counter=5)

    def test_init(self):
        self.assertEqual(self.file_writer.file_name, 'test')
        self.assertEqual(self.file_writer.counter, 5)


if __name__ == "__main__":
    suite_parser = TestLoader().loadTestsFromTestCase(ParserTest)
    suite_info_block = TestLoader().loadTestsFromTestCase(InfoBlockTest)
    suite_file_writer = TestLoader().loadTestsFromTestCase(FileWriterTest)


    TextTestRunner(verbosity=2).run(suite_parser)
    TextTestRunner(verbosity=2).run(suite_info_block)
    TextTestRunner(verbosity=2).run(suite_file_writer)


