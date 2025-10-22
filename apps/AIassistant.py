import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime


class AIAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        self.root.attributes('-topmost', True)

        # Initialize conversation history
        self.conversation_history = []

        # Try to load existing API key
        self.load_api_key()

        # Setup GUI
        self.setup_gui()

        # Check if API key is available
        if not hasattr(self, 'client') or self.client is None:
            self.prompt_for_api_key()

    def load_api_key(self):
        """Load API key from .env file or environment variables"""
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')

        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                # Test the API key with a simple request
                self.client.models.list()
                print("API key loaded successfully")
            except Exception as e:
                print(f"Error with API key: {e}")
                self.client = None
        else:
            self.client = None

    def save_api_key(self, api_key):
        """Save API key to .env file"""
        try:
            with open('.env', 'w') as f:
                f.write(f'OPENAI_API_KEY={api_key}\n')
            os.environ['OPENAI_API_KEY'] = api_key
            self.client = OpenAI(api_key=api_key)
            messagebox.showinfo("Success", "API key saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API key: {e}")
            return False

    def prompt_for_api_key(self):
        """Prompt user to enter API key"""
        api_key = simpledialog.askstring(
            "API Key Required",
            "Please enter your OpenAI API key:",
            show='*',
            parent=self.root
        )

        if api_key:
            if self.save_api_key(api_key):
                self.api_status_label.config(text="API: Connected ✓", foreground="green")
            else:
                self.api_status_label.config(text="API: Disconnected ✗", foreground="red")
        else:
            self.api_status_label.config(text="API: Disconnected ✗", foreground="red")
            messagebox.showwarning("Warning", "API key is required to use the chatbot")

    def setup_gui(self):
        """Setup the main GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Title
        title_label = ttk.Label(
            header_frame,
            text="AI Assistant",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)

        # API status
        status_text = "API: Connected ✓" if self.client else "API: Disconnected ✗"
        status_color = "green" if self.client else "red"
        self.api_status_label = ttk.Label(
            header_frame,
            text=status_text,
            foreground=status_color,
            font=('Arial', 10)
        )
        self.api_status_label.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))

        # Configure header frame grid
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=0)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=('Arial', 10),
            state=tk.DISABLED
        )
        self.chat_display.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # User input
        self.user_input = ttk.Entry(
            input_frame,
            font=('Arial', 10)
        )
        self.user_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.user_input.bind('<Return>', lambda e: self.send_message())

        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
        send_button.grid(row=0, column=1)

        # Configure input frame grid
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=0)

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        # Clear conversation button
        clear_button = ttk.Button(
            control_frame,
            text="Clear Conversation",
            command=self.clear_conversation
        )
        clear_button.grid(row=0, column=0, padx=(0, 10))

        # Settings button
        settings_button = ttk.Button(
            control_frame,
            text="API Settings",
            command=self.open_settings
        )
        settings_button.grid(row=0, column=1)

        # Configure control frame grid
        control_frame.columnconfigure(0, weight=0)
        control_frame.columnconfigure(1, weight=0)
        control_frame.columnconfigure(2, weight=1)

    def send_message(self):
        """Send user message and get AI response"""
        user_message = self.user_input.get().strip()

        if not user_message:
            return

        if not self.client:
            messagebox.showerror("Error", "Please configure your API key first!")
            self.prompt_for_api_key()
            return

        # Clear input field
        self.user_input.delete(0, tk.END)

        # Display user message
        self.display_message("You", user_message, "user")

        # Get AI response
        self.get_ai_response(user_message)

    def get_ai_response(self, user_message):
        """Get response from OpenAI API"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})

            # Create chat completion
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content

            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            # Display AI response
            self.display_message("Assistant", ai_response, "assistant")

        except openai.AuthenticationError:
            messagebox.showerror("Authentication Error", "Invalid API key. Please update your API settings.")
            self.api_status_label.config(text="API: Disconnected ✗", foreground="red")
            self.client = None
        except openai.RateLimitError:
            messagebox.showerror("Rate Limit", "Rate limit exceeded. Please try again later.")
        except openai.APIError as e:
            messagebox.showerror("API Error", f"OpenAI API error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_message(self, sender, message, message_type):
        """Display message in chat display"""
        self.chat_display.config(state=tk.NORMAL)

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}:\n", "timestamp")

        # Add message with appropriate formatting
        if message_type == "user":
            self.chat_display.insert(tk.END, f"{message}\n\n", "user_message")
        else:
            self.chat_display.insert(tk.END, f"{message}\n\n", "assistant_message")

        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_conversation(self):
        """Clear the conversation history and display"""
        self.conversation_history = []
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Add welcome message
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Welcome to AI Assistant! How can I help you today?\n\n", "welcome")
        self.chat_display.config(state=tk.DISABLED)

    def open_settings(self):
        """Open API settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("API Settings")
        settings_window.geometry("400x200")
        settings_window.resizable(False, False)
        settings_window.attributes('-topmost', True)

        # Center the settings window
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Settings frame
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # API key entry
        ttk.Label(settings_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(
            settings_frame,
            textvariable=api_key_var,
            width=50,
            show='*'
        )
        api_key_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        # Load current API key if exists
        current_key = os.getenv('OPENAI_API_KEY')
        if current_key:
            api_key_var.set(current_key)

        # Buttons frame
        buttons_frame = ttk.Frame(settings_frame)
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

        def save_settings():
            new_api_key = api_key_var.get().strip()
            if new_api_key:
                if self.save_api_key(new_api_key):
                    self.api_status_label.config(text="API: Connected ✓", foreground="green")
                    settings_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter an API key")

        def clear_key():
            api_key_var.set("")

        # Save button
        ttk.Button(
            buttons_frame,
            text="Save",
            command=save_settings
        ).grid(row=0, column=0, padx=(0, 10))

        # Clear button
        ttk.Button(
            buttons_frame,
            text="Clear",
            command=clear_key
        ).grid(row=0, column=1, padx=(0, 10))

        # Cancel button
        ttk.Button(
            buttons_frame,
            text="Cancel",
            command=settings_window.destroy
        ).grid(row=0, column=2)

        # Configure grid weights
        settings_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)


def main():
    # Create and run the application
    root = tk.Tk()
    app = AIAssistant(root)

    # Configure text tags for styling
    app.chat_display.tag_configure("user_message", foreground="blue")
    app.chat_display.tag_configure("assistant_message", foreground="green")
    app.chat_display.tag_configure("timestamp", foreground="gray", font=('Arial', 8, 'italic'))
    app.chat_display.tag_configure("welcome", foreground="purple", font=('Arial', 10, 'bold'))

    # Add welcome message
    app.clear_conversation()

    root.mainloop()


if __name__ == "__main__":
    main()