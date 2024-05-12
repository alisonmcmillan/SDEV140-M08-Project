import tkinter as tk  # Importing tkinter library for GUI
from tkinter import messagebox  # Importing messagebox from tkinter for displaying messages
from tkinter import PhotoImage  # Importing PhotoImage from tkinter for image display
import re  # Importing re module for regular expressions

class WelcomeScreen(tk.Frame):
    """
    Displays the welcome screen of the Fitness Tracker App.
    """
    def __init__(self, master, show_login, show_registration):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        
        try:
            self.image = PhotoImage(file="images/image.png")  # Loading image for display
            tk.Label(self, image=self.image).pack()  # Displaying the image
        except tk.TclError as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")  # Displaying error message if image loading fails
        
        tk.Label(self, text="Welcome to Fitness Tracker App", font=("Helvetica", 18)).pack(pady=20)  # Displaying welcome text
        tk.Button(self, text="Login", command=show_login).pack()  # Button to navigate to login screen
        tk.Button(self, text="Sign Up", command=show_registration).pack()  # Button to navigate to registration screen
        tk.Button(self, text="Exit", command=master.quit).pack()  # Button to exit the application

class LoginScreen(tk.Frame):
    """
    Displays the login screen of the Fitness Tracker App.
    """
    def __init__(self, master, show_welcome, show_dashboard):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.show_welcome = show_welcome  # Function reference to show welcome screen
        self.show_dashboard = show_dashboard  # Function reference to show dashboard screen

        tk.Label(self, text="Login", font=("Helvetica", 18)).pack(pady=20)  # Displaying login heading

        tk.Label(self, text="Email:").pack()  # Label for email entry
        self.email_entry = tk.Entry(self)  # Entry widget for email input
        self.email_entry.pack(pady=5)  # Packing email entry widget

        tk.Label(self, text="Password:").pack()  # Label for password entry
        self.password_entry = tk.Entry(self, show="*")  # Entry widget for password input with password masking
        self.password_entry.pack(pady=5)  # Packing password entry widget

        tk.Button(self, text="Login", command=self.login_user).pack(pady=10)  # Button to initiate login process
        tk.Button(self, text="Back", command=self.show_welcome).pack()  # Button to navigate back to welcome screen

    def login_user(self):
        email = self.email_entry.get()  # Getting email input
        password = self.password_entry.get()  # Getting password input

        # Input validation
        if not email.strip():
            tk.messagebox.showerror("Error", "Please enter an email.")
            return

        if not self.validate_email(email):
            tk.messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if not password.strip():
            tk.messagebox.showerror("Error", "Please enter a password.")
            return

        records = self.load_records()  # Loading user records from file

        for record in records:
            if record["email"] == email and record["password"] == password:  # Checking if email and password match
                tk.messagebox.showinfo("Success", f"Welcome back, {record['username']}!")  # Displaying success message
                self.show_dashboard()  # Navigating to dashboard screen
                return

        tk.messagebox.showerror("Error", "Invalid email or password.")  # Displaying error message for invalid credentials

    def validate_email(self, email):
        """
        Validates the format of an email address using regular expressions.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # Regular expression pattern for email validation
        return re.match(pattern, email)  # Checking if email matches the pattern

    def load_records(self):
        """
        Loads user records from a text file.
        """
        try:
            with open("records.txt", "r") as file:  # Opening records file
                records = []
                for line in file:
                    username, email, password = line.strip().split(",")  # Extracting user data from each line
                    records.append({"username": username, "email": email, "password": password})  # Storing user data in records list
            return records  # Returning the list of records
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "Registration records not found.")  # Displaying error if records file not found
            return []  # Returning an empty list if records file not found

class RegistrationScreen(tk.Frame):
    """
    Displays the registration screen of the Fitness Tracker App.
    """
    def __init__(self, master, show_welcome):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self, text="Registration", font=("Helvetica", 18)).pack(pady=20)  # Displaying registration heading
        tk.Label(self, text="Username:").pack()  # Label for username entry
        self.username_entry = tk.Entry(self)  # Entry widget for username input
        self.username_entry.pack(pady=5)  # Packing username entry widget

        tk.Label(self, text="Email:").pack()  # Label for email entry
        self.email_entry = tk.Entry(self)  # Entry widget for email input
        self.email_entry.pack(pady=5)  # Packing email entry widget

        tk.Label(self, text="Password:").pack()  # Label for password entry
        self.password_entry = tk.Entry(self, show="*")  # Entry widget for password input with password masking
        self.password_entry.pack(pady=5)  # Packing password entry widget

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)  # Button to initiate registration process
        tk.Button(self, text="Back", command=show_welcome).pack()  # Button to navigate back to welcome screen

        self.show_welcome = show_welcome  # Function reference to show welcome screen

    def register_user(self):
        username = self.username_entry.get()  # Getting username input
        email = self.email_entry.get()  # Getting email input
        password = self.password_entry.get()  # Getting password input

        if not username.strip():
            tk.messagebox.showerror("Error", "Please enter a username.")  # Displaying error message for empty username
            return

        if not email.strip():
            tk.messagebox.showerror("Error", "Please enter an email.")  # Displaying error message for empty email
            return

        if not self.validate_email(email):
            tk.messagebox.showerror("Error", "Please enter a valid email address.")  # Displaying error message for invalid email
            return

        if not password.strip():
            tk.messagebox.showerror("Error", "Please enter a password.")  # Displaying error message for empty password
            return

        self.save_registration(username, email, password)  # Saving registration data to file

        self.show_dashboard_screen()  # Navigating to dashboard screen

        messagebox.showinfo("Success", "Registration successful!")  # Displaying success message for registration

    def validate_email(self, email):
        """
        Validates the format of an email address using regular expressions.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # Regular expression pattern for email validation
        return re.match(pattern, email)  # Checking if email matches the pattern

    def save_registration(self, username, email, password):
        """
        Saves user registration data to a text file.
        """
        try:
            with open("records.txt", "a") as file:  # Opening records file in append mode
                file.write(f"{username},{email},{password}\n")  # Writing user data to file
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save registration: {e}")  # Displaying error message if registration fails

    def show_dashboard_screen(self):
        self.destroy()  # Destroying current frame
        self.show_welcome()  # Navigating back to welcome screen

class DashboardScreen(tk.Frame):
    """
    Displays the dashboard screen of the Fitness Tracker App.
    """
    def __init__(self, master, show_welcome):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        try:
            self.image = PhotoImage(file="images/image1.png")  # Loading image for display
            tk.Label(self, image=self.image).pack()  # Displaying the image
        except tk.TclError as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")  # Displaying error message if image loading fails

        tk.Label(self, text="Dashboard", font=("Helvetica", 18)).pack(pady=20)  # Displaying dashboard heading

        tk.Button(self, text="Logout", command=show_welcome).pack()  # Button to logout and navigate to welcome screen

class FitnessTrackerApp(tk.Tk):
    """
    Main application class for the Fitness Tracker App.
    """
    def __init__(self):
        super().__init__()
        self.title("Fitness Tracker App")  # Setting window title
        self.geometry("600x400")  # Setting window size
        self.current_screen = None  # Variable to keep track of current screen
        self.show_welcome_screen()  # Displaying welcome screen initially

    def show_welcome_screen(self):
        """
        Displays the welcome screen.
        """
        if self.current_screen:
            self.current_screen.destroy()  # Destroying current screen if exists

        self.current_screen = WelcomeScreen(self, self.show_login_screen, self.show_registration_screen)  # Displaying welcome screen

    def show_login_screen(self):
        """
        Displays the login screen.
        """
        if self.current_screen:
            self.current_screen.destroy()  # Destroying current screen if exists

        self.current_screen = LoginScreen(self, self.show_welcome_screen, self.show_dashboard_screen)  # Displaying login screen

    def show_registration_screen(self):
        """
        Displays the registration screen.
        """
        if self.current_screen:
            self.current_screen.destroy()  # Destroying current screen if exists

        self.current_screen = RegistrationScreen(self, self.show_welcome_screen)  # Displaying registration screen

    def show_dashboard_screen(self):
        """
        Displays the dashboard screen.
        """
        if self.current_screen:
            self.current_screen.destroy()  # Destroying current screen if exists

        self.current_screen = DashboardScreen(self, self.show_welcome_screen)  # Displaying dashboard screen

if __name__ == "__main__":
    app = FitnessTrackerApp()  # Creating instance of FitnessTrackerApp
    app.mainloop()  # Running the application loop
