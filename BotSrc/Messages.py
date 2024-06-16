WELCOME_MESSAGE = "Привет артистам"

GALERY_MESSAGE = "Галерея"


REPORT_MESSAGE = "Опишите, что вас не уcтроило"

REPORT_ADDED_SUCCESS = "Репорт отправлен"


PROCESS_FAILED = "Ooops"

PROCESS_RESTART = "Попробуйте снова"


REG_GET_PROFILE_INFO_MESSAGE = "Ввдеите пару строк о себе, которые будут отображаться в профиле"

REG_GET_LINKS = "Введите ссылки на свои соц сети через запятую"

REG_GET_BIRTHDAY_MESSAGE = "Введите дату рождения в формате DD-MM-YYYY" 

REG_GET_CONTENT_MARK = "Отображать изображения 18+ в ленте?"

REG_NEW_USER_MESSAGE = "REGISTER_NEW_USER_MESSAGE"


REDACT_LINKS_MSG = "Введите новые ссылки через зпт"

REDACT_DESCRIPTION_MSG = "Введите новое описание"

DELETE_PROFILE_MSG = "Вы уверены, что хотите удалить профиль?"

PROFILE_WAS_DELETED = "Профиль был удален"

PROFILE_WAS_SAVED = "Профиль не удален"

UPDATE_SUCCES_MSG = "Успешно обновлено"



NO_PICTURE_FOR_USER = "Для вас нет картинок"

RATE_PICTURE_MSG = "Оцените изображение по 5бальной шкале"

REVIEW_SUCCESS_ADDED = "Ревью добавлено"

REVIEW_FAILED_ADDED = "Ревью НЕ добавлено"

NO_REVIEW_FOR_PICTURE = "Нет ревью"

DESCRIBE_PICTURE_RATE_MSG = "Оставьте отзыв на пикчу"

SWITCH_TO_PICTURE_LINE = "Переход в ленту"

PROFILE_MESSAGE = "PROFILE_MESSAGE"

PROFILE_INFO_MESSAGE = "PROFILE_INFO_MESSAGE"

AUTOR_SEARCH_MODE = "Введите uwername автора"

AUTOR_NOT_FOUND = "Автор не найден"


PICTURE_UPLOAD_SUCCESS = "Пикча успешно загружена"

PICTURE_DELETE_SUCCESS = "Пикча усешно удалена"

PICTURE_LIMIT_REACHED = "Достигнут лимит публикаций"

USER_NOT_FOUND = "Вы не зарегестрированы в боте. Пройдите регистрацию"

USER_ALREADY_EXISTS = "Пользователь уже зарегестрирован в системе"

REGISTER_NOT_FINISHED = "Вы не завершили регистрацию"

IS_R_CONTENT = "Это изображение 18+ ?"

BOT_DESCRIPTION = "Ето бот"


def FormProfileInfo(username, links, reviewCounter, published, description, averageRating):
    return f'''@{username}\nОписание - {description}\nСсылки - {links}\nОпубликовано работ - {published}\nСредняя оценка работ - {averageRating}\nОценено чужих работ - {reviewCounter}'''

def FormPictureCaption(description, averageRating = 0.0, userName = ''):

    text = ''''''

    if (len(userName)):
        text = text + f'''Автор: @{userName}\n'''

    text = text + f'''Описание: {description}\n'''

    if averageRating != 0.0:
        text = text + f'''Средний рейинг: {averageRating}\n'''

    return text
    
    
        
    
    