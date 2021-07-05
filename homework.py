import datetime as dt
from math import fabs


class Record:

    amount: float
    comment: str
    date: dt.date

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount: float, comment: str, date=None) -> None:
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        self.amount = amount
        self.comment = comment


class Calculator:

    limit: int

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, rec: Record) -> None:
        '''Функция сохраняющая новую запись.'''
        self.records.append(rec)

    def get_today_stats(self) -> int:
        '''Информация за день.'''
        expens_today: int = 0
        today_date: dt.date = dt.date.today()
        for record in self.records:
            if record.date == today_date:
                expens_today += record.amount
        return expens_today

    def get_week_stats(self) -> int:
        '''Информация за неделю.'''
        week_sum: int = 0
        date_week_ago: dt.date = (dt.date.today() - dt.timedelta(days=7))
        for record in self.records:
            if dt.date.today() >= record.date > date_week_ago:
                week_sum += record.amount
        return week_sum


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        '''Сколько ещё калорий можно/нужно получить сегодня.'''
        expens_kkal: int = self.get_today_stats()
        if self.limit > expens_kkal:
            expens_kkal = self.limit - expens_kkal
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {expens_kkal} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):

    EURO_RATE = 86.94
    USD_RATE = 73.24

    def get_today_cash_remained(self, currency) -> str:
        '''Сколько ещё денег можно потратить сегодня.'''
        expens: int = self.get_today_stats()

        if currency == 'eur':
            self.limit = self.limit / CashCalculator.EURO_RATE
            expens = self.get_today_stats() / CashCalculator.EURO_RATE
            currency = 'Euro'

        elif currency == 'usd':
            self.limit = self.limit / CashCalculator.USD_RATE
            expens = self.get_today_stats() / CashCalculator.USD_RATE
            currency = 'USD'

        else:
            currency = 'руб'

        if self.limit == expens:
            return 'Денег нет, держись'

        elif self.limit < expens:
            debt = fabs(self.limit - expens)
            return (f'Денег нет, держись: твой долг'
                    f' - {round(debt,2)} {currency}')
        else:
            balance = self.limit - expens
            return f'На сегодня осталось {round(balance,2)} {currency}'
