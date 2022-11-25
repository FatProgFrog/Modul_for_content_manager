import requests
from bs4 import BeautifulSoup
from datetime import datetime

class InfoBlock():
    '''
    Храним заголовок, ссылку и дату
    title: str
    link: str
    date: datetime

    make_date(date: str)->datetime
    '''
    def __init__(self, title: str, link: str, date) -> None:
        self.title = title
        self.link = link
        self.date = date if type(date) is datetime else self.make_date(date)
        self._clear_all()

    def make_date(self, date: str)->datetime:
        '''
        Конвертирует str в datatime
        '''
        self._months = {
            'янва': '01',
            'февр': '02',
            'март': '03',
            'апре': '04',
            'майя': '05',
            'июня': '06',
            'июля': '07',
            'авгу': '08',
            'сент': '09',
            'октя': '10',
            'нояб': '11',
            'дека': '12',
        }
        self._year:int =None
        self._month:int=None
        self._day:int=None
        self._time:list[int]=None
        date = date.replace(',',"")
        if self._is_open_date(date):
            return datetime(datetime.now().year,datetime.now().month,datetime.now().day)
        if self._is_dash(date):
            temp = date.split("-")[0]
            if self._is_a_day(temp):
                self._day=int(temp)
                date=date.split("-")[1]
            else:
                date=temp
        self._spliting_date(date)

        if self._time:
            return datetime(self._year, self._month, self._day, *self._time)
        return datetime(self._year, self._month, self._day)

    def _is_dash(self, date: str)-> bool:
        '''
        Есть ли тире в date
        '''
        if "-" in date:
            return True
        else:
            return False

    def _is_a_year(self, date_item: str)-> bool:
        '''
        Определяем год по колличеству символов
        '''
        len_of_year = 4
        if len(date_item) == len_of_year:
            return True
        else:
            return False

    def _is_a_day(self, date_item: str)-> bool:
        '''
        Определяем день по колличеству символов
        '''
        len_of_day = 2
        if len(date_item.strip()) <= len_of_day:
            return True
        else:
            return False

    def _clear_all(self)-> None:
        '''
        Очистка вспомогательных переменных
        '''
        self._months = None
        self._month = None
        self._year = None
        self._day = None
        self._time = None

    def _spliting_date(self, date: str)-> None:
        '''
        Разбиваем date на year, month, day
        '''
        date: list[str]=date.split()
        for i in date:
            i=i.split(',')[0]
            if i.isdigit():
                if self._is_a_year(i):
                    self._year=int(i)
                elif self._is_a_day(i):
                    if not self._day:
                        self._day=int(i)
            else:
                if ':' in i:
                    self._get_time(i)
                else:
                    self._month=int(self._months[i[0:4].lower()])
        if not self._year:
            self._year=datetime.today().year

    def _get_time(self, time:str)-> None:
        self._time = map(int, time.split(":"))

    def _is_open_date(self, date)-> bool:
        if "открытая дата" in date.lower():
            return True
        else:
            return False


class Parser:
    '''
    Парсит нужную страницу и отдаёт soup
    '''
    def __init__(self, url: str=None)->None:
        self.url=url

    def parse_html(self)->BeautifulSoup:
        if self.url:
            html = requests.get(self.url).text
            soup=BeautifulSoup(html, 'html.parser')
            return soup

    def set_url(self, url)->None:
        self.url=url




class BlockBuilder:
    '''
    Формирует список инфоблоков
    '''
    def __init__(self, soup:BeautifulSoup)->None:
        self.soup=soup
        self.info_blocks:list[InfoBlock]

    def set_blocks(self)->None:
        info_blocks: list[BeautifulSoup]=self.soup.find('main').find_all('div',{'class' : "info-block"})
        result: list[InfoBlock] = []
        for info in info_blocks:
            link=info.find('div', {'class' : 'name'}).find('a').get('href').strip()
            title=info.find('div', {'class':'name'}).find('a').get('title').strip()
            
            date=info.find('div', {'class':'date'}).text.strip()
            result.append(InfoBlock(title, link, date))

        self.info_blocks=result

    def get_blocks(self)->list[InfoBlock]:
        self.set_blocks()
        return self.info_blocks

    def sort_blocks(self)->list[InfoBlock]:
        self.set_blocks()
        return sorted(self.info_blocks, key=lambda x: x.date)


class FileWriter:
    '''
    Записывает в файл
    '''
    def __init__(self, counter:int=None, file_name:str=None)->None:
        self.counter=counter
        self.file_name=file_name
    
    @staticmethod
    def write(self, content:str, file_name:str='noname.txt') -> None:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)

    def write_list(self, content:list[InfoBlock], file_name:str='noname.txt', count:int = '') -> None:
        with open(file_name, 'w', encoding='utf-8') as file:
            for info_block in content:
                file.write(f"{count} {info_block.title} https://www.bileter.ru{info_block.link} {info_block.date} \n")
                if count!='':
                    count+=self.counter

    def write_list_to_clipboard(self, content:list[InfoBlock], file_name:str='clipboard.txt' , count='') -> None:
        with open(file_name, 'w', encoding='utf-8') as file:
            for info_block in content:
                file.write(f"{count} {info_block.link}\n")
                if count!='':
                    count+=self.counter

class Intrface():
    def __init__(self) -> None:
        self.url = self.set_url()
        self.step = self.set_step()

    def set_url(self) -> None:
        return input('Введите адресс подборки \n')

    def set_step(self) -> None:
        return input('Введите шаг для сортировки подборки ')

    def run(self) -> None:
        parser=Parser()
        parser.set_url(self.url)
        builder=BlockBuilder(parser.parse_html())
        list_blocks=builder.sort_blocks()
        if self.step:
            writer = FileWriter(counter=int(self.step))
            writer.write_list_to_clipboard(list_blocks, "clipboard.txt", count=5)
        else:
            writer = FileWriter()
            writer.write_list_to_clipboard(list_blocks, "clipboard.txt")

if __name__ == '__main__':
    app = Intrface()
    app.run()

