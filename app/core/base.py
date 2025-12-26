from abc import ABC, abstractmethod
from typing import Any, List, Union
from numpy.typing import NDArray

class FacialRecognition(ABC):
    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def forward(self, img: NDArray[Any]) -> Any:
        pass