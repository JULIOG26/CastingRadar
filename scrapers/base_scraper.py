from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def scrape(self):
        """
        Debe devolver una lista de objetos Casting.
        """
        pass