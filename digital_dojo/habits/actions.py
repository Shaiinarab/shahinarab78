import datetime
from .models import Habit
from digital_dojo.data.storage import load_habits, save_habits

def add_new_habit(habit_name: str) -> Habit:
    """
    Adds a new habit.
    Args:
        habit_name: The name of the habit.
    Returns:
        The newly created Habit object.
    Raises:
        ValueError: If a habit with the same name already exists.
    """
    habits = load_habits()
    for habit in habits:
        if habit.name == habit_name:
            raise ValueError(f"Habit with name '{habit_name}' already exists.")

    start_date = datetime.date.today().isoformat()
    new_habit = Habit(name=habit_name, start_date=start_date)
    habits.append(new_habit)
    save_habits(habits)
    return new_habit

def record_habit_status(habit_name: str, status: str, date_str: str) -> Habit:
    """
    Records the status of a habit for a given date.
    Args:
        habit_name: The name of the habit.
        status: The status ("pass" or "fail").
        date_str: The date string in "YYYY-MM-DD" format.
    Returns:
        The updated Habit object.
    Raises:
        ValueError: If the habit is not found, status is invalid, or date format is invalid.
    """
    if status not in ["pass", "fail"]:
        raise ValueError("Status must be 'pass' or 'fail'.")

    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    habits = load_habits()
    habit_to_update = None
    for habit in habits:
        if habit.name == habit_name:
            habit_to_update = habit
            break

    if habit_to_update is None:
        raise ValueError(f"Habit with name '{habit_name}' not found.")

    habit_to_update.add_status(date_str, status)
    save_habits(habits)
    return habit_to_update

def get_habit_details(habit_name: str) -> Habit | None:
    """
    Retrieves details of a specific habit.
    Args:
        habit_name: The name of the habit.
    Returns:
        The Habit object if found, otherwise None.
    """
    habits = load_habits()
    for habit in habits:
        if habit.name == habit_name:
            return habit
    return None

def get_all_habits() -> list[Habit]:
    """
    Retrieves all habits.
    Returns:
        A list of all Habit objects.
    """
    return load_habits()
