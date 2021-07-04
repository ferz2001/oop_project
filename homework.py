import datetime as dt
from math import fabs


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount: float, comment: str, date=None):
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        self.amount = amount
        self.comment = comment

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        '''Функция сохраняющая новую запись.'''
        self.records.append(rec)

    def get_today_stats(self):
        '''Информация за день.'''
        expens_today = 0
        today_date = dt.datetime.now().date()
        for i in range(len(self.records)):
            if self.records[i].date == today_date:
                expens_today += self.records[i].amount
        return expens_today

    def get_week_stats(self):
        '''Информация за неделю.'''
        today_date = dt.datetime.now().date()
        expens_week = 0
        for i in range(7):
            for i in range(len(self.records)):
                if self.records[i].date == today_date:
                    expens_week += self.records[i].amount
            today_date += dt.timedelta(days=1)
        return expens_week


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        '''Сколько ещё калорий можно/нужно получить сегодня.'''
        expens = self.get_today_stats()

        if self.limit > expens:
            expens = self.limit - expens
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f'калорийностью не более {expens} кКал')

        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):

    EURO_RATE = 86.94
    USD_RATE = 73.24

    def get_today_cash_remained(self, currency):
        '''Сколько ещё денег можно потратить сегодня.'''
        expens = self.get_today_stats()
        if currency == 'eur':
            self.limit = self.limit / CashCalculator.EURO_RATE
            expens = expens / CashCalculator.EURO_RATE
            currency = 'Euro'

        elif currency == 'usd':
            self.limit = self.limit / CashCalculator.USD_RATE
            expens = expens / CashCalculator.USD_RATE
            currency = 'USD'

        else:
            currency = 'руб'

        if self.limit == expens:
            return 'Денег нет, держись'

        elif self.limit < expens:
            debt = fabs(self.limit - expens)
            return f'Денег нет, держись: твой долг - {debt} {currency}'

        else:
            balance = self.limit - expens
            return f'На сегодня осталось {balance} {currency}'

cash_calculator = CashCalculator(1000)

cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='05.07.2021'))

print(cash_calculator.records[2].date)

print(cash_calculator.get_week_stats())