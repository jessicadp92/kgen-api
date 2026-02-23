from dataclasses import dataclass

from python.generalization import NumericGeneralization, AgeGeneralization, StringGeneralization, DateGeneralization, \
    PlaceGeneralization


@dataclass
class ColumnMeta:
    Name: str
    IDType: str    # "i", "qi", "s"
    DateType: str  # "string", "place", "age", "int", "date"
    PK: bool


class Dataset:
    def __init__(self, rows: list[dict], metadata: list[ColumnMeta]):
        self.rows = rows
        self.metadata = metadata

        self.columns = {m.Name: [r.get(m.Name) for r in rows] for m in metadata}
        self.qi_cols = [m for m in metadata if m.IDType == "qi"]
        self.id_cols = [m for m in metadata if m.IDType == "i"]
        self.safe_cols = [m for m in metadata if m.IDType == "s"]

        self.qi_names = [m.Name for m in self.qi_cols]
        self.size = len(rows)

    def compute_upper_bounds(self):
        bounds = []
        for col in self.qi_cols:
            values = self.columns[col.Name]

            if col.DateType == "int":
                max_val = max(v for v in values if v is not None)
                bounds.append(len(str(abs(int(max_val)))))

            elif col.DateType == "age":
                bounds.append(3)

            elif col.DateType == "date":
                bounds.append(3)

            elif col.DateType == "string":
                max_len = max(len(str(v)) for v in values if v is not None)
                bounds.append(max_len)

            elif col.DateType == "place":
                bounds.append(3)

            else:
                bounds.append(1)

        return bounds

    def compute_lower_bounds(self):
        return [0] * len(self.qi_cols)

    def generalize_value(self, value, level, data_type):
        if data_type in ("int", "numeric"):
            return NumericGeneralization.generalize(value, level)
        elif data_type == "age":
            return AgeGeneralization.generalize(value, level)
        elif data_type == "string":
            return StringGeneralization.generalize(value, level)
        elif data_type == "date":
            return DateGeneralization.generalize(value, level)
        elif data_type == "place":
            return PlaceGeneralization.generalize(value, level)
        else:
            return value

    def generalize_row(self, row: dict, levels: list[int]):
        new_row = row.copy()

        for lvl, meta in zip(levels, self.qi_cols):
            new_row[meta.Name] = self.generalize_value(
                row.get(meta.Name),
                lvl,
                meta.DateType
            )

        for meta in self.id_cols:
            new_row[meta.Name] = "*****"

        return new_row

    def generalize_dataset(self, levels: list[int]):
        return [self.generalize_row(r, levels) for r in self.rows]