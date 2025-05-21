from enums.EnumStatus import EnumApplicationsStatus, EnumHelpStatus

def convert_help_to_value(status: str):
    if status == EnumHelpStatus.WAITING.name:
        return EnumHelpStatus.WAITING.value
    elif status == EnumHelpStatus.COMPLETE.name:
        return EnumHelpStatus.COMPLETE.value
    else:
        return 'Такого статуса не существует'

def convert_help_to_name(status: str):
    if status == EnumHelpStatus.WAITING.value:
        return EnumHelpStatus.WAITING.name
    elif status == EnumHelpStatus.COMPLETE.value:
        return EnumHelpStatus.COMPLETE.name
    else:
        return 'Такого статуса не существует'

def convert_to_enum_value(status: str) -> str:
    if status == EnumApplicationsStatus.NEW.name:
        return EnumApplicationsStatus.NEW.value
    elif status == EnumApplicationsStatus.PROCESSING.name:
        return EnumApplicationsStatus.PROCESSING.value
    elif status == EnumApplicationsStatus.PREPARE.name:
        return EnumApplicationsStatus.PREPARE.value
    elif status == EnumApplicationsStatus.WAITING_PAY.name:
        return EnumApplicationsStatus.WAITING_PAY.value
    elif status == EnumApplicationsStatus.IN_WORK.name:
        return EnumApplicationsStatus.IN_WORK.value
    elif status == EnumApplicationsStatus.EDITS.name:
        return EnumApplicationsStatus.EDITS.value
    elif status == EnumApplicationsStatus.COMPLETE.name:
        return EnumApplicationsStatus.COMPLETE.value
    else:
        return 'Такого статуса не существует'


def convert_to_enum_name(status: str) -> str:
    if status == EnumApplicationsStatus.NEW.value:
        return EnumApplicationsStatus.NEW.name

    elif status == EnumApplicationsStatus.PROCESSING.value:
        return EnumApplicationsStatus.PROCESSING.name

    elif status == EnumApplicationsStatus.PREPARE.value:
        return EnumApplicationsStatus.PREPARE.name

    elif status == EnumApplicationsStatus.WAITING_PAY.value:
        return EnumApplicationsStatus.WAITING_PAY.name

    elif status == EnumApplicationsStatus.IN_WORK.value:
        return EnumApplicationsStatus.IN_WORK.name

    elif status == EnumApplicationsStatus.EDITS.value:
        return EnumApplicationsStatus.EDITS.name

    elif status == EnumApplicationsStatus.COMPLETE.value:
        return EnumApplicationsStatus.COMPLETE.name

    else:
        return 'Такого статуса не существует'

