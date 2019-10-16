# импортируем специальные поля Алхимии для инициализации полей таблицы
from sqlalchemy import Column, DateTime, String, Integer, Float, Boolean, ForeignKey
# импортируем модуль инициализации декларативного класса Алхимии
from DB.dbcore import Base


class Category(Base):
    """
    Класс для создания таблицы Category товара, основан на декларативном стиле sqlalchemy
    """
    # Инициализация полей таблицы
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __repr__(self):
        """
        Метод возвращает формальное строковое представление указанного объекта
        """
        return self.name