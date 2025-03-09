import sys

class ProgressBar:
    """
    A simple text-based progress bar that updates dynamically in the console.

    Attributes:
        name (str): Label for the progress bar.
        bar_width (int): Total width of the progress bar in characters.
        fill_char (str): Character representing completed progress.
        empty_char (str): Character representing remaining progress.
        bar_ends (tuple): Characters enclosing the progress bar (e.g., brackets).
        total (int): The total value representing 100% completion.
        progress (int): The current progress value.
    """

    def __init__(self, name="Loading", bar_width=20, fill_char="█", empty_char="▒", bar_ends=("[", "]"), progress=0, total=100):
        self.name = name
        self.bar_width = bar_width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.bar_ends = bar_ends
        self.total = total
        self.progress = progress
        

    def advance(self, step=1):
        """
        Increases progress by a given step, ensuring it does not exceed total.
        
        Args:
            step (int): Amount to increase progress by.
        """
        self.progress = min(self.progress + step, self.total)  # Prevent overflow
        
        
    def render(self, show_percentage=True) -> str:
        """
        Updates and displays the progress bar in the console.

        Args:
            step (int): Amount to increment the progress.
            show_percentage (bool): Whether to display the percentage value.
            persistent (bool): If False, clears the console before updating.
        """
        
        if self.total <= 0:
            return ""

        progress_ratio = self.progress / self.total
        filled_length = round(progress_ratio * self.bar_width)  # Number of filled characters
        empty_length = self.bar_width - filled_length  # Remaining characters

        # Construct the visual bar
        progress_bar = f"{self.bar_ends[0]}{self.fill_char * filled_length}{self.empty_char * empty_length}{self.bar_ends[1]}"

        # Format progress display
        progress_display = f"{progress_ratio * 100:.1f}%" if show_percentage else f"{self.progress}/{self.total}"

        # Return the progress bar
        return f"{self.name}: {progress_bar} {progress_display}"
    

    def update(self, step=1, show_percentage=True):
        """
        Updates and displays the progress bar in the console.

        Args:
            step (int): Amount to increment the progress.
            show_percentage (bool): Whether to display the percentage value.
        """
        # Advance progress before updating the display
        self.advance(step)

        # Use carriage return '\r' to overwrite the same line
        sys.stdout.write(f"\r{self.render(show_percentage)}")
        sys.stdout.flush()  # Ensure immediate output
        
        # If task is completed, print a new line to start fresh for next task
        if self.progress >= self.total:
            print()  # Prints a new line