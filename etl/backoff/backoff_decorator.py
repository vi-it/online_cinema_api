import functools
import logging
import time
import typing


def backoff(exceptions: tuple, start_sleep_time=0.1, factor=2,
            border_sleep_time=10) -> typing.Any:
    """
    Функция для повторного выполнения функции через некоторое время, если
    возникла ошибка. Использует наивный экспоненциальный рост времени повтора
    (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """
    def func_wrapper(func) -> typing.Any:
        @functools.wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    logging.info(f"Error: occurred {err}")
                    sleep_time *= factor
                    sleep_time = min(sleep_time, border_sleep_time)
                    time.sleep(sleep_time)
        return inner
    return func_wrapper
