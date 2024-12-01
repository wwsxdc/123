import pygame  # Импортируем библиотеку Pygame для работы с графикой и звуком
from PIL import Image  # Импортируем библиотеку PIL для работы с изображениями

import random  # Импортируем библиотеку random для генерации случайных чисел
from functools import lru_cache  # Импортируем lru_cache для кэширования функций
import os  # Импортируем библиотеку os для работы с файловой системой

# Инициализация Pygame и шрифта
pygame.init()  # Инициализация всех модулей Pygame
pygame.font.init()  # Инициализация модуля шрифтов
font = pygame.font.Font(None, 74)  # Создание шрифта с размером 74
sign_font = pygame.font.Font(None, 20)  # Создание шрифта для таблички

# Константы физики
GRAVITY = 0.8  # Сила тяжести
MAX_FALL_SPEED = 15  # Максимальная скорость падения
JUMP_POWER = 15  # Сила прыжка
ACCELERATION = 0.2  # Ускорение
MAX_SPEED = 10  # Максимальная скорость


@lru_cache(maxsize=None)  # Кэширование результатов функции
def load_gif_frames(gif_path, size):
    """Загрузка кадров из GIF-файла и изменение их размера"""
    try:
        frames = []  # Список для хранения кадров
        gif = Image.open(gif_path)  # Открытие GIF-файла

        # Предварительно выделяем память
        frames = [None] * gif.n_frames  # Создание списка для кадров

        # Исправляем цикл
        for i in range(gif.n_frames):  # Перебор всех кадров
            gif.seek(i)  # Переход к i-му кадру
            frame = gif.convert('RGBA').resize(size, Image.LANCZOS)  # Изменение размера кадра
            pygame_surface = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            ).convert_alpha()  # Преобразование в Pygame Surface
            frames[i] = pygame_surface  # Сохранение кадра в список
        return frames  # Возвращение списка кадров
    except FileNotFoundError:
        print(f"Ошибка: Файл {gif_path} не найден")  # Обработка ошибки, если файл не найден
        pygame.quit()  # Завершение Pygame
        exit()  # Выход из программы
    except Exception as e:
        print(f"Ошибка при загрузке анимации: {e}")  # Обработка других ошибок
        pygame.quit()  # Завершение Pygame
        exit()  # Выход из программы


def draw_button(text, x, y, width, height, active_color, inactive_color, mouse_pos):
    """Функция для отрисовки кнопки"""
    button_rect = pygame.Rect(x, y, width, height)  # Создание прямоугольника кнопки
    color = active_color if button_rect.collidepoint(mouse_pos) else inactive_color  # Определение цвета кнопки
    pygame.draw.rect(display, color, button_rect)  # Отрисовка кнопки
    text_surface = font.render(text, True, (255, 255, 255))  # Создание текстовой поверхности
    text_rect = text_surface.get_rect(center=button_rect.center)  # Центрирование текста
    display.blit(text_surface, text_rect)  # Отрисовка текста на кнопке
    return button_rect  # Возвращение прямоугольника кнопки


def pause_menu():
    """Функция для отображения меню паузы"""
    pause = True  # Переменная для отслеживания состояния паузы
    while pause:  # Цикл, пока меню паузы активно
        mouse_pos = pygame.mouse.get_pos()  # Получение позиции мыши

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                return "exit"  # Возврат значения "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                if continue_btn.collidepoint(mouse_pos):  # Если нажата кнопка "Продолжить"
                    return "continue"  # Возврат значения "continue"
                if restart_btn.collidepoint(mouse_pos):  # Если нажата кнопка "Перезапустить"
                    return "restart"  # Возврат значения "restart"
                if exit_btn.collidepoint(mouse_pos):  # Если нажата кнопка "Выход"
                    return "exit"  # Возврат значения "exit"
            if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                if event.key == pygame.K_ESCAPE:  # Если нажата клавиша Escape
                    return "continue"  # Возврат значения "continue"

        # Затемнение фона
        dark_surface = pygame.Surface((screen_width, screen_height))  # Создание затемняющего слоя
        dark_surface.fill((0, 0, 0))  # Заполнение черным цветом
        dark_surface.set_alpha(128)  # Установка прозрачности
        display.blit(dark_surface, (0, 0))  # Отрисовка затемняющего слоя

        # Отрисовка кнопок
        continue_btn = draw_button("Continue", screen_width // 2 - 150, screen_height // 2 - 120, 300, 80,
                                   (100, 200, 100), (50, 150, 50), mouse_pos)
        restart_btn = draw_button("Restart", screen_width // 2 - 150, screen_height // 2, 300, 80, (100, 100, 200),
                                  (50, 50, 150), mouse_pos)
        exit_btn = draw_button("Exit", screen_width // 2 - 150, screen_height // 2 + 120, 300, 80, (200, 100, 100),
                               (150, 50, 50), mouse_pos)

        pygame.display.update()  # Обновление дисплея
        clock.tick(60)  # Ограничение FPS


# Получение разрешения экрана
info_object = pygame.display.Info()  # Получение информации о дисплее
screen_width = info_object.current_w  # Ширина экрана
screen_height = info_object.current_h  # Высота экрана

# Создание окна
screen_width = 800  # Ширина окна
screen_height = 600  # Высота окна
display = pygame.display.set_mode((screen_width, screen_height),
                                  pygame.HWSURFACE | pygame.DOUBLEBUF)  # Создание окна с двойной буферизацией
pygame.display.set_caption('Jump and Run')  # Установка заголовка окна

# Получаем путь к директории скрипта
base_path = os.path.dirname(__file__)  # Получение пути к директории скрипта

# Загрузка иконки и анимаций
icon = pygame.image.load(os.path.join(base_path, 'assets', 'icon.png'))  # Загрузка иконки
pygame.display.set_icon(icon)  # Установка иконки окна

# Загрузка текстуры платформы
platform_texture = pygame.image.load(
    os.path.join(base_path, 'assets', 'platform.png')).convert_alpha()  # Загрузка текстуры платформы

# Загружаем анимацию
animation_right = load_gif_frames(os.path.join(base_path, 'assets', 'beg.gif'),
                                  (64, 64))  # Загрузка анимации движения вправо
animation_idle = load_gif_frames(os.path.join(base_path, 'assets', 'stoit.gif'), (64, 64))  # Загрузка анимации простоя
animation_jump = load_gif_frames(os.path.join(base_path, 'assets', 'jump.gif'), (64, 64))  # Загрузка анимации прыжка
animation_left = [pygame.transform.flip(frame, True, False) for frame in
                  animation_right]  # Загрузка анимации движения влево
animation_jump_left = [pygame.transform.flip(frame, True, False) for frame in
                       animation_jump]  # Загрузка анимации прыжка влево
background_animation = load_gif_frames(os.path.join(base_path, 'assets', 'background.gif'),
                                       (screen_width, screen_height))  # Загрузка фона
background_frame = 0  # Индекс текущего кадра фона

# Инициализация переменных
gg_width = animation_idle[0].get_width()  # Ширина персонажа
gg_height = animation_idle[0].get_height()  # Высота персонажа
gg_x = 32  # Начальная позиция по X
gg_y = 32  # Начальная позиция по Y
camera_x = 0  # Позиция камеры
level_width = screen_width * 100  # Ширина уровня
animation_count = 0  # Счетчик анимации
facing_left = False  # Переменная для отслеживания направления
is_moving = False  # Переменная для отслеживания движения
acceleration = 0.5  # Ускорение
max_speed = 7  # Максимальная скорость
current_speed = 0  # Текущая скорость
make_jump = False  # Переменная для отслеживания прыжка
jump_counter = 30  # Счетчик прыжка
gravity = 35  # Сила тяжести


class PlatformGenerator:
    """Класс для генерации платформ"""

    def __init__(self, level_width, min_y=250, max_y=550):
        self.level_width = level_width  # Ширина уровня
        self.min_y = min_y  # Минимальная высота платформ
        self.max_y = max_y  # Максимальная высота платформ
        self.min_gap = 150  # Минимальное расстояние между платформами
        self.max_gap = 250  # Максимальное расстояние между платформами
        self.platform_width = 150  # Ширина платформы
        self.platform_height = 15  # Высота платформы
        self.last_x = 0  # Последняя позиция по X
        self.last_y = 450  # Последняя позиция по Y
        self.platforms = []  # Список платформ
        self.platform_cache = {}  # Кэш платформ
        self.seed = random.randint(1, 1000000)  # Случайное начальное значение
        self.chunk_size = screen_width  # Размер одного чанка
        self.loaded_chunks = set()  # Множество загруженных чанков

        # Создаем начальную платформу
        self.platforms.append(
            pygame.Rect(32, 450, self.platform_width, self.platform_height)  # Создание прямоугольника платформы
        )
        self.platform_cache[32] = self.platforms[0]  # Кэширование первой платформы

        # Генерируем первую порцию платформ
        self.generate_chunk(screen_width * 2)  # Генерация платформ для первого чанка

    def check_platform_collision(self, new_platform):
        """Улучшенная проверка расстояния между платформами"""
        # Увеличиваем зону проверки
        padding_x = 100  # Горизонтальный отступ
        padding_y = 40  # Вертикальный отступ

        check_rect = pygame.Rect(
            new_platform.x - padding_x,
            new_platform.y - padding_y,
            new_platform.width + padding_x * 2,
            new_platform.height + padding_y * 2
        )

        for platform in self.platforms:  # Перебор всех платформ
            # Проверяем горизонтальное расстояние
            x_distance = abs(platform.centerx - new_platform.centerx)  # Расстояние по X
            y_distance = abs(platform.centery - new_platform.centery)  # Расстояние по Y

            # Если платформы слишком близко по горизонтали
            if x_distance < self.min_gap:
                return True  # Возврат True, если есть столкновение

            # Если платформы близко по горизонтали, проверяем вертикальное расстояние
            if x_distance < self.min_gap * 1.5 and y_distance < 60:
                return True  # Возврат True, если есть столкновение

            # Общая проверка пересечения
            if check_rect.colliderect(platform):
                return True  # Возврат True, если есть столкновение

        return False  # Возврат False, если столкновений нет

    def generate_platforms_for_chunk(self, chunk_start_x):
        """Генерирует платформы для конкретного чанка"""
        random.seed(self.seed + chunk_start_x)  # Установка начального значения для генерации

        chunk_platforms = []  # Список платформ для чанка
        x = chunk_start_x  # Начальная позиция по X
        chunk_end = x + screen_width  # Конечная позиция чанка
        attempts = 0  # Добавляем счетчик попыток

        while x < chunk_end and attempts < 100:  # Ограничиваем количество попыток
            if chunk_platforms:  # Если уже есть платформы в чанке
                last_y = chunk_platforms[-1].y  # Высота последней платформы
                min_new_y = max(self.min_y, last_y - 80)  # Уменьшаем максимальный перепад высот
                max_new_y = min(self.max_y, last_y + 80)  # Увеличиваем максимальный перепад высот
            else:
                min_new_y = self.min_y  # Минимальная высота
                max_new_y = self.max_y  # Максимальная высота

            y = random.randint(min_new_y, max_new_y)  # Генерация случайной высоты для новой платформы
            platform = pygame.Rect(x, y, self.platform_width, self.platform_height)  # Создание прямоугольника платформы

            if not self.check_platform_collision(platform):  # Проверка на столкновение
                chunk_platforms.append(platform)  # Добавление платформы в список
                x += random.randint(self.min_gap, self.max_gap) + self.platform_width  # Увеличение позиции по X
                attempts = 0  # Сбрасываем счетчик после успешного размещения

                # Добавляем дополнительную платформу с меньшей вероятностью
                if random.random() < 0.2:  # Уменьшаем вероятность появления доп. платформ
                    extra_y = random.randint(y - 70, y + 70)  # Генерация высоты для дополнительной платформы
                    extra_x = x - self.min_gap  # Фиксированное расстояние для доп. платформы

                    if self.min_y <= extra_y <= self.max_y and extra_x < chunk_end:  # Проверка на допустимые значения
                        extra_platform = pygame.Rect(
                            extra_x, extra_y,
                            self.platform_width, self.platform_height
                        )
                        if not self.check_platform_collision(extra_platform):  # Проверка на столкновение
                            chunk_platforms.append(extra_platform)  # Добавление дополнительной платформы
            else:
                x += 50  # Небольшой сдвиг при неудачном размещении
                attempts += 1  # Увеличение счетчика попыток

        return chunk_platforms  # Возвращение списка платформ для чанка

    def get_chunk_index(self, x):
        """Получает индекс чанка по координате x"""
        return x // self.chunk_size  # Возвращение индекса чанка

    def generate_chunk(self, target_x):
        """Генерирует новые чанки до указанной x-координаты"""
        target_chunk = self.get_chunk_index(target_x)  # Получение индекса целевого чанка
        current_chunk = self.get_chunk_index(self.last_x)  # Получение индекса текущего чанка

        # Генерируем чанки последовательно
        while current_chunk <= target_chunk:  # Пока текущий чанк меньше или равен целевому
            if current_chunk not in self.loaded_chunks:  # Если чанк еще не загружен
                chunk_start_x = current_chunk * self.chunk_size  # Начальная позиция чанка
                new_platforms = self.generate_platforms_for_chunk(chunk_start_x)  # Генерация платформ для чанка
                self.platforms.extend(new_platforms)  # Добавление новых платформ в общий список
                self.loaded_chunks.add(current_chunk)  # Добавление чанка в загруженные

                # Обновляем last_x только если это самый дальний чанк
                if new_platforms:  # Если есть новые платформы
                    last_platform = max(new_platforms, key=lambda p: p.x + p.width)  # Получение последней платформы
                    self.last_x = max(self.last_x, last_platform.x + last_platform.width)  # Обновление last_x

            current_chunk += 1  # Переход к следующему чанку

    def cleanup_platforms(self, camera_x):
        """Удаляет платформы и чанки, которые остались далеко позади"""
        # Определяем самый ранний видимый чанк
        visible_chunk = self.get_chunk_index(camera_x - screen_width)  # Получение индекса видимого чанка

        # Удаляем старые чанки
        old_chunks = {chunk for chunk in self.loaded_chunks if chunk < visible_chunk - 1}  # Получение старых чанков
        self.loaded_chunks -= old_chunks  # Удаление старых чанков

        # Удаляем платформы из старых чанков
        self.platforms = [p for p in self.platforms if
                          self.get_chunk_index(p.x) >= visible_chunk - 1]  # Оставляем только видимые платформы

    def update(self, camera_x):
        """Обновляет состояние генератора"""
        # Генерируем платформы на два экрана вперед
        self.generate_chunk(camera_x + screen_width * 2)  # Генерация новых чанков
        self.cleanup_platforms(camera_x)  # Очистка старых платформ

        # Обновляем поверхность только для видимой области
        visible_chunk = self.get_chunk_index(camera_x)  # Получение индекса видимого чанка
        next_chunks = {visible_chunk - 1, visible_chunk, visible_chunk + 1}  # Индексы следующих чанков

        # Проверяем, нужно ли загрузить новые чанки
        for chunk in next_chunks:
            if chunk not in self.loaded_chunks and chunk >= 0:  # Если чанк не загружен и его индекс не отрицательный
                self.generate_chunk(chunk * self.chunk_size + self.chunk_size)  # Генерация нового чанка

    def get_platform_surface(self):
        """Создает поверхность для текущих платформ"""
        surface = pygame.Surface((self.level_width, screen_height), pygame.SRCALPHA)  # Создание поверхности
        for platform in self.platforms:  # Перебор всех платформ
            surface.blit(platform_texture, (platform.x, platform.y))  # Отрисовка платформы на поверхности
        self.draw_sign(surface)  # Добавляем отрисовку таблички
        return surface  # Возвращение поверхности

    def draw_sign(self, surface):
        """Рисуем табличку на первой платформе"""
        first_platform = self.platforms[0]  # Получение первой платформы

        # Рисуем саму табличку (прямоугольник)
        sign_rect = pygame.Rect(
            first_platform.x,  # Немного правее от начала платформы
            first_platform.y - 60,  # Над платформой
            150,  # Ширина таблички
            50  # Высота таблички
        )
        pygame.draw.rect(surface, (255, 0, 0), sign_rect)  # Отрисовка таблички
        # Добавляем текст
        text = sign_font.render("Назад дороги нет!", True, (255, 255, 255))  # Создание текстовой поверхности
        text_rect = text.get_rect(center=sign_rect.center)  # Центрирование текста
        surface.blit(text, text_rect)  # Отрисовка текста на табличке


# Заменяем старый код на использование генератора
platform_generator = PlatformGenerator(level_width)  # Создание генератора платформ
platforms = platform_generator.platforms  # Получение платформ
platform_surface = platform_generator.get_platform_surface()  # Получение поверхности платформ

# Обновляем создание поверхности платформ
platform_surface = pygame.Surface((level_width, screen_height), pygame.SRCALPHA)  # Создание поверхности для платформ
for platform in platforms:  # Перебор всех платформ
    platform_surface.blit(platform_texture, (platform.x, platform.y))  # Отрисовка платформы на поверхности


# Добавим функцию для перегенерации уровня при рестарте
def reset_game():
    """Сброс игры"""
    global gg_x, gg_y, camera_x, make_jump, jump_counter, platforms, platform_surface, platform_generator
    gg_x = 50  # Сброс позиции по X
    gg_y = screen_height // 4 - 70  # Сброс позиции по Y
    camera_x = 0  # Сброс позиции камеры
    make_jump = False  # Сброс состояния прыжка
    jump_counter = 30  # Сброс счетчика прыжка

    # Создаем новый генератор платформ
    platform_generator = PlatformGenerator(level_width)  # Создание нового генератора платформ
    platforms = platform_generator.platforms  # Получение платформ
    platform_surface = platform_generator.get_platform_surface()  # Получение поверхности платформ


clock = pygame.time.Clock()  # Создание объекта для управления временем


def death_screen():
    """Экран смерти"""
    while True:  # Цикл, пока экран смерти активен
        mouse_pos = pygame.mouse.get_pos()  # Получение позиции мыши

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                return "exit"  # Возврат значения "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                if restart_btn.collidepoint(mouse_pos):  # Если нажата кнопка "Перезапустить"
                    reset_game()  # Сброс игры
                    return "restart"  # Возврат значения "restart"
                if exit_btn.collidepoint(mouse_pos):  # Если нажата кнопка "Выход"
                    return "exit"  # Возврат значения "exit"

        # Затемнение экрана
        dark_surface = pygame.Surface((screen_width, screen_height))  # Создание затемняющего слоя
        dark_surface.fill((0, 0, 0))  # Заполнение черным цветом
        dark_surface.set_alpha(200)  # Установка прозрачности
        display.blit(dark_surface, (0, 0))  # Отрисовка затемняющего слоя

        # Текст "GAME OVER"
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Создание текстовой поверхности
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 3))  # Центрирование текста
        display.blit(game_over_text, text_rect)  # Отрисовка текста на экране

        # Кнопки
        restart_btn = draw_button("Restart", screen_width // 2 - 150, screen_height // 2, 300, 80, (100, 100, 200),
                                  (50, 50, 150), mouse_pos)
        exit_btn = draw_button("Exit", screen_width // 2 - 150, screen_height // 2 + 120, 300, 80, (200, 100, 100),
                               (150, 50, 50), mouse_pos)

        pygame.display.update()  # Обновление дисплея


def draw_platforms(platforms):
    """Отрисовка платформ"""
    display.blit(platform_surface, (-camera_x, 0))  # Отрисовка поверхности платформ


def check_collision(rect, platforms):
    """Проверка на столкновение"""
    for platform in platforms:  # Перебор всех платформ
        if rect.colliderect(platform):  # Проверка на столкновение
            return True  # Возврат True, если есть столкновение
    return False  # Возврат False, если столкновений нет


def jump():
    """Функция прыжка"""
    global gg_y, jump_counter, make_jump
    if jump_counter >= -JUMP_POWER:  # Если персонаж еще в прыжке
        gg_y -= (jump_counter / 0.5) * (1 - abs(0.1 * jump_counter / JUMP_POWER))  # Изменение позиции по Y
        jump_counter -= 1  # Уменьшение счетчика прыжка
    else:
        jump_counter = JUMP_POWER  # Сброс счетчика прыжка
        make_jump = False  # Сброс состояния прыжка


def run_game():
    """Основной цикл игры"""
    global make_jump, jump_counter, gg_y, gg_x, animation_count, facing_left, is_moving, current_speed, camera_x, background_frame, platform_surface, platforms

    game = True  # Переменная для отслеживания состояния игры
    on_platform = False  # Переменная для отслеживания, находится ли персонаж на платформе
    fall_speed = 0  # Начальная скорость падения

    while game:  # Основной цикл игры
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                return "exit"  # Возврат значения "exit"
            elif event.type == pygame.KEYDOWN:  # Если нажата клавиша
                if event.key == pygame.K_ESCAPE:  # Если нажата клавиша Escape
                    menu_action = pause_menu()  # Показ меню паузы
                    if menu_action in ["exit", "restart"]:  # Если выбрано "выход" или "перезапуск"
                        return menu_action  # Возврат соответствующего значения

        keys = pygame.key.get_pressed()  # Получение состояния клавиш
        is_moving = False  # Сброс состояния движения

        if keys[
            pygame.K_SPACE] and not make_jump and on_platform:  # Если нажата клавиша пробела и персонаж на платформе
            make_jump = True  # Установка состояния прыжка

        if keys[pygame.K_d]:  # Если нажата клавиша "D"
            current_speed = min(current_speed + ACCELERATION, MAX_SPEED)  # Увеличение скорости
            gg_x += current_speed  # Изменение позиции по X
            facing_left = False  # Персонаж смотрит вправо
            is_moving = True  # Установка состояния движения
        elif keys[pygame.K_a]:  # Если нажата клавиша "A"
            current_speed = min(current_speed + ACCELERATION, MAX_SPEED)  # Увеличение скорости
            gg_x -= current_speed  # Изменение позиции по X
            facing_left = True  # Персонаж смотрит влево
            is_moving = True  # Установка состояния движения
        else:
            current_speed = 0  # Сброс скорости
            is_moving = False  # Сброс состояния движения

        if gg_x > screen_width // 2 and current_speed > 0:  # Если персонаж движется вправо
            camera_x = gg_x - screen_width // 2  # Обновление позиции камеры
        camera_x = max(0, min(camera_x, level_width - screen_width))  # Ограничение позиции камеры

        if make_jump:  # Если персонаж прыгает
            jump()  # Вызов функции прыжка

        # Обработка падения
        if not on_platform and not make_jump:  # Если персонаж не на платформе и не прыгает
            fall_speed = min(fall_speed + GRAVITY, MAX_FALL_SPEED)  # Увеличение скорости падения
            gg_y += fall_speed  # Изменение позиции по Y
        else:
            fall_speed = 0  # Сброс скорости падения

        if gg_x < 0:  # Ограничение по X
            gg_x = 0  # Установка границы
        elif gg_x > level_width - gg_width:  # Ограничение по X
            gg_x = level_width - gg_width  # Установка границы

        if gg_y > screen_height:  # Если персонаж упал ниже экрана
            death_result = death_screen()  # Показ экрана смерти
            if death_result == "exit":  # Если выбрано "выход"
                return "exit"  # Возврат значения "exit"
            elif death_result == "restart":  # Если выбрано "перезапуск"
                return "restart"  # Возврат значения "restart"

        rect = pygame.Rect(gg_x, gg_y, gg_width, gg_height)  # Создание прямоугольника персонажа
        future_rect = pygame.Rect(gg_x, gg_y + 5, gg_width, gg_height)  # Прямоугольник для проверки будущей позиции

        if check_collision(rect, platforms):  # Проверка на столкновение
            for platform in platforms:  # Перебор всех платформ
                if rect.colliderect(platform):  # Проверка на столкновение с платформой
                    if gg_y + gg_height > platform.top and gg_y < platform.top:  # Если персонаж касается платформы сверху
                        gg_y = platform.top - gg_height  # Установка позиции персонажа на платформе
                        on_platform = True  # Установка состояния "на платформе"
                        break  # Выход из цикла
        elif check_collision(future_rect, platforms):  # Проверка на столкновение с будущей позицией
            on_platform = True  # Установка состояния "на платформе"
        else:
            on_platform = False  # Сброс состояния "на платформе"

        animation_count += 1  # Увеличение счетчика анимации

        if make_jump:  # Если персонаж прыгает
            frames = animation_jump_left if facing_left else animation_jump  # Выбор кадров анимации
            frame_index = (animation_count // 5) % len(frames)  # Индекс текущего кадра
            current_frame = frames[frame_index]  # Получение текущего кадра
        elif is_moving:  # Если персонаж движется
            frames = animation_left if facing_left else animation_right  # Выбор кадров анимации
            frame_index = (animation_count // 5) % len(frames)  # Индекс текущего кадра
            current_frame = frames[frame_index]  # Получение текущего кадра
        else:  # Если персонаж не движется
            frame_index = (animation_count // 10) % len(animation_idle)  # Индекс текущего кадра
            current_frame = animation_idle[frame_index]  # Получение текущего кадра

        background_frame = (background_frame + 1) % len(background_animation)  # Обновление кадра фона
        display.blit(background_animation[background_frame], (0, 0))  # Отрисовка фона
        draw_platforms(platforms)  # Отрисовка платформ
        display.blit(current_frame, (gg_x - camera_x, gg_y))  # Отрисовка персонажа

        # Обновляем генератор платформ
        platform_generator.update(camera_x)  # Обновление генератора платформ
        platforms = platform_generator.platforms  # Получение платформ

        # Простая отрисовка платформ без эффектов
        for platform in platforms:  # Перебор всех платформ
            if platform.x - camera_x > -platform.width and platform.x - camera_x < screen_width:  # Проверка видимости платформы
                display.blit(platform_texture, (platform.x - camera_x, platform.y))  # Отрисовка платформы

        pygame.display.update()  # Обновление дисплея
        clock.tick(60)  # Ограничение FPS


def main():
    """Основная функция игры"""
    running = True  # Переменная для отслеживания состояния игры
    while running:  # Основной цикл игры
        result = run_game()  # Запуск игры
        if result == "exit":  # Если выбрано "выход"
            running = False  # Завершение игры
        elif result == "restart":  # Если выбрано "перезапуск"
            reset_game()  # Сброс игры
            continue  # Продолжение цикла


# Инициализация микшера Pygame
pygame.mixer.init()  # Инициализация звукового модуля Pygame

# Загрузка фонового звука
background_music = os.path.join(base_path, 'sound', 'background_music.mp3')  # Путь к фоновому звуку
pygame.mixer.music.load(background_music)  # Загрузка фонового звука
pygame.mixer.music.set_volume(0.5)  # Установка громкости фонового звука
pygame.mixer.music.play(-1)  # Воспроизведение фонового звука в бесконечном цикле

main()  # Запуск основной функции игры
pygame.quit()  # Завершение Pygame
