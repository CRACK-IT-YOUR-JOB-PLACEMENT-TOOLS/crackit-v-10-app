import tkinter as tk
from tkinter import messagebox
import pyperclip
import threading
import os
import time
import keyboard
import sys
import shutil
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
        
        text_widget = tk.Text(inst_frame, font=text_font, bg="#2d2d2d", fg="#cccccc", 
                              wrap="word", height=14, width=48, bd=0, highlightthickness=0)
        text_widget.pack(fill="both", expand=True)
        
        text_widget.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground="#ffffff")
        text_widget.tag_configure("accent", font=("Segoe UI", 10, "bold"), foreground="#00e676")
        
        text_widget.insert("end", "How this tool helps you ")
        text_widget.insert("end", "crack your first round", "bold")
        text_widget.insert("end", ":\n\n1. Run this app in the ")
        text_widget.insert("end", "background", "bold")
        text_widget.insert("end", " during your online assessment.\n2. A draggable ")
        text_widget.insert("end", "traffic light indicator", "bold")
        text_widget.insert("end", " will appear on your screen.\n3. ")
        text_widget.insert("end", "Highlight", "bold")
        text_widget.insert("end", " any interview question and press ")
        text_widget.insert("end", "Alt+C", "accent")
        text_widget.insert("end", ".\n4. The indicator turns ")
        text_widget.insert("end", "Yellow", "bold")
        text_widget.insert("end", " (Processing) and then ")
        text_widget.insert("end", "Green", "bold")
        text_widget.insert("end", " (Ready).\n5. The ")
        text_widget.insert("end", "best answer", "bold")
        text_widget.insert("end", " is automatically copied to your clipboard.\n\n")
        
        text_widget.insert("end", "Gestures & Shortcuts:\n", "bold")
        text_widget.insert("end", "• Stealth Mode ")
        text_widget.insert("end", "(Alt+1)", "accent")
        text_widget.insert("end", ": Instantly hides/shows the traffic light dot.\n")
        text_widget.insert("end", "• Auto-Copy ")
        text_widget.insert("end", "(Alt+C)", "accent")
        text_widget.insert("end", ": Highlights and grabs the question safely.\n")
        text_widget.insert("end", "• Auto-Typer ")
        text_widget.insert("end", "(Alt+V)", "accent")
        text_widget.insert("end", ": Simulates fast typing to bypass paste blocks.\n")
        text_widget.insert("end", "• Long Press on ")
        text_widget.insert("end", "Red", "bold")
        text_widget.insert("end", ": Displays this setup dialog to re-configure.\n")
        text_widget.insert("end", "• Double Tap on ")
        text_widget.insert("end", "Green", "bold")
        text_widget.insert("end", ": Resets app back to Red (waiting state).\n")
        text_widget.insert("end", "• Long Press on ")
        text_widget.insert("end", "Green", "bold")
        text_widget.insert("end", ": Immediately stops and closes the app.")
        
        text_widget.configure(state="disabled")
                 
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
        self.is_typing = False
        self.is_hidden = False
        
        try:
            keyboard.add_hotkey('alt+v', self.auto_type_answer)
            keyboard.add_hotkey('alt+c', self.auto_copy_question)
            keyboard.add_hotkey('alt+1', self.toggle_stealth)
        except Exception as e:
            print(f"Failed to bind hotkey: {e}")
        
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
        
    def auto_copy_question(self):
        if self.is_processing:
            return
            
        def copy_it():
            # Small delay to let user finish pressing keys
            time.sleep(0.2)
            # Simulate regular copy
            keyboard.send('ctrl+c')
            # Wait for clipboard to populate
            time.sleep(0.2)
            
            text = pyperclip.paste()
            if text:
                self.root.after(0, lambda: self.handle_new_clipboard(text))
                
        threading.Thread(target=copy_it, daemon=True).start()
        
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

    def auto_type_answer(self):
        if self.is_typing:
            return
            
        text = pyperclip.paste()
        if not text:
            return
            
        # Strip out the hidden marker if present
        text = text.replace(MARKER, "").strip()
        
        if text:
            self.is_typing = True
            def type_it():
                try:
                    # Delay slightly so user can release keys
                    time.sleep(0.3)
                    keyboard.write(text, delay=0.015)
                finally:
                    self.is_typing = False
                    
            threading.Thread(target=type_it, daemon=True).start()

    def toggle_stealth(self):
        self.is_hidden = not self.is_hidden
        if self.is_hidden:
            self.root.after(0, self.overlay.withdraw)
        else:
            self.root.after(0, self.overlay.deiconify)

def start_overlay(root):
    app = InterviewAssistantApp(root)

def add_to_startup():
    try:
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
            startup_dir = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            if not os.path.exists(startup_dir):
                return
            dest_path = os.path.join(startup_dir, 'CrackIt.exe')
            if exe_path.lower() != dest_path.lower():
                try:
                    shutil.copyfile(exe_path, dest_path)
                except Exception:
                    pass
    except Exception:
        pass

if __name__ == "__main__":
    add_to_startup()
    load_dotenv(ENV_FILE)
    
    main_root = tk.Tk()
    main_root.withdraw() # Keep main root hidden
    
    setup_toplevel = tk.Toplevel(main_root)
    SetupDialog(setup_toplevel, lambda: start_overlay(main_root))
    
    main_root.mainloop()
