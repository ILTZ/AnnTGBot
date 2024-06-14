
WELCOME_MESSAGE = "Привет артистам"

GET_PROFILE_INFO_MESSAGE = "Ввдеите пару строк о себе, которые будут отображаться в профиле"

GET_BIRTHDAY_MESSAGE = "Введите дату рождения"

GET_CONTENT_MARK = "Отображать изображения 18+ в ленте?"

REGISTER_NEW_USER_MESSAGE = "REGISTER_NEW_USER_MESSAGE"

PROFILE_MESSAGE = "PROFILE_MESSAGE"

PROFILE_INFO_MESSAGE = "PROFILE_INFO_MESSAGE"

PICTURE_UPLOAD_SUCCESS = "Пикча успешно загружена"

PICTURE_UPLOAD_FAILED = "Пикча НЕ загружена"

PICTURE_LIMIT_REACHED = "Достигнут лимит публикаций"

USER_NOT_FOUND = "Вы не зарегестрированы в боте. Пройдите регистрацию"

USER_ALREADY_EXISTS = "Пользователь уже зарегестрирован в системе"

REGISTER_NOT_FINISHED = "Вы не завершили регистрацию"

BOT_DESCRIPTION = "Ето бот"

def FormProfileInfo(username, links, reviewCounter, published, description, averageRating):
    return f'''@{username}\n
                Описание - {description}\n
                Ссылки - {links}\n
                Опубликовано работ - {published}\n
                Средняя оценка работ - {averageRating}\n
                Оценено чужих работ - {reviewCounter}'''