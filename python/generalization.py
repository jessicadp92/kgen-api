from datetime import datetime

# -------------------------
# Numeric / Age Generalization
# -------------------------
class NumericGeneralization:
    @staticmethod
    def generalize(value, level):
        if value is None:
            return None
        value = int(value)
        if level == 0:
            return str(value)
        multiple = 10 ** level
        lower = (value // multiple) * multiple
        upper = lower + multiple - 1
        return f"{lower}-{upper}"


class AgeGeneralization(NumericGeneralization):
    @staticmethod
    def generalize(value, level):
        if value is None:
            return None
        value = int(value)
        if level == 0:
            return value
        elif level == 1:
            decade_start = (value // 10) * 10
            return f"{decade_start}-{decade_start + 9}"
        elif level == 2:
            return "adult" if value >= 18 else "minor"
        else:
            return "*"


# -------------------------
# String Generalization
# -------------------------
class StringGeneralization:
    @staticmethod
    def generalize(value, level, min_length=1):
        if value is None:
            return None
        s = str(value)
        if level == 0:
            return s
        if level >= len(s):
            return "*" * len(s)
        # Mascheramento finale
        masked_len = max(len(s) - level, min_length)
        return s[:masked_len] + "*" * (len(s) - masked_len)


# -------------------------
# Date Generalization
# -------------------------
class DateGeneralization:
    @staticmethod
    def generalize(value, level):
        if value is None:
            return None
        # Convert string to date if needed
        if isinstance(value, str):
            try:
                date_obj = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                return value
        else:
            date_obj = value

        if level == 0:
            return date_obj.strftime("%d/%m/%Y")
        elif level == 1:
            return date_obj.strftime("%m/%Y")
        elif level == 2:
            return str(date_obj.year)
        elif level == 3:
            decade_start = (date_obj.year // 10) * 10
            return f"{decade_start}-{decade_start + 9}"
        elif level == 4:
            range_start = (date_obj.year // 50) * 50
            return f"{range_start}-{range_start + 49}"
        else:
            return "*"


# -------------------------
# Place Generalization
# -------------------------
class PlaceGeneralization:
    @staticmethod
    def generalize(value, level):
        if value is None:
            return None
        if level == 0:
            return value
        elif level == 1:
            return "Region"   # placeholder, in futuro usare mappa reale
        elif level == 2:
            return "Country"
        elif level >= 3:
            return "Worldwide"
        return value