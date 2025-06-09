from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, DataTable, Label, TextArea, Markdown
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer, VerticalScroll
from textual.binding import Binding
from textual.reactive import reactive
import datetime
import pytz # For timezone aware datetime objects

from digital_dojo.habits import get_all_habits, add_new_habit, record_habit_status, Habit

from digital_dojo.journal.prompts import get_random_prompt
from digital_dojo.journal.entries import add_journal_entry, get_all_journal_entries, get_journal_entry_by_id, JournalEntry

# Urge Log imports
from digital_dojo.urges import (
    get_active_urge_logs,
    start_new_urge_log,
    add_sensation_to_log,
    end_urge_log,
    get_all_urge_logs, # Added import
    UrgeLogEntry
)


class BaseContentScreen(Screen):
    BINDINGS = [Binding("b", "go_back", "Back to Menu")]

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None, message: str = "Coming Soon") -> None:
        super().__init__(name, id, classes)
        self.message = message
        self._has_composed_header_footer = False

    def compose_default(self) -> ComposeResult:
        if not self._has_composed_header_footer:
            yield Header()
            yield Footer()
            self._has_composed_header_footer = True

    def compose(self) -> ComposeResult:
        yield from self.compose_default()
        yield Container(
            Static(self.message, id="message_static"),
            Button("Back to Main Menu (Press B)", id="back_button", variant="primary")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_button":
            self.app.pop_screen()

    def action_go_back(self) -> None:
        self.app.pop_screen()


class HabitsScreen(BaseContentScreen):
    TITLE = "Manage Habits"
    # ... (code for HabitsScreen remains the same) ...
    def __init__(self) -> None:
        super().__init__(message="Habit Management", id="habits_screen")
        self.selected_habit_name: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()

        yield Label("Enter new habit name:", classes="label_padding")
        yield Input(placeholder="e.g., Morning Meditation", id="new_habit_name")
        yield Horizontal(
            Button("Add Habit", id="add_habit_button", variant="success"),
            classes="button_container"
        )

        yield DataTable(id="habits_table", cursor_type="row")

        yield Horizontal(
            Button("Mark Selected Pass", id="mark_pass_button", variant="success"),
            Button("Mark Selected Fail", id="mark_fail_button", variant="error"),
            classes="button_container"
        )
        yield Label("", id="status_label")
        yield Footer()
        self._has_composed_header_footer = True

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Habit Name", "Current Streak")
        self._load_and_display_habits()

    def _load_and_display_habits(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        status_label = self.query_one("#status_label", Label)
        try:
            habits = get_all_habits()
            if not habits:
                table.add_row("No habits yet. Add one above!")
            for habit in habits:
                streak = habit.get_current_streak()
                table.add_row(habit.name, str(streak))
            status_label.update("Habits loaded.")
        except Exception as e:
            status_label.update(f"Error loading habits: {e}")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one(DataTable)
        status_label = self.query_one("#status_label", Label)
        try:
            selected_row_index = event.cursor_row
            if selected_row_index is None:
                 status_label.update("No row selected (index is None).")
                 return
            row_values = table.get_row_at(selected_row_index)
            if not row_values:
                status_label.update("Selected row data is empty.")
                return
            self.selected_habit_name = str(row_values[0])
            status_label.update(f"Selected: {self.selected_habit_name}")
        except IndexError:
            status_label.update("Could not retrieve habit name from selected row.")
            self.selected_habit_name = None
        except Exception as e:
            self.selected_habit_name = None
            status_label.update(f"Error selecting habit: {e}")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        status_label = self.query_one("#status_label", Label)
        new_habit_input = self.query_one("#new_habit_name", Input)

        if event.button.id == "add_habit_button":
            habit_name = new_habit_input.value
            if habit_name:
                try:
                    add_new_habit(habit_name)
                    new_habit_input.value = ""
                    self._load_and_display_habits()
                    status_label.update(f"Habit '{habit_name}' added.")
                except ValueError as e:
                    status_label.update(str(e))
                except Exception as e:
                    status_label.update(f"Error adding habit: {e}")
            else:
                status_label.update("Please enter a habit name.")

        elif event.button.id in ["mark_pass_button", "mark_fail_button"]:
            if not self.selected_habit_name:
                status_label.update("No habit selected from the table.")
                return
            status = "pass" if event.button.id == "mark_pass_button" else "fail"
            date_str = datetime.date.today().isoformat()
            try:
                record_habit_status(self.selected_habit_name, status, date_str)
                self._load_and_display_habits()
                status_label.update(f"Marked '{self.selected_habit_name}' as {status} for today.")
            except ValueError as e:
                status_label.update(str(e))
            except Exception as e:
                status_label.update(f"Error recording status: {e}")
        elif event.button.id == "back_button":
             self.app.pop_screen()

class JournalScreen(BaseContentScreen):
    TITLE = "Philosopher's Journal"
    current_prompt: reactive[dict | None] = reactive(None)
    # ... (code for JournalScreen remains the same) ...
    def __init__(self) -> None:
        super().__init__(message="Journaling Section", id="journal_screen")

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Static("Philosophical Prompt:", classes="label_padding"),
            Static(id="prompt_display", classes="prompt_box"),
            Label("Your Thoughts:", classes="label_padding"),
            TextArea(id="journal_text_area", language="markdown", theme="vscode_dark"),
            Horizontal(
                Button("Save Journal Entry", id="save_entry_button", variant="success"),
                Button("Get New Prompt", id="new_prompt_button", variant="primary"),
                classes="button_container"
            ),
            Horizontal(
                Button("View Past Entries", id="view_past_entries_button", variant="default"),
                classes="button_container"
            ),
            Label("", id="journal_status_label")
        )
        yield Footer()
        self._has_composed_header_footer = True

    def on_mount(self) -> None:
        self._load_random_prompt()
        self.query_one("#journal_text_area", TextArea).focus()

    def _format_prompt_text(self, prompt: dict | None) -> str:
        if not prompt:
            return "No prompt loaded. Press 'Get New Prompt' or try again."
        text = f"[b]Type:[/b] {prompt.get('type', 'N/A')}\n"
        if prompt.get('source'):
            text += f"[b]Source:[/b] {prompt.get('source', 'N/A')}\n\n"
        else:
            text += "\n"
        text += f"{prompt.get('text', 'Prompt text missing.')}"
        return text

    def _load_random_prompt(self) -> None:
        status_label = self.query_one("#journal_status_label", Label)
        prompt_display_widget = self.query_one("#prompt_display", Static)
        try:
            self.current_prompt = get_random_prompt()
            if self.current_prompt:
                formatted_text = self._format_prompt_text(self.current_prompt)
                prompt_display_widget.update(formatted_text)
                status_label.update("New prompt loaded.")
            else:
                prompt_display_widget.update("Could not load a new prompt. The list might be empty.")
                status_label.update("Failed to load new prompt.")
        except Exception as e:
            prompt_display_widget.update("Error loading prompt.")
            status_label.update(f"Error: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status_label = self.query_one("#journal_status_label", Label)
        journal_text_area = self.query_one("#journal_text_area", TextArea)

        if event.button.id == "save_entry_button":
            entry_text = journal_text_area.text
            if not entry_text.strip():
                status_label.update("Cannot save an empty journal entry.")
                return
            if not self.current_prompt:
                status_label.update("No prompt is currently loaded. Cannot save entry.")
                return
            try:
                add_journal_entry(user_text=entry_text, prompt_id=self.current_prompt["id"])
                journal_text_area.text = ""
                status_label.update("Journal entry saved successfully!")
            except ValueError as e:
                status_label.update(f"Error saving entry: {e}")
            except Exception as e:
                status_label.update(f"An unexpected error occurred: {e}")

        elif event.button.id == "new_prompt_button":
            self._load_random_prompt()
            journal_text_area.text = ""
            journal_text_area.focus()
        elif event.button.id == "view_past_entries_button":
            self.app.push_screen(ViewJournalEntriesScreen())
        elif event.button.id == "back_button":
             self.app.pop_screen()


class ViewJournalEntriesScreen(BaseContentScreen):
    TITLE = "Past Journal Entries"
    # ... (code for ViewJournalEntriesScreen remains the same) ...
    def __init__(self) -> None:
        super().__init__(message="Viewing Past Journal Entries", id="view_journal_entries_screen")
        self.all_entries: list[JournalEntry] = []
        self.selected_entry_id: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("All Past Journal Entries:", classes="label_padding")
        yield DataTable(id="past_entries_table", cursor_type="row")

        yield Label("Selected Entry Details:", classes="label_padding")
        yield ScrollableContainer(
            Static(id="full_prompt_text_header", content="[b]Prompt:[/b]"),
            Static(id="full_prompt_text", content="Select an entry to view its prompt."),
            Static(id="full_entry_text_header", content="[b]Entry:[/b]", classes="label_padding_top"),
            Static(id="full_entry_text", content="Select an entry to view its content."),
            id="full_entry_container"
        )
        yield Label("", id="view_entries_status_label")
        yield Footer()
        self._has_composed_header_footer = True

    def on_mount(self) -> None:
        table = self.query_one("#past_entries_table", DataTable)
        table.add_columns("ID", "Date", "Prompt Snippet", "Entry Snippet")
        self._load_past_entries()
        status_label = self.query_one("#view_entries_status_label", Label)
        status_label.update("Select an entry from the table above to see details.")

    def _load_past_entries(self) -> None:
        table = self.query_one("#past_entries_table", DataTable)
        status_label = self.query_one("#view_entries_status_label", Label)
        table.clear()
        try:
            self.all_entries = get_all_journal_entries()
            if not self.all_entries:
                table.add_row("No journal entries found.")
                status_label.update("No entries to display.")
                return
            for entry in self.all_entries:
                prompt_snippet = (entry.prompt_text_snapshot[:47] + "...") if entry.prompt_text_snapshot and len(entry.prompt_text_snapshot) > 50 else entry.prompt_text_snapshot or "N/A"
                entry_snippet = (entry.user_text[:47] + "...") if len(entry.user_text) > 50 else entry.user_text
                table.add_row(entry.entry_id, entry.date_iso, prompt_snippet, entry_snippet)
            status_label.update(f"Loaded {len(self.all_entries)} entries.")
        except Exception as e:
            status_label.update(f"Error loading entries: {e}")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one("#past_entries_table", DataTable)
        status_label = self.query_one("#view_entries_status_label", Label)
        full_prompt_widget = self.query_one("#full_prompt_text", Static)
        full_entry_widget = self.query_one("#full_entry_text", Static)
        try:
            selected_row_index = event.cursor_row
            if selected_row_index is None:
                 status_label.update("No row selected (index is None).")
                 return
            try:
                row_values = table.get_row_at(selected_row_index)
                if not row_values:
                    status_label.update("Selected row data is empty.")
                    return
                self.selected_entry_id = str(row_values[0])
            except IndexError:
                status_label.update("Could not retrieve entry ID from selected row.")
                return
            selected_full_entry = None
            for entry in self.all_entries:
                if entry.entry_id == self.selected_entry_id:
                    selected_full_entry = entry
                    break
            if selected_full_entry:
                prompt_display = selected_full_entry.prompt_text_snapshot or "No prompt associated with this entry."
                full_prompt_widget.update(prompt_display)
                full_entry_widget.update(selected_full_entry.user_text)
                status_label.update(f"Displaying entry ID: {selected_full_entry.entry_id}")
            else:
                full_prompt_widget.update("Could not find details for selected entry.")
                full_entry_widget.update("")
                status_label.update(f"Error: Entry with ID {self.selected_entry_id} not found in loaded list.")
        except Exception as e:
            full_prompt_widget.update("Error displaying entry.")
            full_entry_widget.update("")
            status_label.update(f"Error selecting entry: {e}")
        elif event.button.id == "back_button":
             self.app.pop_screen()


class UrgeLogScreen(BaseContentScreen):
    TITLE = "Urge Surfing Log"
    active_urge_log: reactive[UrgeLogEntry | None] = reactive(None)
    current_duration_s: reactive[int] = reactive(0)

    def __init__(self) -> None:
        super().__init__(message="Urge Log Management", id="urge_log_screen")
        self.timer_update_interval = None # For self.set_interval

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("", id="urge_status_label") # General status/error messages

        # --- View for when NO urge is active ---
        with Vertical(id="inactive_urge_view"):
            yield Static("Start a new urge surfing session:", classes="label_padding")
            yield Input(placeholder="Urge Type (e.g., smoking, sugar craving)", id="urge_type_input")
            yield Input(placeholder="Initial Intensity (1-10)", id="urge_intensity_input", type="integer")
            yield Horizontal(
                Button("Start Urge Log", id="start_urge_button", variant="success"),
                classes="button_container"
            )

        # --- View for when an urge IS active ---
        with Vertical(id="active_urge_view", classes="hidden_view"): # Start hidden
            yield Static("Current Urge Session:", classes="label_padding")
            yield Static(id="active_urge_details") # Shows type, start time, initial intensity
            yield Static(id="urge_timer_display") # Shows current duration

            yield Label("Log sensations as they arise:", classes="label_padding")
            yield Input(placeholder="e.g., tightness in chest, thoughts of giving in", id="sensation_input")
            yield Horizontal(
                Button("Add Sensation Note", id="add_sensation_button", variant="primary"),
                classes="button_container"
            )

            yield Label("Logged Sensations:", classes="label_padding")
            # Using VerticalScroll for sensations instead of ScrollableContainer for simpler text addition
            yield VerticalScroll(
                Static(id="sensation_log_display_content"), # Content will be added here
                id="sensation_log_display_container"
            )

            yield Horizontal(
                Button("End Urge Session", id="end_urge_button", variant="error"),
                classes="button_container"
            )

        yield Horizontal( # Button for viewing past logs, always visible
            Button("View Past Urge Logs", id="view_past_urges_button", variant="default"),
            classes="button_container"
        )
        yield Footer()
        self._has_composed_header_footer = True

    def on_mount(self) -> None:
        self._check_for_active_urge()
        # Start timer, but paused. _update_view_based_on_state will resume if needed.
        self.timer_update_interval = self.set_interval(1, self._update_timer_display, pause=True)

    def _check_for_active_urge(self) -> None:
        status_label = self.query_one("#urge_status_label", Label)
        try:
            active_logs = get_active_urge_logs()
            if active_logs:
                self.active_urge_log = active_logs[0] # Assume only one can be active
                status_label.update("Active urge session loaded.")
            else:
                self.active_urge_log = None
                status_label.update("No active urge session.")
        except Exception as e:
            self.active_urge_log = None
            status_label.update(f"Error checking for active urges: {e}")
            # self.app.log(f"Error in _check_for_active_urge: {e}")
        self._update_view_based_on_state() # Ensure view updates even if error

    def _update_view_based_on_state(self) -> None:
        inactive_view = self.query_one("#inactive_urge_view", Vertical)
        active_view = self.query_one("#active_urge_view", Vertical)
        details_display = self.query_one("#active_urge_details", Static)
        timer_display = self.query_one("#urge_timer_display", Static)

        if self.active_urge_log:
            inactive_view.display = False
            active_view.display = True

            start_dt = datetime.datetime.fromisoformat(self.active_urge_log.start_time)
            # Make it timezone aware if it's not, assuming local if no tzinfo
            if start_dt.tzinfo is None:
                 start_dt = start_dt.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)


            details_text = (
                f"[b]Type:[/b] {self.active_urge_log.urge_type}\n"
                f"[b]Started:[/b] {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"[b]Initial Intensity:[/b] {self.active_urge_log.initial_intensity}"
            )
            details_display.update(details_text)
            self._update_sensation_display()
            self._update_timer_display() # Initial timer update
            if self.timer_update_interval: self.timer_update_interval.resume()
        else:
            inactive_view.display = True
            active_view.display = False
            timer_display.update("Duration: --:--")
            if self.timer_update_interval: self.timer_update_interval.pause()
            self.current_duration_s = 0


    def _update_timer_display(self) -> None:
        timer_display = self.query_one("#urge_timer_display", Static)
        if self.active_urge_log and self.active_urge_log.start_time:
            try:
                # Ensure start_time is timezone-aware (UTC from ISO format)
                start_dt_utc = datetime.datetime.fromisoformat(self.active_urge_log.start_time)
                if start_dt_utc.tzinfo is None: # Should have tz from isoformat if stored correctly
                    start_dt_utc = start_dt_utc.replace(tzinfo=pytz.utc)

                # Get current time as timezone-aware (UTC)
                now_utc = datetime.datetime.now(pytz.utc)

                duration = now_utc - start_dt_utc
                self.current_duration_s = int(duration.total_seconds())

                minutes = self.current_duration_s // 60
                seconds = self.current_duration_s % 60
                timer_display.update(f"Duration: {minutes:02d}:{seconds:02d}")
            except Exception as e:
                timer_display.update("Duration: Error")
                # self.app.log(f"Error updating timer: {e}")
        else:
            timer_display.update("Duration: --:--")


    # This is the Textual reactive callback
    async def watch_active_urge_log(self, old_log: UrgeLogEntry | None, new_log: UrgeLogEntry | None) -> None:
        self._update_view_based_on_state()

    def _update_sensation_display(self) -> None:
        sensation_content = self.query_one("#sensation_log_display_content", Static)
        if self.active_urge_log and self.active_urge_log.sensations_log:
            log_text = ""
            for sensation in self.active_urge_log.sensations_log:
                try:
                    timestamp_dt = datetime.datetime.fromisoformat(sensation['timestamp'])
                    # Make it timezone aware if it's not, assuming local if no tzinfo
                    if timestamp_dt.tzinfo is None:
                        timestamp_dt = timestamp_dt.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)

                    time_str = timestamp_dt.strftime('%H:%M:%S')
                    log_text += f"-[{time_str}] {sensation['note']}\n"
                except Exception: # Fallback for bad timestamp
                    log_text += f"-[Invalid Time] {sensation['note']}\n"

            sensation_content.update(log_text if log_text else "No sensations logged yet.")
        else:
            sensation_content.update("No sensations logged yet.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status_label = self.query_one("#urge_status_label", Label)

        if event.button.id == "start_urge_button":
            type_input = self.query_one("#urge_type_input", Input)
            intensity_input = self.query_one("#urge_intensity_input", Input)
            urge_type = type_input.value
            intensity_str = intensity_input.value

            if not urge_type:
                status_label.update("Urge type cannot be empty.")
                return
            if not intensity_str:
                status_label.update("Initial intensity cannot be empty.")
                return

            try:
                intensity = int(intensity_str)
                if not (1 <= intensity <= 10):
                    raise ValueError("Intensity must be between 1 and 10.")
            except ValueError as e:
                status_label.update(str(e))
                return

            try:
                new_log = start_new_urge_log(urge_type, intensity)
                self.active_urge_log = new_log # This will trigger watch_active_urge_log
                type_input.value = ""
                intensity_input.value = ""
                status_label.update(f"Urge log started for '{urge_type}'.")
            except Exception as e:
                status_label.update(f"Error starting urge log: {e}")

        elif event.button.id == "add_sensation_button":
            sensation_input = self.query_one("#sensation_input", Input)
            note = sensation_input.value
            if not note:
                status_label.update("Sensation note cannot be empty.")
                return
            if self.active_urge_log:
                try:
                    updated_log = add_sensation_to_log(self.active_urge_log.entry_id, note)
                    self.active_urge_log = updated_log # Update reactive property
                    self._update_sensation_display() # Manually update display after adding
                    sensation_input.value = ""
                    status_label.update("Sensation added.")
                except Exception as e:
                    status_label.update(f"Error adding sensation: {e}")
            else:
                status_label.update("No active urge log to add sensation to.")

        elif event.button.id == "end_urge_button":
            if self.active_urge_log:
                try:
                    end_urge_log(self.active_urge_log.entry_id)
                    status_label.update(f"Urge session for '{self.active_urge_log.urge_type}' ended.")
                    self.active_urge_log = None # This will trigger watch_active_urge_log
                except Exception as e:
                    status_label.update(f"Error ending urge session: {e}")
            else:
                status_label.update("No active urge session to end.")

        elif event.button.id == "view_past_urges_button":
            # status_label.update("Viewing past urge logs - Coming soon!")
            self.app.push_screen(ViewUrgeLogsScreen())

        elif event.button.id == "back_button":
             self.app.pop_screen()


class ViewUrgeLogsScreen(BaseContentScreen):
    TITLE = "Past Urge Logs"

    def __init__(self) -> None:
        super().__init__(message="Viewing Past Urge Logs", id="view_urge_logs_screen")
        self.all_logs: list[UrgeLogEntry] = []
        self.selected_log_id: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("All Past Urge Logs:", classes="label_padding")
        yield DataTable(id="past_urge_logs_table", cursor_type="row")

        yield Label("Selected Urge Log Details:", classes="label_padding")
        yield ScrollableContainer(
            Static(id="full_urge_log_details"), # For basic info
            Markdown(id="full_urge_sensations_markdown"), # For sensation list
            id="full_urge_log_container"
        )
        yield Label("", id="view_urge_logs_status_label")
        yield Footer()
        self._has_composed_header_footer = True # We are handling header/footer

    def on_mount(self) -> None:
        table = self.query_one("#past_urge_logs_table", DataTable)
        table.add_columns("ID", "Type", "Start Time", "Duration (s)", "Intensity")
        self._load_past_urge_logs()

        status_label = self.query_one("#view_urge_logs_status_label", Label)
        details_static = self.query_one("#full_urge_log_details", Static)
        sensations_markdown = self.query_one("#full_urge_sensations_markdown", Markdown)

        status_label.update("Select a log from the table to view details.")
        details_static.update("Details will appear here.")
        sensations_markdown.update("*Sensations will appear here.*")


    def _load_past_urge_logs(self) -> None:
        table = self.query_one("#past_urge_logs_table", DataTable)
        status_label = self.query_one("#view_urge_logs_status_label", Label)
        table.clear()
        try:
            self.all_logs = get_all_urge_logs()
            if not self.all_logs:
                table.add_row("No urge logs found.")
                status_label.update("No urge logs to display.")
                return

            for log in self.all_logs:
                duration_str = str(log.duration_seconds) if log.duration_seconds is not None else "N/A (Active?)"

                start_dt_obj = datetime.datetime.fromisoformat(log.start_time)
                # Ensure timezone awareness for display, convert to local
                if start_dt_obj.tzinfo is None:
                    start_dt_obj = start_dt_obj.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)
                start_time_str = start_dt_obj.strftime('%Y-%m-%d %H:%M:%S')

                table.add_row(log.entry_id, log.urge_type, start_time_str, duration_str, str(log.initial_intensity))
            status_label.update(f"Loaded {len(self.all_logs)} urge logs.")
        except Exception as e:
            status_label.update(f"Error loading urge logs: {e}")
            # self.app.log(f"Error in _load_past_urge_logs: {e}")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one("#past_urge_logs_table", DataTable)
        status_label = self.query_one("#view_urge_logs_status_label", Label)
        details_static = self.query_one("#full_urge_log_details", Static)
        sensations_markdown = self.query_one("#full_urge_sensations_markdown", Markdown)

        try:
            selected_row_index = event.cursor_row
            if selected_row_index is None:
                status_label.update("No row selected.")
                return

            row_values = table.get_row_at(selected_row_index)
            if not row_values:
                status_label.update("Selected row data is empty.")
                return

            self.selected_log_id = str(row_values[0]) # Entry ID is the first column

            selected_full_log = None
            for log_entry in self.all_logs:
                if log_entry.entry_id == self.selected_log_id:
                    selected_full_log = log_entry
                    break

            if selected_full_log:
                # Format basic details
                start_dt = datetime.datetime.fromisoformat(selected_full_log.start_time)
                if start_dt.tzinfo is None: # Ensure timezone for display
                     start_dt = start_dt.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)
                start_time_str = start_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

                end_time_str = "Still Active"
                if selected_full_log.end_time:
                    end_dt = datetime.datetime.fromisoformat(selected_full_log.end_time)
                    if end_dt.tzinfo is None: # Ensure timezone for display
                        end_dt = end_dt.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)
                    end_time_str = end_dt.strftime('%Y-%m-%d %H:%M:%S %Z')

                duration_val = selected_full_log.duration_seconds
                duration_str_detail = f"{duration_val // 60}m {duration_val % 60}s" if duration_val is not None else "N/A"

                details_text = (
                    f"[b]ID:[/b] {selected_full_log.entry_id}\n"
                    f"[b]Type:[/b] {selected_full_log.urge_type}\n"
                    f"[b]Start Time:[/b] {start_time_str}\n"
                    f"[b]End Time:[/b] {end_time_str}\n"
                    f"[b]Duration:[/b] {duration_str_detail}\n"
                    f"[b]Initial Intensity:[/b] {selected_full_log.initial_intensity}"
                )
                details_static.update(details_text)

                # Format sensations for Markdown
                sensation_md = "### Sensations Logged:\n\n"
                if selected_full_log.sensations_log:
                    for sensation in selected_full_log.sensations_log:
                        s_ts = datetime.datetime.fromisoformat(sensation['timestamp'])
                        if s_ts.tzinfo is None: # Ensure timezone for display
                            s_ts = s_ts.replace(tzinfo=pytz.utc).astimezone(datetime.datetime.now().astimezone().tzinfo)
                        s_time_str = s_ts.strftime('%H:%M:%S')
                        sensation_md += f"* **[{s_time_str}]**: {sensation['note']}\n"
                else:
                    sensation_md += "*No sensations were logged for this urge session.*"

                sensations_markdown.update(sensation_md)
                status_label.update(f"Displaying details for log ID: {self.selected_log_id}")
            else:
                details_static.update("Log details not found.")
                sensations_markdown.update("")
                status_label.update(f"Error: Log with ID {self.selected_log_id} not found in loaded list.")

        except Exception as e:
            details_static.update("Error displaying log details.")
            sensations_markdown.update("")
            status_label.update(f"Error selecting log: {e}")
            # self.app.log(f"Error in ViewUrgeLogsScreen on_data_table_row_selected: {e}")
        elif event.button.id == "back_button":
             self.app.pop_screen()
