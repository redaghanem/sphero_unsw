"""
# ========================================================================
#  sphero_unsw: Extensions and patches for Sphero BOLT+
#  A fork of the original spherov2 library
#
#  Copyright (c) 2019-2021
#      Hanbang Wang,  https://www.cis.upenn.edu/~hanbangw
#      Elionardo Feliciano
#  Original project: https://github.com/EnotPoloskun/spherov2.py
#
#  library spherov2 was originally created for educational use in CIS 521: 
#  Artificial Intelligence at the University of Pennsylvania, where Sphero 
#  robots are used to help teach the foundations of AI.
#
#
#  This extension was developed by:
#       Kathryn Kasmarik (kathryn.kasmarik@unsw.edu.au)
#       Reda Ghanem (reda.ghanem@unsw.edu.au)
#  From the School of Systems and Computing, UNSW Canberra, to support the Sphero BOLT+ robot.
#
#  This extension has been developed for educational use as part of the course ZEIT1102:
#  Introduction to Programming at the University of New South Wales, Canberra (UNSW Canberra).
#  It is specifically designed to support students in learning programming fundamentals and 
#  introductory robotics concepts through hands-on activities using Sphero BOLT+ robots.
#
#  |---------------------------------------------------------------------|
#  | Version: 0.1.9                                                      |
#  | License: MIT License                                                |
#  | Repository: https://github.com/redaghanem/sphero_unsw               |
#  | Pypi package: https://pypi.org/project/sphero-unsw                  |
#  |---------------------------------------------------------------------|
#
# ========================================================================
"""


# ------------------------------------------------------------------------- #
# [1] Import necessary libraries
# ------------------------------------------------------------------------- #

# Import all necessary classes and functions from sphero_unsw
from sphero_unsw import scanner


# ------------------------------------------------------------------------- #
# [2] Create a new class for scanning and selecting Sphero toys
# ------------------------------------------------------------------------- #

# Define a class named 'toys_scanner' for scanning and selecting Sphero toys
class toys_scanner:
    """
    Scans for nearby Sphero toys and lets the user select one to connect to.
    """

    # Constructor: initializes the object with empty toy list and no selected toy
    def __init__(self):
        self.toys = []            # This will hold the list of found Sphero toys
        self.selected_toy = None  # This will store the toy selected by the user

    # Main method to scan and select a toy
    def scan_and_select_toy(self, scanning_time=3):
        """
        Scan for nearby Sphero toys and let the user select one.

        Args:
            scanning_time (int): How many seconds to scan for toys (default: 3).

        Returns:
            object: The selected toy object, or None if not selected.
        """

        # Loop until the user selects a valid toy
        while True:
            # Print message to user
            print(f"\nScanning for Sphero toys for {scanning_time} seconds...")

            # Use the scanner to find toys nearby
            self.toys = scanner.find_toys(timeout=scanning_time)

            # Check if any toys were found
            if not self.toys:
                # No toys found, print a warning
                print("No Sphero toys found. Ensure your Bluetooth is on and the toy is awake.")
            else:
                # Toys were found, print them in a numbered list
                print("\nAvailable Sphero toys:")
                for idx, toy in enumerate(self.toys, start=1):
                    print(f"{idx}. {toy.name}")  # Show index and toy name

            # Prompt user for input
            print("\nPress 'ENTER' to rescan, or enter the number of the toy to connect:")

            # Read user input and remove leading/trailing whitespace
            choice = input("Your choice: ").strip()

            # If user just presses 'ENTER', restart the loop (rescan)
            if choice == "":
                continue

            try:
                # Convert input to an integer
                choice_num = int(choice)

                # Check if input number corresponds to a toy in the list
                if 1 <= choice_num <= len(self.toys):
                    # Save the selected toy
                    self.selected_toy = self.toys[choice_num - 1]

                    # Print confirmation
                    print(f"You selected: {self.selected_toy.name}\n")

                    # Return the selected toy
                    return self.selected_toy
                else:
                    # User entered a number that's out of range
                    print(f"Please enter a number between 1 and {len(self.toys)}.")
            except ValueError:
                # User did not enter a number
                print(f"Invalid input. Please enter a between 1 and {len(self.toys)} or press 'ENTER' to rescan.")

    # .......................................................................................
    # Function to get the selected toy
    def get_selected_toy(self):
        """
        Get the currently selected toy.

        Returns:
            object: The selected toy object, or None if no toy is selected.
        """
        return self.selected_toy
    # .......................................................................................
