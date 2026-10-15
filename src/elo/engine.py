from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class Prediction:
    prediction: str
    confidence: str
    logic_exploit: str
    layer: str
    epa_swing: float

@dataclass
class Grade:
    call: Literal["BUY", "FADE", "HOLD", "DISTRESSED", "STANDARD"]
    side: str
    line: str
    why: str
    anomalies: list[str]
    weight: int
    row: Optional[dict] = None
