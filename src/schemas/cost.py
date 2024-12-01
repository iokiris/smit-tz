import datetime

from pydantic import BaseModel, root_validator, model_validator
from typing import Dict, List


class CargoItem(BaseModel):
    cargo_type: str
    rate: float

    @model_validator(mode='before')
    def validate_float(cls, values):
        if 'rate' in values:
            values['rate'] = float(values['rate'])
        return values


class CargoCost(BaseModel):
    data: Dict[datetime.date, List[CargoItem]]

