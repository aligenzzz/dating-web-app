from typing import Any


class AppState:
    _state: dict[str, Any] = {}

    @classmethod
    def set(cls, key, value):
        cls._state[key] = value

    @classmethod
    def get(cls, key):
        return cls._state.get(key)

    @classmethod
    def clear(cls):
        cls._state.clear()
