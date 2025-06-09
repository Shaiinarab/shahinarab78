import uuid
import datetime
from digital_dojo.data.storage import load_journal_entries, save_journal_entries
from digital_dojo.journal.prompts import get_prompt_by_id


class JournalEntry:
    def __init__(self, user_text: str, prompt_id: str | None = None, prompt_text_snapshot: str | None = None, entry_id: str | None = None, date_iso: str | None = None):
        self.entry_id = entry_id if entry_id else str(uuid.uuid4())
        self.date_iso = date_iso if date_iso else datetime.date.today().isoformat()
        self.prompt_id = prompt_id
        self.prompt_text_snapshot = prompt_text_snapshot
        self.user_text = user_text

    def to_dict(self) -> dict:
        """Converts JournalEntry data to a dictionary for JSON serialization."""
        return {
            "entry_id": self.entry_id,
            "date_iso": self.date_iso,
            "prompt_id": self.prompt_id,
            "prompt_text_snapshot": self.prompt_text_snapshot,
            "user_text": self.user_text,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'JournalEntry':
        """Creates a JournalEntry object from a dictionary."""
        return cls(
            entry_id=data.get("entry_id"), # Allow for older data that might not have it, so uuid generates
            date_iso=data.get("date_iso"),   # Allow for older data
            prompt_id=data.get("prompt_id"),
            prompt_text_snapshot=data.get("prompt_text_snapshot"),
            user_text=data["user_text"] # user_text is essential
        )

# --- Journal Entry Management Functions ---

def add_journal_entry(user_text: str, prompt_id: str | None = None) -> JournalEntry:
    """
    Adds a new journal entry.
    Args:
        user_text: The text content of the journal entry.
        prompt_id: Optional ID of the philosophical prompt used.
    Returns:
        The newly created JournalEntry object.
    Raises:
        ValueError: If the provided prompt_id is not found.
    """
    entry_id = uuid.uuid4().hex # Using hex for a shorter string if preferred
    date_iso = datetime.date.today().isoformat()
    prompt_text_snapshot = "" # Default to empty string

    if prompt_id:
        prompt = get_prompt_by_id(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt with ID {prompt_id} not found.")
        prompt_text_snapshot = prompt.get("text", "") # Get text, default to empty if key missing

    new_entry = JournalEntry(
        entry_id=entry_id,
        date_iso=date_iso,
        prompt_id=prompt_id,
        prompt_text_snapshot=prompt_text_snapshot,
        user_text=user_text
    )

    entries = load_journal_entries()
    entries.append(new_entry)
    save_journal_entries(entries)
    return new_entry

def get_journal_entry_by_id(entry_id: str) -> JournalEntry | None:
    """
    Retrieves a specific journal entry by its ID.
    Args:
        entry_id: The ID of the journal entry.
    Returns:
        The JournalEntry object if found, otherwise None.
    """
    entries = load_journal_entries()
    for entry in entries:
        if entry.entry_id == entry_id:
            return entry
    return None

def get_journal_entries_by_date(date_str: str) -> list[JournalEntry]:
    """
    Retrieves all journal entries for a specific date.
    Args:
        date_str: The date string in "YYYY-MM-DD" format.
    Returns:
        A list of JournalEntry objects for that date.
    Raises:
        ValueError: If the date_str format is invalid.
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    entries = load_journal_entries()
    return [entry for entry in entries if entry.date_iso == date_str]

def get_all_journal_entries() -> list[JournalEntry]:
    """
    Retrieves all journal entries.
    Returns:
        A list of all JournalEntry objects.
    """
    return load_journal_entries()
