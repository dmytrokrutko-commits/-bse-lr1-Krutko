"""
HookCraft — модуль реалізації UML-моделі з ЛР №2.

Класи: User, Guest, RegisteredUser, Admin,
       Hook, History, GenerationRequest, AuthService
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import List, Optional


# ---------------------------------------------------------------------------
# Виключення
# ---------------------------------------------------------------------------

class AuthError(Exception):
    """Помилка автентифікації."""


class LimitExceededError(Exception):
    """Перевищено ліміт генерацій."""


class ValidationError(Exception):
    """Помилка валідації вхідних даних."""


# ---------------------------------------------------------------------------
# Hook
# ---------------------------------------------------------------------------

VALID_STYLES = {"intriguing", "humorous", "neutral"}


class Hook:
    """Один текстовий «гачок»."""

    def __init__(self, hook_id: int, text: str, style: str) -> None:
        if not text or not text.strip():
            raise ValidationError("Hook text must not be empty.")
        if style not in VALID_STYLES:
            raise ValidationError(
                f"Unknown style '{style}'. Valid: {VALID_STYLES}"
            )
        self.id: int = hook_id
        self.text: str = text.strip()
        self.style: str = style
        self.is_favorite: bool = False
        self.created_at: datetime = datetime.utcnow()

    def copy_to_clipboard(self) -> str:
        """Повертає текст (імітація копіювання у буфер)."""
        return self.text

    def get_text(self) -> str:
        return self.text

    def __repr__(self) -> str:  # pragma: no cover
        return f"Hook(id={self.id}, style={self.style!r}, text={self.text[:30]!r})"


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------

class History:
    """Список гачків конкретного користувача (композиція з RegisteredUser)."""

    def __init__(self) -> None:
        self._hooks: List[Hook] = []

    @property
    def list_of_hooks(self) -> List[Hook]:
        return list(self._hooks)

    def add_hook(self, hook: Hook) -> None:
        if not isinstance(hook, Hook):
            raise ValidationError("Only Hook instances can be added to History.")
        self._hooks.append(hook)

    def clear_history(self) -> None:
        self._hooks.clear()

    def __len__(self) -> int:
        return len(self._hooks)


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User:
    """Базовий клас користувача."""

    _next_id: int = 1

    def __init__(self, email: str, role: str) -> None:
        self.id: int = User._next_id
        User._next_id += 1
        self.email: str = email
        self.role: str = role
        self.registration_date: datetime = datetime.utcnow()
        self._password_hash: Optional[str] = None

    # ------------------------------------------------------------------
    # authenticate — нетривіальна логіка: валідація email + хеш пароля
    # ------------------------------------------------------------------
    def authenticate(self, email: str, password: str) -> bool:
        """
        Перевіряє email та пароль.

        Правила:
        - email має містити '@' та домен із крапкою
        - пароль не порожній та не коротший за 6 символів
        - порівнюємо SHA-256-хеш із збереженим
        """
        # валідація email
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email format: {email!r}")

        # валідація довжини пароля
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters.")

        if email != self.email:
            return False
        if self._password_hash is None:
            return False

        incoming_hash = hashlib.sha256(password.encode()).hexdigest()
        return incoming_hash == self._password_hash

    def set_password(self, password: str) -> None:
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters.")
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    def get_history(self) -> List[Hook]:
        """Базова реалізація — порожній список (перевизначається у підкласах)."""
        return []


# ---------------------------------------------------------------------------

class Guest(User):
    """Незареєстрований користувач."""

    DEFAULT_LIMIT = 3

    def __init__(self) -> None:
        super().__init__(email="guest@hookcraft.local", role="guest")
        self.remaining_generations: int = self.DEFAULT_LIMIT

    # ------------------------------------------------------------------
    # use_trial — нетривіальна логіка: декремент з обробкою ліміту
    # ------------------------------------------------------------------
    def use_trial(self) -> int:
        """
        Зменшує лічильник пробних генерацій.
        Повертає залишок. Кидає LimitExceededError при вичерпанні.
        """
        if self.remaining_generations <= 0:
            raise LimitExceededError(
                "Trial limit exceeded. Please register to continue."
            )
        self.remaining_generations -= 1
        return self.remaining_generations


# ---------------------------------------------------------------------------

class RegisteredUser(User):
    """Зареєстрований користувач."""

    def __init__(self, email: str) -> None:
        super().__init__(email=email, role="registered")
        self.favorite_hooks: List[Hook] = []
        self._history: History = History()

    def save_to_favorites(self, hook: Hook) -> None:
        if not isinstance(hook, Hook):
            raise ValidationError("Only Hook instances can be saved.")
        if hook not in self.favorite_hooks:
            hook.is_favorite = True
            self.favorite_hooks.append(hook)

    def view_history(self) -> List[Hook]:
        return self._history.list_of_hooks

    def get_history(self) -> List[Hook]:
        return self.view_history()

    @property
    def history(self) -> History:
        return self._history


# ---------------------------------------------------------------------------

class Admin(User):
    """Адміністратор системи."""

    def __init__(self, email: str) -> None:
        super().__init__(email=email, role="admin")
        self._user_limit: int = Guest.DEFAULT_LIMIT

    def manage_users(self, users: List[User]) -> dict:
        """Повертає статистику по ролях."""
        stats: dict = {}
        for u in users:
            stats[u.role] = stats.get(u.role, 0) + 1
        return stats

    def update_limits(self, new_limit: int) -> None:
        """Оновлює глобальний ліміт пробних генерацій."""
        if new_limit < 0:
            raise ValidationError("Limit must be non-negative.")
        Guest.DEFAULT_LIMIT = new_limit
        self._user_limit = new_limit


# ---------------------------------------------------------------------------
# GenerationRequest
# ---------------------------------------------------------------------------

class GenerationRequest:
    """Запит на генерацію гачків."""

    _counter: int = 0

    def __init__(self, topic: str, style: str, user_id: int) -> None:
        GenerationRequest._counter += 1
        self.request_id: int = GenerationRequest._counter
        self.topic: str = topic
        self.style: str = style
        self.timestamp: datetime = datetime.utcnow()
        self.user_id: int = user_id
        self._result: List[Hook] = []

    # ------------------------------------------------------------------
    # submit — нетривіальна логіка: валідація + генерація шаблонних гачків
    # ------------------------------------------------------------------
    def submit(self) -> List[Hook]:
        """
        Формує список Hook-об'єктів на основі теми та стилю.

        Правила:
        - тема не порожня та не довша за 200 символів
        - стиль з дозволеного набору
        - генерується 3 варіанти (у prod замінити на виклик OpenAI API)
        """
        topic = self.topic.strip()
        if not topic:
            raise ValidationError("Topic must not be empty.")
        if len(topic) > 200:
            raise ValidationError("Topic must not exceed 200 characters.")
        if self.style not in VALID_STYLES:
            raise ValidationError(
                f"Invalid style '{self.style}'. Valid: {VALID_STYLES}"
            )

        templates = {
            "intriguing": [
                f"Ви навіть не уявляєте, що ховається за темою «{topic}»…",
                f"Один факт про «{topic}», який змінить ваш погляд назавжди.",
                f"Це знають одиниці: таємниця «{topic}» розкрита.",
            ],
            "humorous": [
                f"«{topic}» — звучить серйозно, але насправді це смішно.",
                f"Якщо б «{topic}» було мемом, воно б виглядало саме так.",
                f"Моя кішка теж знає все про «{topic}». Ну, майже.",
            ],
            "neutral": [
                f"Все, що вам потрібно знати про «{topic}».",
                f"Короткий огляд теми «{topic}».",
                f"Основні тези щодо «{topic}».",
            ],
        }

        self._result = [
            Hook(hook_id=i + 1, text=t, style=self.style)
            for i, t in enumerate(templates[self.style])
        ]
        return self._result

    def get_result(self) -> List[Hook]:
        """Повертає вже згенеровані гачки (або порожній список)."""
        return list(self._result)


# ---------------------------------------------------------------------------
# AuthService
# ---------------------------------------------------------------------------

class AuthService:
    """Сервіс реєстрації та автентифікації."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}   # email -> User

    # ------------------------------------------------------------------
    # register — нетривіальна логіка: унікальність email + валідація
    # ------------------------------------------------------------------
    def register(self, email: str, password: str) -> RegisteredUser:
        """
        Реєструє нового користувача.

        Правила:
        - коректний формат email
        - пароль ≥ 6 символів
        - email ще не зареєстрований
        """
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email: {email!r}")
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters.")
        if email in self._users:
            raise AuthError(f"Email already registered: {email!r}")

        user = RegisteredUser(email=email)
        user.set_password(password)
        self._users[email] = user
        return user

    def login(self, email: str, password: str) -> User:
        """Перевіряє облікові дані і повертає User."""
        if email not in self._users:
            raise AuthError("User not found.")
        user = self._users[email]
        if not user.authenticate(email, password):
            raise AuthError("Wrong password.")
        return user

    def logout(self, user: User) -> None:
        """Завершення сесії (у спрощеній реалізації — заглушка)."""
        # У реальній системі тут анулювався б JWT-токен
        pass
