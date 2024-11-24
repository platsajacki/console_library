import os
from csv import DictReader, DictWriter
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from core.data_types import Model, ModelDict
from core.exceptions import IDErorr
from core.interfaces import DataManager


@dataclass
class CSVDataManager(DataManager):
    path: str | Path
    fieldnames: list[str]
    id_field: str = 'id'

    def __post_init__(self):
        """Проверяем после создания эксземпляра класса, что файл существует и является CSV."""
        if not self._is_csv():
            raise ValueError(f'Файл {self.path} не является CSV файлом.')
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'a'):
                ...
        self.fields = [self.id_field] + self.fieldnames
        self.max_id = self.get_max_id()

    def get_max_id(self) -> int:
        """Получаем максимальный id из файла."""
        all_rows = self._read()
        if not all_rows:
            return 0
        return max(list(all_rows.keys()))

    def get_id(self) -> int:
        """Присваиваем id новому объекту."""
        self.max_id = self.max_id + 1
        return self.max_id

    def _read(self) -> dict[int, ModelDict]:
        """Получаем все объекты из файле."""
        data = {}
        with open(self.path, mode='r') as file:
            reader = DictReader(file, fieldnames=self.fields)
            next(reader, None)
            for row in reader:
                data[int(row['id'])] = row
            return data

    def _is_csv(self) -> bool:
        """Проверяет, что файл имеет расширение .csv."""
        fmt = '.csv'
        if isinstance(self.path, str):
            return self.path.lower().endswith(fmt)
        if isinstance(self.path, Path):
            return self.path.suffix.lower() == fmt
        return False

    def _write(self, data: ModelDict) -> None:
        """Перезаписывает файл с нуля."""
        with open(self.path, mode='w') as file:
            writer = DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(list(data.values()))

    def _get_model_dict(self, id: int, data: dict[int, ModelDict]) -> ModelDict:
        try:
            return data[id]
        except KeyError:
            raise IDErorr(message=f'ID {id} не существует.')

    def create(self, data: Model | Sequence[Model]) -> ModelDict | list[ModelDict]:
        with open(self.path, mode='a') as file:
            writer = DictWriter(f=file, fieldnames=self.fields)
            if file.tell() == 0:
                writer.writeheader()
            write_data: ModelDict | list[ModelDict]
            if isinstance(data, Sequence):
                write_data = [d.to_dict() | {self.id_field: self.get_id()} for d in data]
                writer.writerows(write_data)
            else:
                write_data = data.to_dict() | {self.id_field: self.get_id()}
                writer.writerow(write_data)
            return write_data

    def read_list(self) -> list[ModelDict]:
        return list(self._read().values())

    def read_detail(self, id: int) -> ModelDict:
        return self._get_model_dict(id, self._read())

    def udate(self, id: int, data: Model) -> ModelDict:
        objects = self._read()
        model_data = {self.id_field: id} | data.to_dict()
        self._get_model_dict(id, objects)
        objects[id] = model_data
        self._write(objects)
        return model_data

    def delete(self, id: int) -> ModelDict:
        objects = self._read()
        obj = self._get_model_dict(id, objects)
        del objects[id]
        self._write(objects)
        return obj

    def search(self, field: str, value: str) -> list[ModelDict]:
        if field not in self.fieldnames:
            raise ValueError('Поля %s нет в файле.' % field)
        objects = self.read_list()
        data = []
        for obj in objects:
            if value.lower() in obj[field].lower():
                data.append(obj)
        return data
