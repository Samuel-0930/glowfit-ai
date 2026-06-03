from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from src.glowfit.schemas import Product, Review, UserPreferences

ModelT = TypeVar("ModelT", bound=BaseModel)


def _read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_list(path: Path, model: type[ModelT]) -> list[ModelT]:
    payload = _read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"Expected list payload in {path}")
    return [model.model_validate(item) for item in payload]


def load_products(path: Path) -> list[Product]:
    return _load_list(path, Product)


def load_reviews(path: Path) -> list[Review]:
    return _load_list(path, Review)


def load_preferences(path: Path) -> UserPreferences:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected object payload in {path}")
    return UserPreferences.model_validate(payload)
