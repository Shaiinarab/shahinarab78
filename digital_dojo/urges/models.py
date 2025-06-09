import uuid
import datetime

class UrgeLogEntry:
    def __init__(self, urge_type: str, initial_intensity: int, entry_id: str | None = None, start_time: str | None = None):
        self.entry_id = entry_id if entry_id else uuid.uuid4().hex
        self.urge_type = urge_type
        # Ensure start_time is in ISO format with 'T'
        if start_time:
            # Attempt to parse to validate and reformat if necessary
            dt_obj = datetime.datetime.fromisoformat(start_time.replace(" ", "T"))
            self.start_time = dt_obj.isoformat()
        else:
            self.start_time = datetime.datetime.now().isoformat()

        self.end_time: str | None = None
        self.initial_intensity = initial_intensity
        self.sensations_log: list[dict] = []

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "urge_type": self.urge_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "initial_intensity": self.initial_intensity,
            "sensations_log": self.sensations_log,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'UrgeLogEntry':
        entry = cls(
            urge_type=data["urge_type"],
            initial_intensity=data["initial_intensity"],
            entry_id=data.get("entry_id"), # Handle older data that might autogenerate
            start_time=data.get("start_time") # Handle older data
        )
        entry.end_time = data.get("end_time")
        entry.sensations_log = data.get("sensations_log", [])
        # Ensure start_time from loaded data is also correctly formatted if it exists
        if entry.start_time:
            try:
                dt_obj = datetime.datetime.fromisoformat(entry.start_time.replace(" ", "T"))
                entry.start_time = dt_obj.isoformat()
            except ValueError:
                # Handle cases where parsing might fail for old/bad data
                # Or decide on a stricter policy (e.g., raise error)
                print(f"Warning: Could not parse start_time '{entry.start_time}' for entry_id '{entry.entry_id}'. Leaving as is.")

        # Ensure timestamps in sensations_log are also correctly formatted
        for sensation in entry.sensations_log:
            if "timestamp" in sensation:
                try:
                    s_dt_obj = datetime.datetime.fromisoformat(sensation["timestamp"].replace(" ", "T"))
                    sensation["timestamp"] = s_dt_obj.isoformat()
                except ValueError:
                    print(f"Warning: Could not parse sensation timestamp '{sensation['timestamp']}' for entry_id '{entry.entry_id}'. Leaving as is.")
        return entry

    def end_session(self):
        """Sets the end_time to the current time."""
        self.end_time = datetime.datetime.now().isoformat()

    def add_sensation(self, note: str):
        """Adds a new sensation note with the current timestamp."""
        self.sensations_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "note": note
        })

    @property
    def duration_seconds(self) -> int | None:
        """Calculates the duration of the urge session in seconds if end_time is set."""
        if self.start_time and self.end_time:
            # Ensure correct parsing, especially if loaded from JSON
            start_dt = datetime.datetime.fromisoformat(self.start_time)
            end_dt = datetime.datetime.fromisoformat(self.end_time)
            return int((end_dt - start_dt).total_seconds())
        return None
