

from collections import deque
from abc import ABCMeta, abstractmethod

class PoolableObject(metaclass=ABCMeta):
    """
    Базовый класс для объектов, поддерживающих повторное использование
    без пересоздавания.
    """
    
    pool = deque()

    @classmethod
    def create(cls, *args):
        if len(cls.pool) == 0:
            return cls(*args)
        else:
            obj = cls.pool.pop()
            obj.reset(*args)
            return obj

    def delete(self, group):
        group.remove(self)
        self.pool.append(self)

    @abstractmethod
    def reset(self, *args):
        pass
