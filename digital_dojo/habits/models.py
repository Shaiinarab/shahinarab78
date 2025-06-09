import datetime

class Habit:
    def __init__(self, name: str, start_date: str):
        self.name = name
        self.start_date = start_date
        self.streaks = {}  # Key: "YYYY-MM-DD", Value: "pass" or "fail"

    def add_status(self, date: str, status: str):
        """Adds a daily status for the habit.
        Args:
            date: The date string in "YYYY-MM-DD" format.
            status: "pass" or "fail".
        """
        if status not in ["pass", "fail"]:
            raise ValueError("Status must be 'pass' or 'fail'")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        self.streaks[date] = status

    def get_current_streak(self) -> int:
        """Calculates the current streak of consecutive 'pass' days."""
        today = datetime.date.today()
        current_streak = 0
        dates = sorted(self.streaks.keys(), reverse=True)

        # Find the latest recorded date
        last_recorded_date_str = None
        if dates:
            last_recorded_date_str = dates[0]

        # If no entries or last entry is not "pass", streak is 0
        if not last_recorded_date_str or self.streaks[last_recorded_date_str] != "pass":
            return 0

        last_recorded_date = datetime.datetime.strptime(last_recorded_date_str, "%Y-%m-%d").date()

        # Check if the last recorded day is today or yesterday, otherwise streak is broken
        if last_recorded_date != today and last_recorded_date != (today - datetime.timedelta(days=1)):
             # If the last recorded day is not today or yesterday, and it was a "pass",
             # the streak was 1 for that day. But it's now broken.
             # However, the requirement is "consecutive 'pass' days leading up to the current day or the last recorded day"
             # This implies if the last recorded day was a pass, the streak refers to that point.
             # Let's refine this: The streak is broken if the last recorded day isn't today or yesterday,
             # UNLESS all recorded days form a continuous streak.
             pass # Further logic will handle this.


        # Iterate backwards from the most recent entry
        temp_date = last_recorded_date
        idx = 0
        while idx < len(dates):
            current_date_str = dates[idx]
            current_date = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()

            if self.streaks[current_date_str] == "pass":
                if idx == 0: # First entry in sorted (latest)
                    current_streak += 1
                else:
                    # Check if it's consecutive to the previous date in the list
                    prev_date_in_list = datetime.datetime.strptime(dates[idx-1], "%Y-%m-%d").date()
                    if current_date == prev_date_in_list - datetime.timedelta(days=1):
                        current_streak += 1
                    else:
                        # Not consecutive with the previous recorded pass, so this streak ends here.
                        # If this is the most recent streak, it's the one we report.
                        break
            else: # status is "fail"
                # If the most recent entry is a "fail", the streak is 0.
                # If we encounter a "fail" while iterating back, the streak ends.
                if idx == 0: # most recent entry
                    return 0
                break
            idx +=1
            temp_date -= datetime.timedelta(days=1)


        # If the streak extends to today or yesterday, it's current.
        # If the last recorded day with a "pass" is older than yesterday, the streak is broken (effectively 0 for "current").
        # However, the method asks for "current streak ... leading up to the current day OR THE LAST RECORDED DAY."
        # This means if the last entry was "2023-10-01": "pass", and before that "2023-09-30": "pass",
        # and today is "2023-10-25", the streak for "2023-10-01" was 2.
        # The wording is a bit ambiguous for "current streak" if the last recorded day is old.
        # Let's assume "current streak" means:
        # 1. If the last recorded day is today or yesterday, and it's a "pass", count consecutive days.
        # 2. If the last recorded day is older than yesterday, the "current" streak (as of today) is 0.
        #    However, the method could also be interpreted as "the most recent streak length found in the records".
        # Let's go with interpretation #2 for "current streak" for now.
        # The previously calculated current_streak is the streak ending on last_recorded_date.
        # Now, check if this streak is "current" with respect to today.

        if not dates: # No entries
            return 0

        if self.streaks[dates[0]] == "fail": # Last entry was a fail
            return 0

        # last_recorded_date is the date of dates[0]
        if last_recorded_date == today or last_recorded_date == (today - datetime.timedelta(days=1)):
            return current_streak
        else:
            # The streak is not current (i.e. not connected to today or yesterday)
            return 0


    def to_dict(self) -> dict:
        """Converts habit data to a dictionary."""
        return {
            "name": self.name,
            "start_date": self.start_date,
            "streaks": self.streaks.copy()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        """Creates a Habit object from a dictionary."""
        habit = cls(name=data["name"], start_date=data["start_date"])
        habit.streaks = data.get("streaks", {}).copy()
        return habit
