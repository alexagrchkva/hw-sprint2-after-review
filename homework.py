from typing import Dict, Type

SWIMMING: str = 'SWM'
RUNNING: str = 'RUN'
SPORTSWALKING: str = 'WLK'


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f'Тип тренировки: {self.training_type}; ' \
               f'Длительность: {self.duration:.3f} ч.; ' \
               f'Дистанция: {self.distance:.3f} км; ' \
               f'Ср. скорость: {self.speed:.3f} км/ч; ' \
               f'Потрачено ккал: {self.calories:.3f}.'


class Training:
    M_IN_KM: int = 1000
    MINUTES: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о тренировке"""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег"""

    running_calories_coef_1: float = 18
    running_calories_coef_2: float = 20

    def get_spent_calories(self) -> float:
        calories_for_running = ((self.running_calories_coef_1
                                 * self.get_mean_speed()
                                 - self.running_calories_coef_2)
                                * self.weight / self.M_IN_KM
                                * (self.duration * Training.MINUTES))
        return calories_for_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба"""
    calories_wlk_1: float = 0.035
    calories_wlk_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.calories_wlk_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.calories_wlk_2 * self.weight)
                * (self.duration * Training.MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""
    swimming_calories_coef: float = 1.1
    LEN_STEP: float = 1.38

    def __init__(self,
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
        return \
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.swimming_calories_coef) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные с датчиков"""

    workout_dict: Dict[str, Type[Training]] = {
        SWIMMING: Swimming,
        RUNNING: Running,
        SPORTSWALKING: SportsWalking
    }

    cls_name = workout_dict[workout_type]
    training = cls_name(*data)
    return training


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    training_message: str = info.get_message()
    print(training_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1206, 12, 6]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)