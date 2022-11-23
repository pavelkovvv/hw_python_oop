class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float):
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self):
        """Возвращает строку сообщения"""
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{format(self.duration, ".3f")} ч.; Дистанция: '
                f'{format(self.distance, ".3f")} км; Ср. скорость: '
                f'{format(self.speed, ".3f")} км/ч; Потрачено ккал: '
                f'{format(self.calories, ".3f")}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self, action: int = None, duration: float = None,
                 weight: int = None, *args) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: int = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.__class__.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(f'{self.__class__.__name__}', self.duration,
                           self.get_distance(),
                           self.__class__.get_mean_speed(self),
                           self.__class__.get_spent_calories(self))


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    MINUTES_IN_HOUR: int = 60

    def __init__(self, action: int = None, duration: float = None,
                 weight: int = None, *args):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    MINUTES_IN_HOUR: int = 60
    CM_IN_M: int = 100
    KMH_IN_MSEC: float = round(10 / 36, 3)

    def __init__(self, action: int = None, duration: float = None,
                 weight: int = None, height: int = None, *args):
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CORRECTION_FACTOR_FOR_SWIMMING: float = 1.1
    QUANTITY_SWIMMS: int = 2

    def __init__(self, action: int = None, duration: float = None,
                 weight: int = None, length_pool: int = None,
                 count_pool: int = None):
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CORRECTION_FACTOR_FOR_SWIMMING)
                * self.QUANTITY_SWIMMS * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in type_training:
        char_class: Training = type_training[workout_type](*data)
        return char_class
    else:
        print('Вы задали неверный тип тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
