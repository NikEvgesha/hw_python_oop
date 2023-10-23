class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    SEC_IN_HOUR = 3600
    LEN_STEP = 0.65
    distance: float = 0
    mean_speed: float = 0
    spent_calories: float = 0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        if self.distance == 0:
            self.distance = self.get_distance()
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.spent_calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.distance,
                           self.mean_speed,
                           self.spent_calories)


class Running(Training):
    """Тренировка: бег."""
    SPENT_CALORIES_KOEF = 18
    SPENT_CALORIES_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        if self.mean_speed == 0:
            self.mean_speed = self.get_mean_speed()
        duration_min = self.duration * self.MIN_IN_HOUR
        return ((self.SPENT_CALORIES_KOEF * self.mean_speed
                + self.SPENT_CALORIES_SHIFT)
                * self.weight / self.M_IN_KM * duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_KOEF1 = 0.035
    CALORIES_KOEF2 = 0.029
    KMH_TO_MS = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        if self.mean_speed == 0:
            self.mean_speed = self.get_mean_speed()
        speed_m_in_s = self.mean_speed * self.KMH_TO_MS
        return ((self.CALORIES_KOEF1 * self.weight
                + (speed_m_in_s**2 / (self.height / self.SM_IN_M))
                * self.CALORIES_KOEF2 * self.weight) * self.duration
                * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_KOEF1 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        if self.mean_speed == 0:
            self.mean_speed = self.get_mean_speed()
        return ((self.mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_KOEF1
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_types:
        return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training:
            main(training)
        else:
            print("Ошибка в данных")
