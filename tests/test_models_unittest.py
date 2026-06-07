"""
Модульні тести для hookcraft.models (unittest)
Кожен тест відповідає патерну AAA (Arrange / Act / Assert).
Техніка: EP / BVA / позитивний / негативний — у коментарях.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from hookcraft.models import (
    Admin,
    AuthError,
    AuthService,
    GenerationRequest,
    Guest,
    History,
    Hook,
    LimitExceededError,
    RegisteredUser,
    User,
    ValidationError,
)


# ===========================================================================
# Hook
# ===========================================================================

class TestHook(unittest.TestCase):

    def test_create_valid_hook_intriguing(self):
        # EP: valid style, non-empty text (позитивний)
        # Arrange / Act
        hook = Hook(1, "Якась тема", "intriguing")
        # Assert
        self.assertEqual(hook.text, "Якась тема")
        self.assertEqual(hook.style, "intriguing")
        self.assertFalse(hook.is_favorite)

    def test_create_valid_hook_humorous(self):
        # EP: valid style "humorous" (позитивний)
        hook = Hook(2, "Смішна тема", "humorous")
        self.assertEqual(hook.style, "humorous")

    def test_create_valid_hook_neutral(self):
        # EP: valid style "neutral" (позитивний)
        hook = Hook(3, "Нейтральна тема", "neutral")
        self.assertEqual(hook.style, "neutral")

    def test_empty_text_raises(self):
        # EP: порожній рядок → ValidationError (негативний)
        with self.assertRaises(ValidationError):
            Hook(1, "", "intriguing")

    def test_whitespace_only_text_raises(self):
        # BVA: рядок тільки з пробілів (негативний)
        with self.assertRaises(ValidationError):
            Hook(1, "   ", "intriguing")

    def test_invalid_style_raises(self):
        # EP: недозволений стиль (негативний)
        with self.assertRaises(ValidationError):
            Hook(1, "Тема", "unknown_style")

    def test_copy_to_clipboard_returns_text(self):
        # EP: перевірка методу (позитивний)
        hook = Hook(1, "Мій текст", "neutral")
        self.assertEqual(hook.copy_to_clipboard(), "Мій текст")

    def test_text_stripped_on_creation(self):
        # BVA: пробіли на краях мають обрізатись (позитивний)
        hook = Hook(1, "  текст  ", "neutral")
        self.assertEqual(hook.text, "текст")


# ===========================================================================
# History
# ===========================================================================

class TestHistory(unittest.TestCase):

    def test_add_hook_and_retrieve(self):
        # EP: додавання валідного Hook (позитивний)
        history = History()
        hook = Hook(1, "Тема", "neutral")
        history.add_hook(hook)
        self.assertEqual(len(history), 1)
        self.assertIs(history.list_of_hooks[0], hook)

    def test_clear_history(self):
        # EP: очищення (позитивний)
        history = History()
        history.add_hook(Hook(1, "A", "neutral"))
        history.add_hook(Hook(2, "B", "humorous"))
        history.clear_history()
        self.assertEqual(len(history), 0)

    def test_add_non_hook_raises(self):
        # EP: не-Hook об'єкт → ValidationError (негативний)
        history = History()
        with self.assertRaises(ValidationError):
            history.add_hook("not a hook")


# ===========================================================================
# Guest.use_trial
# ===========================================================================

class TestGuestUseTrial(unittest.TestCase):

    def test_use_trial_decrements(self):
        # BVA: від 3 до 2 (позитивний)
        guest = Guest()
        remaining = guest.use_trial()
        self.assertEqual(remaining, 2)

    def test_use_trial_exactly_limit(self):
        # BVA: три виклики підряд — останній успішний (позитивний)
        guest = Guest()
        guest.use_trial()
        guest.use_trial()
        remaining = guest.use_trial()
        self.assertEqual(remaining, 0)

    def test_use_trial_exceeds_limit(self):
        # BVA: четвертий виклик → LimitExceededError (негативний)
        guest = Guest()
        for _ in range(3):
            guest.use_trial()
        with self.assertRaises(LimitExceededError):
            guest.use_trial()

    def test_use_trial_zero_remaining(self):
        # BVA: remaining вже 0 без попередніх викликів (граничне, негативний)
        guest = Guest()
        guest.remaining_generations = 0
        with self.assertRaises(LimitExceededError):
            guest.use_trial()


# ===========================================================================
# User.authenticate
# ===========================================================================

class TestUserAuthenticate(unittest.TestCase):

    def _make_user(self, email="user@example.com", password="secret123"):
        u = RegisteredUser(email=email)
        u.set_password(password)
        return u

    def test_correct_credentials(self):
        # EP: правильні дані (позитивний)
        user = self._make_user()
        self.assertTrue(user.authenticate("user@example.com", "secret123"))

    def test_wrong_password(self):
        # EP: неправильний пароль (негативний)
        user = self._make_user()
        self.assertFalse(user.authenticate("user@example.com", "wrongpass"))

    def test_wrong_email_returns_false(self):
        # EP: email не збігається (негативний)
        user = self._make_user()
        self.assertFalse(user.authenticate("other@example.com", "secret123"))

    def test_invalid_email_format_raises(self):
        # EP: email без @ → ValidationError (негативний)
        user = self._make_user()
        with self.assertRaises(ValidationError):
            user.authenticate("not-an-email", "secret123")

    def test_short_password_raises(self):
        # BVA: пароль 5 символів → ValidationError (негативний)
        user = self._make_user()
        with self.assertRaises(ValidationError):
            user.authenticate("user@example.com", "12345")

    def test_password_exactly_6_chars(self):
        # BVA: пароль рівно 6 символів — граничне значення (позитивний)
        user = self._make_user(password="sixchr")
        self.assertTrue(user.authenticate("user@example.com", "sixchr"))


# ===========================================================================
# GenerationRequest.submit
# ===========================================================================

class TestGenerationRequestSubmit(unittest.TestCase):

    def test_submit_returns_3_hooks(self):
        # EP: валідна тема і стиль → 3 гачки (позитивний)
        req = GenerationRequest("Python", "intriguing", user_id=1)
        hooks = req.submit()
        self.assertEqual(len(hooks), 3)

    def test_submit_hooks_have_correct_style(self):
        # EP: стиль гачків відповідає запиту (позитивний)
        req = GenerationRequest("Python", "humorous", user_id=1)
        hooks = req.submit()
        self.assertTrue(all(h.style == "humorous" for h in hooks))

    def test_submit_empty_topic_raises(self):
        # EP: порожня тема → ValidationError (негативний)
        req = GenerationRequest("", "neutral", user_id=1)
        with self.assertRaises(ValidationError):
            req.submit()

    def test_submit_topic_too_long_raises(self):
        # BVA: тема 201 символ → ValidationError (негативний)
        long_topic = "а" * 201
        req = GenerationRequest(long_topic, "neutral", user_id=1)
        with self.assertRaises(ValidationError):
            req.submit()

    def test_submit_topic_exactly_200_chars(self):
        # BVA: тема рівно 200 символів — граничне значення (позитивний)
        topic = "а" * 200
        req = GenerationRequest(topic, "neutral", user_id=1)
        hooks = req.submit()
        self.assertEqual(len(hooks), 3)

    def test_submit_invalid_style_raises(self):
        # EP: неіснуючий стиль → ValidationError (негативний)
        req = GenerationRequest("Тема", "formal", user_id=1)
        with self.assertRaises(ValidationError):
            req.submit()

    def test_get_result_before_submit_is_empty(self):
        # EP: get_result до submit → порожній список (позитивний)
        req = GenerationRequest("Тема", "neutral", user_id=1)
        self.assertEqual(req.get_result(), [])

    def test_get_result_after_submit(self):
        # EP: get_result після submit (позитивний)
        req = GenerationRequest("Тема", "neutral", user_id=1)
        req.submit()
        self.assertEqual(len(req.get_result()), 3)


# ===========================================================================
# AuthService
# ===========================================================================

class TestAuthService(unittest.TestCase):

    def test_register_and_login(self):
        # EP: повний happy-path (позитивний)
        svc = AuthService()
        svc.register("alice@test.com", "password1")
        user = svc.login("alice@test.com", "password1")
        self.assertEqual(user.email, "alice@test.com")

    def test_register_duplicate_email_raises(self):
        # EP: повторна реєстрація → AuthError (негативний)
        svc = AuthService()
        svc.register("bob@test.com", "password1")
        with self.assertRaises(AuthError):
            svc.register("bob@test.com", "otherpass")

    def test_register_invalid_email_raises(self):
        # EP: некоректний email → ValidationError (негативний)
        svc = AuthService()
        with self.assertRaises(ValidationError):
            svc.register("bad-email", "password1")

    def test_register_short_password_raises(self):
        # BVA: пароль 5 символів → ValidationError (негативний)
        svc = AuthService()
        with self.assertRaises(ValidationError):
            svc.register("c@test.com", "12345")

    def test_login_wrong_password_raises(self):
        # EP: неправильний пароль → AuthError (негативний)
        svc = AuthService()
        svc.register("d@test.com", "correctpass")
        with self.assertRaises(AuthError):
            svc.login("d@test.com", "wrongpass")

    def test_login_unknown_user_raises(self):
        # EP: незареєстрований email → AuthError (негативний)
        svc = AuthService()
        with self.assertRaises(AuthError):
            svc.login("nobody@test.com", "somepass")


# ===========================================================================
# Admin
# ===========================================================================

class TestAdmin(unittest.TestCase):

    def setUp(self):
        Guest.DEFAULT_LIMIT = 3  # reset before each test

    def tearDown(self):
        Guest.DEFAULT_LIMIT = 3  # restore after each test

    def test_manage_users_stats(self):
        # EP: підрахунок ролей (позитивний)
        admin = Admin("admin@hookcraft.com")
        users = [Guest(), Guest(), RegisteredUser("x@x.com")]
        stats = admin.manage_users(users)
        self.assertEqual(stats["guest"], 2)
        self.assertEqual(stats["registered"], 1)

    def test_update_limits_valid(self):
        # EP: новий ліміт 5 (позитивний)
        admin = Admin("admin@hookcraft.com")
        admin.update_limits(5)
        self.assertEqual(Guest.DEFAULT_LIMIT, 5)

    def test_update_limits_zero(self):
        # BVA: ліміт = 0 — граничне значення (позитивний)
        admin = Admin("admin@hookcraft.com")
        admin.update_limits(0)
        self.assertEqual(Guest.DEFAULT_LIMIT, 0)

    def test_update_limits_negative_raises(self):
        # BVA: ліміт < 0 → ValidationError (негативний)
        admin = Admin("admin@hookcraft.com")
        with self.assertRaises(ValidationError):
            admin.update_limits(-1)


# ===========================================================================
# RegisteredUser
# ===========================================================================

class TestRegisteredUser(unittest.TestCase):

    def test_save_to_favorites(self):
        # EP: збереження гачка в обрані (позитивний)
        user = RegisteredUser("u@test.com")
        hook = Hook(1, "Текст", "neutral")
        user.save_to_favorites(hook)
        self.assertIn(hook, user.favorite_hooks)
        self.assertTrue(hook.is_favorite)

    def test_view_history_reflects_added_hooks(self):
        # EP: перегляд історії (позитивний)
        user = RegisteredUser("u@test.com")
        hook = Hook(1, "Текст", "neutral")
        user.history.add_hook(hook)
        self.assertIn(hook, user.view_history())

    def test_get_history_base_returns_empty(self):
        # EP: базовий User.get_history() → [] (позитивний)
        u = User.__new__(User)
        u.id = 0
        u.email = "x@x.com"
        u.role = "base"
        result = u.get_history()
        self.assertEqual(result, [])


# ===========================================================================
# Extra coverage tests
# ===========================================================================

class TestExtraCoverage(unittest.TestCase):

    def test_authenticate_no_password_set_returns_false(self):
        # EP: authenticate коли пароль ніколи не встановлювався (негативний)
        # Arrange
        user = RegisteredUser("nopass@test.com")
        # Act
        result = user.authenticate("nopass@test.com", "anypass1")
        # Assert
        self.assertFalse(result)

    def test_set_password_short_raises(self):
        # BVA: set_password з паролем < 6 символів → ValidationError (негативний)
        user = RegisteredUser("u@test.com")
        with self.assertRaises(ValidationError):
            user.set_password("12345")

    def test_hook_get_text(self):
        # EP: get_text повертає текст (позитивний)
        hook = Hook(1, "Якийсь текст", "neutral")
        self.assertEqual(hook.get_text(), "Якийсь текст")

    def test_save_to_favorites_non_hook_raises(self):
        # EP: не-Hook у favorites → ValidationError (негативний)
        user = RegisteredUser("u@test.com")
        with self.assertRaises(ValidationError):
            user.save_to_favorites("just a string")  # type: ignore

    def test_auth_service_logout_no_error(self):
        # EP: logout виконується без помилок (позитивний)
        svc = AuthService()
        user = svc.register("logout@test.com", "password1")
        svc.logout(user)  # should not raise

    def test_registered_user_get_history(self):
        # EP: get_history у RegisteredUser делегує до view_history (позитивний)
        user = RegisteredUser("u@test.com")
        hook = Hook(1, "Текст", "neutral")
        user.history.add_hook(hook)
        self.assertEqual(user.get_history(), [hook])

    def test_save_to_favorites_duplicate_not_added(self):
        # EP: той самий Hook не додається двічі (позитивний)
        user = RegisteredUser("u@test.com")
        hook = Hook(1, "Текст", "neutral")
        user.save_to_favorites(hook)
        user.save_to_favorites(hook)
        self.assertEqual(len(user.favorite_hooks), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
