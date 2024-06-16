
WELCOME_MESSAGE = "Привет артистам"

GALERY_MESSAGE = "Галерея"

REG_GET_PROFILE_INFO_MESSAGE = "Ввдеите пару строк о себе, которые будут отображаться в профиле"

NO_PICTURE_FOR_USER = "Для вас нет картинок"

RATE_PICTURE_MSG = "Оцените изображение по 5бальной шкале"

REVIEW_SUCCESS_ADDED = "Ревью добавлено"

REVIEW_FAILED_ADDED = "Ревью НЕ добавлено"

NO_REVIEW_FOR_PICTURE = "Нет ревью"

DESCRIBE_PICTURE_RATE_MSG = "Оставьте отзыв на пикчу"

SWITCH_TO_PICTURE_LINE = "Переход в ленту"

REG_GET_BIRTHDAY_MESSAGE = "Введите дату рождения"

REG_GET_CONTENT_MARK = "Отображать изображения 18+ в ленте?"

REGISTER_NEW_USER_MESSAGE = "REGISTER_NEW_USER_MESSAGE"

PROFILE_MESSAGE = "PROFILE_MESSAGE"

PROFILE_INFO_MESSAGE = "PROFILE_INFO_MESSAGE"

PICTURE_UPLOAD_SUCCESS = "Пикча успешно загружена"

PICTURE_UPLOAD_FAILED = "Пикча НЕ загружена"

PICTURE_DELETE_SUCCESS = "Пикча усешно удалена"

PICTURE_DELETE_FAILED = "Пикча НЕ удалена"

PICTURE_LIMIT_REACHED = "Достигнут лимит публикаций"

USER_NOT_FOUND = "Вы не зарегестрированы в боте. Пройдите регистрацию"

USER_ALREADY_EXISTS = "Пользователь уже зарегестрирован в системе"

REGISTER_NOT_FINISHED = "Вы не завершили регистрацию"

IS_R_CONTENT = "Это изображение 18+ ?"

BOT_DESCRIPTION = "Ето бот"

def FormProfileInfo(username, links, reviewCounter, published, description, averageRating):
    return f'''@{username}\nОписание - {description}\nСсылки - {links}\nОпубликовано работ - {published}\nСредняя оценка работ - {averageRating}\nОценено чужих работ - {reviewCounter}'''

def FormPictureCaption(description, averageRating, userName = ''):
    if len(userName) == 0:
        return f'''Описание: {description}\nСредний рейинг: {averageRating}'''
    else:
        return f'''Автор: @{userName}\nОписание: {description}\nСредний рейинг: {averageRating}'''
    
    