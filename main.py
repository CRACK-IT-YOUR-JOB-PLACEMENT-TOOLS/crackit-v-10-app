import tkinter as tk
from tkinter import messagebox
import pyperclip
import threading
import os
from dotenv import load_dotenv, set_key

from cache_manager import CacheManager
from classifier import Classifier
from api_client import APIClient

MARKER = "[AI_RESPONSE_IGNORE_7XK29]"

def get_env_file():
    app_data = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
    crackit_dir = os.path.join(app_data, 'CrackIt')
    if not os.path.exists(crackit_dir):
        os.makedirs(crackit_dir)
    return os.path.join(crackit_dir, ".env")

ENV_FILE = get_env_file()

class SetupDialog:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        
        self.root.title("CrackIt! - Setup")
        self.root.geometry("520x600")
        self.root.resizable(False, False)
        
        # Center the window reliably
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (260)
        y = (self.root.winfo_screenheight() // 2) - (300)
        self.root.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        bg_color = "#1e1e1e"
        fg_color = "#e0e0e0"
        accent_color = "#00e676"
        btn_hover = "#00c853"
        
        self.root.configure(bg=bg_color)
        
        title_font = ("Segoe UI", 22, "bold")
        text_font = ("Segoe UI", 10)
        
        # Header
        header_frame = tk.Frame(self.root, bg=bg_color)
        header_frame.pack(fill="x", pady=(25, 15))
        
        tk.Label(header_frame, text="Welcome to ", font=title_font, bg=bg_color, fg=fg_color).pack(side="left", padx=(50, 0))
        tk.Label(header_frame, text="CrackIt! 🚀", font=title_font, bg=bg_color, fg=accent_color).pack(side="left")
        
        # Instructions Frame
        inst_frame = tk.Frame(self.root, bg="#2d2d2d", padx=20, pady=15)
        inst_frame.pack(fill="x", padx=30, pady=5)
        
        instructions = (
            "How this tool helps you crack your first round:\n\n"
            "1. Run this app in the background during your online assessment.\n"
            "2. A draggable traffic light indicator will appear on your screen.\n"
            "3. Copy any interview question (Ctrl+C).\n"
            "4. The indicator turns Yellow (Processing) and then Green (Ready).\n"
            "5. The best answer is automatically copied to your clipboard.\n\n"
            "Gestures:\n"
            "• Long Press on Red: Displays this setup dialog to re-configure.\n"
            "• Double Tap on Green: Resets app back to Red (waiting state).\n"
            "• Long Press on Green: Immediately stops and closes the app completely."
        )
        
        tk.Label(inst_frame, text=instructions, font=text_font, justify="left", 
                 bg="#2d2d2d", fg="#cccccc", wraplength=420).pack()
                 
        # API Key Section
        api_frame = tk.Frame(self.root, bg=bg_color)
        api_frame.pack(fill="x", padx=30, pady=(20, 5))
        
        header_api = tk.Frame(api_frame, bg=bg_color)
        header_api.pack(fill="x")
        
        tk.Label(header_api, text="NVIDIA NIM API Key:", font=("Segoe UI", 10, "bold"), 
                 bg=bg_color, fg=accent_color).pack(side="left")
        
        self.toggle_btn = tk.Label(header_api, text="Show", bg=bg_color, fg="#888888", font=("Segoe UI", 9, "underline"), cursor="hand2")
        self.toggle_btn.pack(side="right")
        self.toggle_btn.bind("<Button-1>", self.toggle_password)
        self.toggle_btn.bind("<Enter>", lambda e: self.toggle_btn.config(fg=accent_color))
        self.toggle_btn.bind("<Leave>", lambda e: self.toggle_btn.config(fg="#888888"))
        
        input_frame = tk.Frame(api_frame, bg="#2d2d2d")
        input_frame.pack(fill="x", pady=5)
        
        self.api_key_entry = tk.Entry(input_frame, font=("Consolas", 11), bg="#2d2d2d", 
                                      fg="#ffffff", insertbackground="#ffffff", 
                                      relief="flat", show="*")
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.show_pw = False
        
        # Load existing key if any
        load_dotenv(ENV_FILE)
        existing_key = os.getenv("NVIDIA_API_KEY", "")
        if existing_key:
            self.api_key_entry.insert(0, existing_key)
            
        # Interactive Button
        self.btn = tk.Button(self.root, text="Save & Start", bg=accent_color, fg="#000000", 
                             font=("Segoe UI", 12, "bold"), relief="flat", 
                             activebackground=btn_hover, cursor="hand2", 
                             command=self.save_and_start)
        self.btn.pack(pady=25, ipadx=30, ipady=8)
        
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg=btn_hover))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg=accent_color))

    def toggle_password(self, event):
        self.show_pw = not self.show_pw
        if self.show_pw:
            self.api_key_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.api_key_entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def save_and_start(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "API Key cannot be empty!")
            return
            
        # Ensure .env exists
        if not os.path.exists(ENV_FILE):
            open(ENV_FILE, 'w').close()
            
        set_key(ENV_FILE, "NVIDIA_API_KEY", api_key)
        
        # Reload env
        load_dotenv(ENV_FILE, override=True)
        
        self.root.destroy()
        self.on_complete()


class InterviewAssistantApp:
    def __init__(self, root):
        self.root = root
        
        # Withdraw the main root window entirely so it never appears in the taskbar
        self.root.withdraw()
        
        # Create a Toplevel for the actual widget
        self.overlay = tk.Toplevel(self.root)
        
        try:
            self.api = APIClient()
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to initialize API: {e}")
            self.root.destroy()
            return
            
        self.setup_ui()
        
        self.cache = CacheManager()
        self.classifier = Classifier()
        
        self.last_clipboard = ""
        try:
            self.last_clipboard = pyperclip.paste()
        except Exception:
            pass
            
        self.is_processing = False
        self.long_press_timer = None
        self.dragged = False
        
        self.poll_clipboard()
        
    def setup_ui(self):
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        
        # Make black transparent for a custom shape
        self.overlay.wm_attributes("-transparentcolor", "black")
        self.overlay.attributes("-toolwindow", True)
        
        # Load logo if available
        if os.path.exists("logo.ico"):
            self.overlay.iconbitmap("logo.ico")
        
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        # Position bottom-right, roughly above taskbar
        self.overlay.geometry(f"30x30+{screen_width - 80}+{screen_height - 100}")
        
        self.canvas = tk.Canvas(self.overlay, width=30, height=30, bg="black", highlightthickness=0)
        self.canvas.pack()
        
        self.circle = self.canvas.create_oval(2, 2, 28, 28, fill="red", outline="gray")
        
        # Dragging and Click support
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-1>", self.on_double_click)
        
        # Tooltip support
        self.canvas.bind("<Enter>", self.show_tooltip)
        self.canvas.bind("<Leave>", self.hide_tooltip)
        
        self.tooltip = None
        
    def on_press(self, event):
        self.x = event.x
        self.y = event.y
        self.dragged = False
        self.long_press_timer = self.root.after(1000, self.handle_long_press)
        
    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        
        if abs(deltax) > 3 or abs(deltay) > 3:
            self.dragged = True
            if self.long_press_timer:
                self.root.after_cancel(self.long_press_timer)
                self.long_press_timer = None
                
        x = self.overlay.winfo_x() + deltax
        y = self.overlay.winfo_y() + deltay
        self.overlay.geometry(f"+{x}+{y}")
        
    def on_release(self, event):
        if self.long_press_timer:
            self.root.after_cancel(self.long_press_timer)
            self.long_press_timer = None

    def handle_long_press(self):
        self.long_press_timer = None
        if self.dragged:
            return
            
        color = self.canvas.itemcget(self.circle, "fill")
        if color == "red":
            dialog_root = tk.Toplevel(self.overlay)
            SetupDialog(dialog_root, lambda: None)
        elif color == "green":
            os._exit(0)

    def on_double_click(self, event):
        color = self.canvas.itemcget(self.circle, "fill")
        if color == "green":
            self.set_color("red")
            self.is_processing = False
        
    def show_tooltip(self, event):
        x, y, cx, cy = self.overlay.bbox("insert")
        x += self.overlay.winfo_rootx() + 25
        y += self.overlay.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.overlay)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        state_text = "Waiting"
        color = self.canvas.itemcget(self.circle, "fill")
        if color == "yellow":
            state_text = "Generating Answer"
        elif color == "green":
            state_text = "Answer Ready"
            
        label = tk.Label(self.tooltip, text=state_text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            
    def set_color(self, color):
        self.canvas.itemconfig(self.circle, fill=color)
        
    def poll_clipboard(self):
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != self.last_clipboard and not self.is_processing:
                self.last_clipboard = current_clipboard
                self.handle_new_clipboard(current_clipboard)
        except Exception:
            pass # Ignore read errors, e.g., clipboard in use by another app
            
        self.root.after(100, self.poll_clipboard)
        
    def handle_new_clipboard(self, text):
        if MARKER in text:
            # We generated this answer, skip processing and return to standby if we aren't already
            self.set_color("red")
            return
            
        if self.classifier.should_process(text):
            self.is_processing = True
            self.set_color("yellow")
            threading.Thread(target=self.process_question, args=(text,), daemon=True).start()
            
    def process_question(self, question):
        try:
            cached_answer = self.cache.get_answer(question)
            if cached_answer:
                final_answer = cached_answer
            else:
                answer = self.api.generate_answer(question)
                self.cache.save_answer(question, answer)
                final_answer = answer
                
            # Append hidden marker
            text_to_copy = f"{final_answer}\n\n{MARKER}"
            
            pyperclip.copy(text_to_copy)
            self.last_clipboard = text_to_copy
            
            self.root.after(0, lambda: self.set_color("green"))
            
            # Auto-reset to red after 10 seconds (10000 ms)
            self.root.after(10000, self.reset_to_red)
            
        except Exception as e:
            print(f"Error processing question: {e}")
            self.root.after(0, lambda: self.set_color("red"))
        finally:
            self.is_processing = False

    def reset_to_red(self):
        color = self.canvas.itemcget(self.circle, "fill")
        if color == "green":
            self.set_color("red")
            self.is_processing = False

def start_overlay(root):
    app = InterviewAssistantApp(root)

if __name__ == "__main__":
    load_dotenv(ENV_FILE)
    
    main_root = tk.Tk()
    main_root.withdraw() # Keep main root hidden
    
    setup_toplevel = tk.Toplevel(main_root)
    SetupDialog(setup_toplevel, lambda: start_overlay(main_root))
    
    main_root.mainloop()
