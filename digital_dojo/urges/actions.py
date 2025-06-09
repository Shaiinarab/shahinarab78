from .models import UrgeLogEntry
from digital_dojo.data.storage import load_urge_logs, save_urge_logs
import datetime

def start_new_urge_log(urge_type: str, initial_intensity: int) -> UrgeLogEntry:
    """
    Starts a new urge log session.
    Args:
        urge_type: The type of urge (e.g., "smoking", "snacking").
        initial_intensity: User-reported intensity (1-10).
    Returns:
        The newly created UrgeLogEntry.
    Raises:
        ValueError: If initial_intensity is not between 1 and 10.
    """
    if not (1 <= initial_intensity <= 10):
        raise ValueError("Initial intensity must be between 1 and 10.")

    # start_time will be set by the UrgeLogEntry constructor
    new_log = UrgeLogEntry(urge_type=urge_type, initial_intensity=initial_intensity)

    logs = load_urge_logs()
    logs.append(new_log)
    save_urge_logs(logs)
    return new_log

def add_sensation_to_log(entry_id: str, sensation_note: str) -> UrgeLogEntry:
    """
    Adds a sensation note to an active urge log.
    Args:
        entry_id: The ID of the urge log.
        sensation_note: The textual note describing the sensation.
    Returns:
        The updated UrgeLogEntry.
    Raises:
        ValueError: If log not found or already ended.
    """
    logs = load_urge_logs()
    log_to_update = None
    for i, log in enumerate(logs):
        if log.entry_id == entry_id:
            log_to_update = log
            break

    if log_to_update is None:
        raise ValueError(f"Urge log with ID {entry_id} not found.")
    if log_to_update.end_time is not None:
        raise ValueError(f"Urge log with ID {entry_id} has already ended.")

    log_to_update.add_sensation(sensation_note)
    save_urge_logs(logs)
    return log_to_update

def end_urge_log(entry_id: str) -> UrgeLogEntry:
    """
    Ends an active urge log session.
    Args:
        entry_id: The ID of the urge log to end.
    Returns:
        The updated UrgeLogEntry with end_time set.
    Raises:
        ValueError: If log not found or already ended.
    """
    logs = load_urge_logs()
    log_to_update = None
    for i, log in enumerate(logs):
        if log.entry_id == entry_id:
            log_to_update = log
            break

    if log_to_update is None:
        raise ValueError(f"Urge log with ID {entry_id} not found.")
    if log_to_update.end_time is not None:
        raise ValueError(f"Urge log with ID {entry_id} has already ended.")

    log_to_update.end_session()
    save_urge_logs(logs)
    return log_to_update

def get_urge_log_details(entry_id: str) -> UrgeLogEntry | None:
    """
    Retrieves details of a specific urge log.
    Args:
        entry_id: The ID of the urge log.
    Returns:
        The UrgeLogEntry if found, otherwise None.
    """
    logs = load_urge_logs()
    for log in logs:
        if log.entry_id == entry_id:
            return log
    return None

def get_all_urge_logs() -> list[UrgeLogEntry]:
    """
    Retrieves all urge logs.
    Returns:
        A list of all UrgeLogEntry objects.
    """
    return load_urge_logs()

def get_active_urge_logs() -> list[UrgeLogEntry]:
    """
    Retrieves all active (not yet ended) urge logs.
    Returns:
        A list of UrgeLogEntry objects where end_time is None.
    """
    logs = load_urge_logs()
    return [log for log in logs if log.end_time is None]
