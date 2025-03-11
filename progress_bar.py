import sys

class ProgressBar:
    """
    A simple text-based progress bar that updates dynamically in the console.

    Attributes:
        name (str, optional): Label for the progress bar (default: Loading).
        bar_width (int, optional): Total width of the progress bar in characters (default: 20).
        fill_char (str, optional): Character representing completed progress (default: █).
        empty_char (str, optional): Character representing remaining progress (default: ▒).
        bar_ends (tuple, optional): Characters enclosing the progress bar (e.g., brackets) (default: ([, ])).
        total (int, optional): The total value representing 100% completion (default: 100). 
        progress (int, optional): The current progress value (default: 0).
    """

    def __init__(self, name="Loading", bar_width=20, fill_char="█", empty_char="▒", bar_ends=("[", "]"), progress=0, total=100):
        self.name = name
        self.bar_width = bar_width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.bar_ends = bar_ends
        self.total = total
        self.progress = progress
        

    def advance(self, step=1) -> None:
        """
        Increases progress by a given step, ensuring it does not exceed total.
        
        Args:
            step (int, optional): Amount to increment the progress (default: 1).
            
        Returns:
            None.
        """
        
        self.progress = min(self.progress + step, self.total)  # Prevent overflow
        
        
    def render(self, show_percentage=True) -> str:
        """
        Updates and displays the progress bar in the console.

        Args:
            show_percentage (bool, optional): Whether to display the current progress as a percentage (default: True).
            
        Returns:
            str: A string representation of the progress bar with optional percentage or fraction display.
            Returns an empty string if total is less than or equal to zero.
          
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
    

    def update(self, step=1, show_percentage=True) -> None:
        """
        Updates and displays the progress bar in the console.

        Args:
            step (int, optional): Amount to increment the progress (default: 1).
            show_percentage (bool, optional): Whether to display the current progress as a percentage (default: True).
            
        Returns:
            None.
        """
        
        # Advance progress before updating the display
        self.advance(step)

        # Use carriage return '\r' to overwrite the same line
        sys.stdout.write(f"\r{self.render(show_percentage)}")
        sys.stdout.flush() 
        
        # If task is completed, print a new line to start fresh for next task
        if self.progress >= self.total:
            print()