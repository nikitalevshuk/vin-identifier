# Таблица значений VIN-символов
VIN_TRANSLATION = {
    **{str(i): i for i in range(10)},  # Цифры 0-9
    **{
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
        "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
        "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9
    }
}

# Весовые коэффициенты для VIN (без контрольного знака)
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

def calculate_vin_checksum(vin):
    """Рассчитывает контрольную сумму VIN-кода по ISO 3779."""
    total = sum(VIN_TRANSLATION[vin[i]] * VIN_WEIGHTS[i] for i in range(17) if i != 8)
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)


def check_vin(vin):
    """Проверяет, соответствует ли VIN-код стандарту ISO 3779 (формат + контрольная сумма)."""

    # 1. Проверяем длину
    if len(vin) != 17:
        return False, "Неверная длина VIN (должно быть 17 символов)."

    # 2. Проверяем запрещенные символы
    if any(char in "IOQ" for char in vin):
        return False, "VIN не должен содержать буквы I, O, Q."

    # 3. Проверяем, что 12-17 символы – только цифры (серийный номер)
    if not vin[11:].isdigit():
        return False, "Серийный номер (12-17 символы) должен содержать только цифры."

    # 4. Проверяем контрольную сумму
    expected_checksum = calculate_vin_checksum(vin)
    if vin[8] != expected_checksum:
        return False, f"Ошибка контрольной суммы: ожидалось {expected_checksum}, получено {vin[8]}"

    return True