import datetime as dt
from typing import Dict, List


class Record:
    """Класс для создания записей."""
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount: int, comment: str, date=None) -> None:
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        self.amount = amount
        self.comment = comment


class Calculator:
    """Класс с основными методами для калькулятора."""
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: List[Record] = []
        self.week_ago_time: dt.date = dt.date.today() - dt.timedelta(days=7)
        self.today_date: dt.date = dt.date.today()

    def add_record(self, record: Record) -> None:
        """Функция сохраняющая новую запись."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        '''Информация за день.'''
        expens_today: int = sum(record.amount for record in self.records
                                if record.date == self.today_date)
        return expens_today

    def get_week_stats(self) -> int:
        '''Информация за неделю.'''
        week_sum: int = sum(record.amount for record in self.records if dt.
                            date.today() >= record.date > self.week_ago_time)
        return week_sum

    def get_expense(self, item_expense: int) -> int:
        """Метод для высчитывания остатка денег/калорий"""
        item_expense -= self.limit
        return abs(item_expense)


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""
    def get_calories_remained(self) -> str:
        '''Сколько ещё калорий можно/нужно получить сегодня.'''
        expense_kkal: int = self.get_today_stats()
        if self.limit > expense_kkal:
            expens_kkal = self.get_expense(expense_kkal)
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {expens_kkal} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег"""
    RUB: float = 1.00
    EURO_RATE: float = 86.94
    USD_RATE: float = 73.24

    def get_today_cash_remained(self, currency: str) -> str:
        '''Сколько ещё денег можно потратить сегодня.'''
        expense_money = self.limit - self.get_today_stats()
        if not expense_money:
            return 'Денег нет, держись'
        valute: Dict[str, tuple[float, str]] = {'rub': (self.RUB,
                                                        'руб'),
                                                'eur': (self.EURO_RATE,
                                                        'Euro'),
                                                'usd': (self.USD_RATE,
                                                        'USD')}
        rate, valute_text = valute[currency]
        limit = self.limit / rate
        expense_money_rate = self.get_today_stats() / rate

        if limit < expense_money_rate and limit:
            debt: float = abs(limit - expense_money_rate)
            return (f'Денег нет, держись: твой долг'
                    f' - {round(debt,2)} {valute_text}')
        elif limit > expense_money_rate:
            balance: float = limit - expense_money_rate
            return f'На сегодня осталось {round(balance,2)} {valute_text}'
        else:
            return 'Ошибка'
