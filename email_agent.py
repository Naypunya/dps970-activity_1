
from pathlib import Path
from email.parser import BytesParser
from email import policy
from email.utils import parseaddr
import re
import shutil


class EmailFilterAgent:
    """Simple reflex agent for classifying email files."""

    def __init__(
        self,
        allow_file,
        blocked_file,
        words_file,
        spam_folder="spam",
        email_folder="email",
    ):
        self.allow_domains = self.load_list(allow_file)
        self.blocked_domains = self.load_list(blocked_file)
        self.spam_words = self.load_list(words_file)

        self.spam_folder = Path(spam_folder)
        self.email_folder = Path(email_folder)

        self.spam_folder.mkdir(parents=True, exist_ok=True)
        self.email_folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_list(filename):
        with open(filename, encoding="utf-8") as file:
            return {
                line.strip().lower().lstrip("@")
                for line in file
                if line.strip() and not line.lstrip().startswith("#")
            }

    @staticmethod
    def read_email(filename):
        with open(filename, "rb") as file:
            message = BytesParser(policy=policy.default).parse(file)

        sender = parseaddr(message.get("From", ""))[1]
        domain = sender.rsplit("@", 1)[-1].lower() if "@" in sender else ""

        body_parts = []
        parts = message.walk() if message.is_multipart() else [message]

        for part in parts:
            if part.get_content_maintype() != "text":
                continue

            try:
                content = part.get_content()
            except (LookupError, UnicodeError, ValueError):
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset() or "utf-8"
                content = payload.decode(charset, errors="replace")

            if isinstance(content, str):
                body_parts.append(content)

        return domain, "\n".join(body_parts)

    def classify_email(self, filename):
        domain, body = self.read_email(filename)

        # Rule 1: Trusted domains always pass.
        if domain in self.allow_domains:
            return "email"

        # Rule 2: Blocked domains are always spam.
        if domain in self.blocked_domains:
            return "spam"

        # Rule 3: More than five bad-word occurrences means spam.
        words = re.findall(r"\b[\w']+\b", body.lower())
        count = sum(word in self.spam_words for word in words)

        return "spam" if count > 5 else "email"

    def process_email(self, filename):
        source = Path(filename)
        classification = self.classify_email(source)

        destination_folder = (
            self.spam_folder
            if classification == "spam"
            else self.email_folder
        )
        destination = destination_folder / source.name

        if source.resolve() == destination.resolve():
            return classification, destination

        if destination.exists():
            raise FileExistsError(f"File already exists: {destination}")

        shutil.move(str(source), str(destination))
        return classification, destination


def main():
    root = Path(__file__).resolve().parent
    data = root / "test_data"

    agent = EmailFilterAgent(
        data / "allow_domains.txt",
        data / "blocked_domains.txt",
        data / "spam_words.txt",
        root / "spam",
        root / "email",
    )

    for filename in sorted(data.glob("*.eml")):
        classification, destination = agent.process_email(filename)
        print(f"{destination.name}: {classification} -> {destination}")


if __name__ == "__main__":
    main()
