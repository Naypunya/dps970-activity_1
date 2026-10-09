
import tempfile
import unittest
from pathlib import Path

from email_agent import EmailFilterAgent


class TestEmailFilterAgent(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        self.agent = EmailFilterAgent(
    self.make_list("allow.txt", "trusted.com"),
    self.make_list("blocked.txt", "blocked.com"),
    self.make_list("words.txt", "winner\nprize\nfree\ncash\nurgent\nclaim"),
    self.root / "spam",
    self.root / "email",
)

    def make_list(self, filename, contents):
        path = self.root / filename
        path.write_text(contents, encoding="utf-8")
        return path

    def make_email(self, sender, body):
        path = self.root / "sample.eml"
        path.write_text(
            f"From: {sender}\n"
            "To: user@example.net\n"
            "Subject: Test\n\n"
            f"{body}\n",
            encoding="utf-8",
        )
        return path

    def tearDown(self):
        self.temp.cleanup()

    def test_trusted_domain_overrides_bad_words(self):
        path = self.make_email(
            "person@trusted.com",
            "winner prize free cash urgent claim winner",
        )
        self.assertEqual(self.agent.classify_email(path), "email")

    def test_blocked_domain_is_spam(self):
        path = self.make_email(
            "person@blocked.com",
            "Hello there",
        )
        self.assertEqual(self.agent.classify_email(path), "spam")

    def test_six_bad_word_occurrences_are_spam(self):
        path = self.make_email(
            "person@unknown.com",
            "winner prize free cash urgent claim",
        )
        self.assertEqual(self.agent.classify_email(path), "spam")

    def test_five_bad_word_occurrences_are_not_spam(self):
        path = self.make_email(
            "person@unknown.com",
            "winner prize free cash urgent",
        )
        self.assertEqual(self.agent.classify_email(path), "email")

    def test_moving_spam_email(self):
        path = self.make_email(
            "person@blocked.com",
            "Hello",
        )
        result, destination = self.agent.process_email(path)

        self.assertEqual(result, "spam")
        self.assertTrue(destination.exists())
        self.assertEqual(destination.parent, self.root / "spam")


if __name__ == "__main__":
    unittest.main()
