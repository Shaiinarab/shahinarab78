import json
from digital_dojo.habits.models import Habit
from digital_dojo.journal.entries import JournalEntry
from digital_dojo.urges.models import UrgeLogEntry # Added import

HABITS_FILE = "digital_dojo/data/habits.json"
JOURNAL_ENTRIES_FILE = "digital_dojo/data/journal_entries.json"
URGE_LOGS_FILE = "digital_dojo/data/urge_logs.json" # Added file constant

def save_habits(habits: list[Habit]):
    """Saves a list of Habit objects to the JSON file."""
    habits_data = [habit.to_dict() for habit in habits]
    try:
        with open(HABITS_FILE, "w") as f:
            json.dump(habits_data, f, indent=4)
    except IOError as e:
        print(f"Error saving habits: {e}")
        # Potentially re-raise or handle more gracefully depending on application needs

def load_habits() -> list[Habit]:
    """Loads habits from the JSON file.
    Returns a list of Habit objects. If the file doesn't exist or is empty,
    or contains invalid JSON, returns an empty list.
    """
    habits_list = []
    try:
        with open(HABITS_FILE, "r") as f:
            habits_data = json.load(f)
            if not isinstance(habits_data, list):
                print(f"Warning: {HABITS_FILE} does not contain a list. Returning empty list.")
                return []
            for habit_dict in habits_data:
                if isinstance(habit_dict, dict):
                    try:
                        habits_list.append(Habit.from_dict(habit_dict))
                    except KeyError as e:
                        print(f"Warning: Skipping habit due to missing key: {e} in dict {habit_dict}")
                    except Exception as e:
                        print(f"Warning: Error creating Habit from dict {habit_dict}: {e}")
                else:
                    print(f"Warning: Skipping non-dictionary item in habits file: {habit_dict}")
    except FileNotFoundError:
        # This is an expected case, so just return an empty list.
        pass
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {HABITS_FILE}. Returning empty list.")
        # If the file exists but is invalid, good to return empty and maybe log.
        # For a new setup, an empty or non-existent file is normal.
        return [] # Explicitly return empty list on JSON error
    except IOError as e:
        print(f"Error loading habits: {e}. Returning empty list.")
        return []
    return habits_list

# --- Journal Entry Storage Functions ---

def save_journal_entries(entries: list[JournalEntry]):
    """Saves a list of JournalEntry objects to the JSON file."""
    entries_data = [entry.to_dict() for entry in entries]
    try:
        with open(JOURNAL_ENTRIES_FILE, "w") as f:
            json.dump(entries_data, f, indent=4)
    except IOError as e:
        print(f"Error saving journal entries: {e}")

def load_journal_entries() -> list[JournalEntry]:
    """Loads journal entries from the JSON file.
    Returns a list of JournalEntry objects. If the file doesn't exist or is empty,
    or contains invalid JSON, returns an empty list.
    """
    entries_list = []
    try:
        with open(JOURNAL_ENTRIES_FILE, "r") as f:
            entries_data = json.load(f)
            if not isinstance(entries_data, list):
                print(f"Warning: {JOURNAL_ENTRIES_FILE} does not contain a list. Returning empty list.")
                return []
            for entry_dict in entries_data:
                if isinstance(entry_dict, dict):
                    try:
                        entries_list.append(JournalEntry.from_dict(entry_dict))
                    except KeyError as e:
                        print(f"Warning: Skipping journal entry due to missing key: {e} in dict {entry_dict}")
                    except Exception as e:
                        print(f"Warning: Error creating JournalEntry from dict {entry_dict}: {e}")
                else:
                    print(f"Warning: Skipping non-dictionary item in journal entries file: {entry_dict}")
    except FileNotFoundError:
        pass  # Expected case, return empty list
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {JOURNAL_ENTRIES_FILE}. Returning empty list.")
        return []
    except IOError as e:
        print(f"Error loading journal entries: {e}. Returning empty list.")
        return []
    return entries_list

# --- Urge Log Entry Storage Functions ---

def save_urge_logs(logs: list[UrgeLogEntry]):
    """Saves a list of UrgeLogEntry objects to the JSON file."""
    logs_data = [log.to_dict() for log in logs]
    try:
        with open(URGE_LOGS_FILE, "w") as f:
            json.dump(logs_data, f, indent=4)
    except IOError as e:
        print(f"Error saving urge logs: {e}")

def load_urge_logs() -> list[UrgeLogEntry]:
    """Loads urge logs from the JSON file.
    Returns a list of UrgeLogEntry objects. If the file doesn't exist or is empty,
    or contains invalid JSON, returns an empty list.
    """
    logs_list = []
    try:
        with open(URGE_LOGS_FILE, "r") as f:
            logs_data = json.load(f)
            if not isinstance(logs_data, list):
                print(f"Warning: {URGE_LOGS_FILE} does not contain a list. Returning empty list.")
                return []
            for log_dict in logs_data:
                if isinstance(log_dict, dict):
                    try:
                        logs_list.append(UrgeLogEntry.from_dict(log_dict))
                    except KeyError as e:
                        print(f"Warning: Skipping urge log due to missing key: {e} in dict {log_dict}")
                    except Exception as e:
                        print(f"Warning: Error creating UrgeLogEntry from dict {log_dict}: {e}")
                else:
                    print(f"Warning: Skipping non-dictionary item in urge logs file: {log_dict}")
    except FileNotFoundError:
        pass  # Expected case, return empty list
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {URGE_LOGS_FILE}. Returning empty list.")
        return []
    except IOError as e:
        print(f"Error loading urge logs: {e}. Returning empty list.")
        return []
    return logs_list
