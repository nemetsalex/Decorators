# Задание 3

from datetime import datetime


def log_decorator(path):
    """Декоратор-логер для записи в файл даты, времени вызова декорируемой функции, ее имени, агрументов и результата"""
    def log_decorator_(old_function):
        def foo(*args, **kwargs):
            date_time = datetime.now()
            str_time = date_time.strftime('%Y-%m-%d время %H-%M-%S')
            func_name = old_function.__name__
            result = old_function(*args, **kwargs)
            with open(f'{path}log_03.txt', 'a', encoding='utf-8') as file:
                file.write(f'\nДата вызова функции: {str_time}\n'
                           f'Имя функции: {func_name}\n'
                           f'Аргументы функции: {args, kwargs}\n'
                           f'Возвращаемое значение функции: {result}\n'
                           f'{"*"*50}\n')
            return result
        return foo
    return log_decorator_