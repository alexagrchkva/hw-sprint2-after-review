from dataclasses import dataclass
from typing import Type

SWIMMING: str = 'SWM'
RUNNING: str = 'RUN'
SPORTSWALKING: str = 'WLK'


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """
        Возвращает сообщение с информацией о тренировке:
        тип, длительность, дистанция, средняя скорость,
        количество потраченных килокалорий
        """
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество калорий"""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о тренировке"""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег"""

    RUN_CAL_1: float = 18
    RUN_CAL_2: float = 20

    def get_spent_calories(self) -> float:
        calories_for_running = (
                         (
                          self.RUN_CAL_1 * self.get_mean_speed()
                          - self.RUN_CAL_2
                         ) * self.weight
                         / self.M_IN_KM
                         * (
                             self.duration * Training.MIN_IN_HOUR
                          )
        )
        return calories_for_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба"""
    WKL_CAL_1: float = 0.035
    WKL_CAL_2: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.WKL_CAL_1 * self.weight
                + (self.get_mean_speed()
                   ** 2 // self.height)
                * self.WKL_CAL_2
                * self.weight
             )
            * self.duration
            * Training.MIN_IN_HOUR

        )


class Swimming(Training):
    """Тренировка: плавание."""
    SWM_CAL: float = 1.1
    LEN_STEP: float = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
                self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (
              self.get_mean_speed() + self.SWM_CAL
            ) * 2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные с датчиков"""

    workout_dict: [str, Type[Training]] = {
        SWIMMING: Swimming,
        RUNNING: Running,
        SPORTSWALKING: SportsWalking
    }

    cls_name = workout_dict[workout_type]
    training = cls_name(*data)

    if workout_type in workout_dict.keys():
        return training
    else:
        print("Тренировка не поддерживается "
              "// Unsupported training type")


def main(training: Training) -> None:
    """Основная функция"""
    info = training.show_training_info()
    training_message: str = info.get_message()
    print(training_message)


if __name__ == '__main__':
    packages = [(SWIMMING, [720, 1, 80, 25, 40]),
                (RUNNING, [1206, 12, 6]),
                (SPORTSWALKING, [9000, 1, 75, 180])
                ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
