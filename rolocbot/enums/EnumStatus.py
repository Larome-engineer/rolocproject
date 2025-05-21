from enum import Enum


class EnumApplicationsStatus(Enum):
    NEW = 'Новая'
    PROCESSING = 'В обработке'
    PREPARE = 'Составление ТЗ'
    WAITING_PAY = 'Ожидание оплаты'
    IN_WORK = 'В работе дизайнера'
    EDITS = 'Правки'
    COMPLETE = 'Завершена'

class EnumHelpStatus(Enum):
    WAITING = 'В ожидании'
    COMPLETE = 'Обработан'
