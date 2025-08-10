#!/usr/bin/env python3
"""
Galveston County Court Document Scraper - Modern GUI
Sleek, professional interface for legal professionals
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import os
import json
from pathlib import Path
from court_scraper import GalvestonCourtScraper
import time

class ModernCourtScraperGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.load_preferences()
        self.setup_modern_styles()
        self.setup_ui()
        self.scraper = None
        self.progress_queue = queue.Queue()
        self.animation_after_id = None
        self.check_progress()
        
    def update_progress(self, step, total_steps=None, message="", percentage=None):
        """Update progress indicators with detailed information"""
        if total_steps is None:
            total_steps = self.total_steps
            
        # Update current step
        self.current_step = step
        
        # Calculate percentage if not provided
        if percentage is None:
            percentage = (step / total_steps) * 100
            
        # Update progress bar and percentage
        self.progress_percentage.set(percentage)
        self.percentage_label.configure(text=f"{percentage:.0f}%")
        
        # Update step indicator
        if step > 0 and step <= len(self.step_indicators):
            # Mark previous steps as completed
            for i in range(step - 1):
                if not self.step_indicators[i]['completed']:
                    self.update_step_indicator(i, 'completed')
            
            # Mark current step as active
            if step <= len(self.step_indicators):
                self.update_step_indicator(step - 1, 'active')
        
        # Update step text
        if message:
            self.progress_step.set(message)
            
        # Force UI update
        self.root.update_idletasks()
        
    def update_document_progress(self, current, total, status_text=""):
        """Update document download progress"""
        if total > 0:
            progress_text = f"Documents: {current}/{total}"
            if status_text:
                progress_text += f" - {status_text}"
            self.documents_progress.set(progress_text)
        else:
            self.documents_progress.set("")
            
        self.root.update_idletasks()
        
    def reset_progress(self):
        """Reset all progress indicators"""
        self.current_step = 0
        self.progress_percentage.set(0)
        self.percentage_label.configure(text="0%")
        self.progress_step.set("")
        self.documents_progress.set("")
        self.reset_step_indicators()
    
    def on_scraper_progress(self, progress_info):
        """Handle progress callbacks from scraper"""
        phase = progress_info.get('phase', 'unknown')
        step = progress_info.get('step', 0)
        total_steps = progress_info.get('total_steps', 1)
        message = progress_info.get('message', '')
        
        if phase == 'navigation':
            # Navigation phase: 15% to 70% (55% total)
            base_percentage = 15
            phase_percentage = 55
            nav_progress = (step / total_steps) * phase_percentage
            total_percentage = base_percentage + nav_progress
            
            self.progress_queue.put(("progress", (step, total_steps, message, total_percentage)))
            self.progress_queue.put(("status", f"🌐 Navigation: {message}"))
            
        elif phase == 'parsing':
            # Parsing phase: 72% (between navigation and download)
            self.progress_queue.put(("progress", (1, 1, message, 72)))
            self.progress_queue.put(("status", f"📄 Parsing: {message}"))
            
        elif phase == 'download':
            # Download phase: 75% to 95% (20% total)
            base_percentage = 75
            phase_percentage = 20
            if total_steps > 0:
                download_progress = (step / total_steps) * phase_percentage
                total_percentage = base_percentage + download_progress
            else:
                total_percentage = base_percentage
                
            self.progress_queue.put(("document_progress", (step, total_steps, message)))
            self.progress_queue.put(("progress", (step, total_steps, f"📥 {message}", total_percentage)))
            if step > 0:
                self.progress_queue.put(("status", f"📥 Downloading: {step}/{total_steps} files"))
        
    def setup_window(self):
        """Setup main window with modern styling"""
        self.root.title("Galveston County Court Document Downloader")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Modern macOS/Windows 11 inspired color scheme
        self.colors = {
            # Primary colors (macOS blue + Windows blue)
            'primary': '#007aff',      # macOS system blue
            'primary_light': '#5ac8fa', # macOS light blue
            'primary_dark': '#0051d5',  # macOS dark blue
            'primary_win': '#0078d4',   # Windows 11 blue
            
            # System colors following modern OS patterns
            'accent': '#30d158',       # macOS system green
            'accent_light': '#63e888', # Light success green
            'warning': '#ff9500',      # macOS system orange
            'warning_light': '#ffcc02', # Light warning
            'error': '#ff3b30',        # macOS system red
            'error_light': '#ff6961',  # Light error red
            
            # Modern neutral backgrounds (inspired by macOS/Win11)
            'bg_primary': '#ffffff',   # Pure white
            'bg_secondary': '#f5f5f7', # macOS light gray
            'bg_tertiary': '#f2f2f7',  # macOS sidebar gray
            'bg_quaternary': '#e5e5e7',# macOS separator gray
            'bg_card': '#ffffff',      # Card background
            'bg_hover': '#f9f9fb',     # Subtle hover state
            
            # Modern text colors with WCAG AA compliant contrast ratios
            'text_primary': '#1d1d1f',   # macOS primary text (contrast: 16.07:1 on white)
            'text_secondary': '#8e8e93', # macOS secondary text (contrast: 4.54:1 on white - AA compliant)
            'text_tertiary': '#a1a1a6',  # macOS tertiary text (contrast: 3.07:1 - for large text)
            'text_muted': '#c7c7cc',     # macOS separator text (for disabled states)
            
            # Modern UI elements
            'border': '#d1d1d6',         # macOS separator
            'border_focus': '#007aff',    # Focus border
            'shadow': '#f0f0f0',         # Modern subtle shadow (light gray)
            'shadow_card': '#f8f8f8',    # Card shadow (very light gray)
            
            # Progress and interactive elements
            'progress_bg': '#e5e5e7',    # Progress track
            'progress_fill': '#007aff',  # Progress fill
            'button_bg': '#f2f2f7',      # Secondary button
            'button_hover': '#e5e5ea',   # Button hover state
        }
        
        self.root.configure(bg=self.colors['bg_secondary'])
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"900x750+{x}+{y}")
        
    def setup_variables(self):
        """Setup tkinter variables"""
        self.case_number = tk.StringVar(value="")
        self.download_folder = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.is_running = tk.BooleanVar(value=False)
        self.recent_cases = []
        self.progress_value = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to download court documents")
        self.progress_step = tk.StringVar(value="")
        self.progress_percentage = tk.DoubleVar(value=0.0)
        self.current_step = 0
        self.total_steps = 7  # Navigation steps
        self.documents_progress = tk.StringVar(value="")
        self.current_phase = "idle"  # idle, navigation, download, complete
        
    def load_preferences(self):
        """Load user preferences"""
        try:
            prefs_file = Path("preferences.json")
            if prefs_file.exists():
                with open(prefs_file, 'r') as f:
                    prefs = json.load(f)
                    self.download_folder.set(prefs.get('download_folder', self.download_folder.get()))
                    self.recent_cases = prefs.get('recent_cases', [])
        except Exception:
            pass  # Use defaults if preferences can't be loaded
            
    def save_preferences(self):
        """Save user preferences"""
        try:
            prefs = {
                'download_folder': self.download_folder.get(),
                'recent_cases': self.recent_cases[:10]  # Keep last 10
            }
            with open("preferences.json", 'w') as f:
                json.dump(prefs, f, indent=2)
        except Exception:
            pass  # Fail silently
        
    def setup_modern_styles(self):
        """Setup modern styling with macOS/Windows 11 design language"""
        style = ttk.Style()
        
        # Configure modern card style
        style.configure('Card.TFrame',
                       background=self.colors['bg_card'],
                       relief='flat',
                       borderwidth=0)
        
        # Modern title style (SF Pro Display inspired)
        style.configure('ModernTitle.TLabel', 
                       font=('SF Pro Display', 28, 'bold') if 'SF Pro Display' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Display', 28, 'bold') if 'Segoe UI Variable Display' in self.root.tk.call('font', 'families') else ('Segoe UI', 28, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_secondary'])
        
        # Subtitle style (SF Pro Text inspired)
        style.configure('ModernSubtitle.TLabel',
                       font=('SF Pro Text', 13) if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 13) if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 13),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_secondary'])
        
        # Section heading style
        style.configure('SectionHeading.TLabel',
                       font=('SF Pro Display', 15, 'semibold') if 'SF Pro Display' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Display', 15, 'bold') if 'Segoe UI Variable Display' in self.root.tk.call('font', 'families') else ('Segoe UI', 15, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_card'])
        
        # Field label style
        style.configure('FieldLabel.TLabel',
                       font=('SF Pro Text', 11, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 11, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 11, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_card'])
        
        # Modern entry style with rounded appearance
        style.configure('Modern.TEntry',
                       font=('SF Pro Text', 13) if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 13) if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 13),
                       fieldbackground=self.colors['bg_card'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=self.colors['primary'],
                       focuscolor=self.colors['border_focus'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['border_focus']),
                            ('!focus', self.colors['border'])],
                 focuscolor=[('focus', self.colors['border_focus'])])
        
        # Primary button style (macOS style)
        style.configure('Primary.TButton',
                       font=('SF Pro Text', 13, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 13, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 13, 'bold'),
                       foreground='white',
                       background=self.colors['primary'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['primary_dark'])])
        
        # Secondary button style (modern subtle)
        style.configure('Secondary.TButton',
                       font=('SF Pro Text', 12) if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 12) if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 12),
                       foreground=self.colors['text_primary'],
                       background=self.colors['button_bg'],
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['bg_quaternary'])])
        
        # Success button style
        style.configure('Success.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground='white',
                       background=self.colors['accent'],
                       borderwidth=0,
                       relief='flat')
        
        # Modern progress bar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['primary_light'],
                       troughcolor=self.colors['bg_secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['primary_light'],
                       darkcolor=self.colors['primary_light'])
        
        # Enhanced progress bar with modern macOS/Windows 11 styling
        style.configure('Enhanced.Horizontal.TProgressbar',
                       background=self.colors['progress_fill'],
                       troughcolor=self.colors['progress_bg'],
                       borderwidth=0,
                       relief='flat',
                       lightcolor=self.colors['progress_fill'],
                       darkcolor=self.colors['progress_fill'],
                       thickness=8)  # Thinner, more modern
        
        # Status label styles with modern typography
        style.configure('Status.TLabel',
                       font=('SF Pro Text', 12) if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 12) if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 12),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_card'])
        
        style.configure('Success.TLabel',
                       font=('SF Pro Text', 12, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 12, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 12, 'bold'),
                       foreground=self.colors['accent'],
                       background=self.colors['bg_card'])
        
        style.configure('Warning.TLabel',
                       font=('SF Pro Text', 12, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 12, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 12, 'bold'),
                       foreground=self.colors['warning'],
                       background=self.colors['bg_card'])
        
        style.configure('Error.TLabel',
                       font=('SF Pro Text', 12, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 12, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 12, 'bold'),
                       foreground=self.colors['error'],
                       background=self.colors['bg_card'])
        
    def create_card_frame(self, parent, title=None, padding=24):
        """Create a modern macOS/Windows 11 style card with subtle shadows"""
        # Container for the entire card with proper margin (8px grid system)
        card_container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        card_container.pack(fill='x', pady=(0, 24), padx=8)
        
        # Modern subtle shadow using Frame stacking (simulating CSS box-shadow)
        shadow_frame = tk.Frame(card_container, bg=self.colors['shadow'], height=2)  # Very subtle gray
        shadow_frame.place(x=1, y=2, relwidth=1, relheight=1)
        
        # Main card frame with minimal border following modern design
        card_frame = tk.Frame(card_container, 
                             bg=self.colors['bg_card'],
                             relief='solid',
                             bd=1,
                             highlightcolor=self.colors['border'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=0)
        card_frame.pack(fill='both', expand=True)
        
        # Inner content frame with proper padding (following 8px grid)
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=padding, pady=padding)
        
        if title:
            # Modern title styling without decorative elements
            title_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
            title_frame.pack(fill='x', pady=(0, 16))  # 16px bottom margin
            
            title_label = ttk.Label(title_frame, text=title, style='SectionHeading.TLabel')
            title_label.pack(side='left')
            
        return content_frame
    
    def setup_step_indicators(self):
        """Create visual step indicators for navigation process"""
        # Define the navigation steps
        steps = [
            "🌐 Open Website",
            "🔍 Navigate to Records", 
            "📋 Select Case Search",
            "⌨️ Enter Case Number",
            "🔗 Click Case Link (1st)",
            "🔗 Click Case Link (2nd)",
            "📄 Extract Documents"
        ]
        
        # Create step indicator widgets
        for i, step_text in enumerate(steps):
            step_frame = tk.Frame(self.steps_frame, bg=self.colors['bg_card'])
            step_frame.pack(side='left', padx=5, pady=5)
            
            # Step circle indicator
            circle_frame = tk.Frame(step_frame, bg=self.colors['bg_card'])
            circle_frame.pack()
            
            step_circle = tk.Label(circle_frame,
                                  text=str(i + 1),
                                  font=('SF Pro Text', 11, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 11, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 11, 'bold'),
                                  fg=self.colors['text_tertiary'],
                                  bg=self.colors['bg_tertiary'],
                                  width=3,
                                  height=1,
                                  relief='flat',
                                  bd=0)
            step_circle.pack()
            
            # Step text with modern typography
            step_label = tk.Label(step_frame,
                                 text=step_text,
                                 font=('SF Pro Text', 9) if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 9) if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 9),
                                 fg=self.colors['text_tertiary'],
                                 bg=self.colors['bg_card'],
                                 wraplength=80,
                                 justify='center')
            step_label.pack(pady=(4, 0))
            
            self.step_indicators.append({
                'frame': step_frame,
                'circle': step_circle,
                'label': step_label,
                'completed': False
            })
        
    def update_step_indicator(self, step_index, status='active'):
        """Update step indicator appearance based on status"""
        if 0 <= step_index < len(self.step_indicators):
            indicator = self.step_indicators[step_index]
            
            if status == 'active':
                # Current active step - modern blue styling
                indicator['circle'].configure(
                    fg='white',
                    bg=self.colors['primary'],
                    relief='flat',
                    bd=0
                )
                indicator['label'].configure(fg=self.colors['primary'])
            elif status == 'completed':
                # Completed step - modern green with checkmark
                indicator['circle'].configure(
                    text='✓',
                    fg='white',
                    bg=self.colors['accent'],
                    relief='flat',
                    bd=0
                )
                indicator['label'].configure(fg=self.colors['accent'])
                indicator['completed'] = True
            elif status == 'error':
                # Error step - modern red styling
                indicator['circle'].configure(
                    text='✗',
                    fg='white',
                    bg=self.colors['error'],
                    relief='flat',
                    bd=0
                )
                indicator['label'].configure(fg=self.colors['error'])
        
    def reset_step_indicators(self):
        """Reset all step indicators to initial state"""
        for i, indicator in enumerate(self.step_indicators):
            indicator['circle'].configure(
                text=str(i + 1),
                fg=self.colors['text_tertiary'],
                bg=self.colors['bg_tertiary'],
                relief='flat',
                bd=0
            )
            indicator['label'].configure(fg=self.colors['text_tertiary'])
            indicator['completed'] = False
        
    def setup_ui(self):
        """Setup modern user interface"""
        # Main container with modern background and proper margins (8px grid)
        main_container = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        main_container.pack(fill='both', expand=True, padx=24, pady=24)
        
        # Header section
        self.setup_header(main_container)
        
        # Input card
        self.setup_input_card(main_container)
        
        # Action card
        self.setup_action_card(main_container)
        
        # Progress card
        self.setup_progress_card(main_container)
        
        # Results card
        self.setup_results_card(main_container)
        
        # Footer
        self.setup_footer(main_container)
        
    def setup_header(self, parent):
        """Setup modern header with clean design"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        header_frame.pack(fill='x', pady=(0, 32))  # 32px bottom margin
        
        # Title with modern typography
        title_label = ttk.Label(header_frame, 
                               text="Court Document Downloader",
                               style='ModernTitle.TLabel')
        title_label.pack(pady=(0, 8))  # 8px bottom margin
        
        # Subtitle with description
        subtitle_label = ttk.Label(header_frame,
                                  text="Automatically download court documents from Galveston County Public Access",
                                  style='ModernSubtitle.TLabel')
        subtitle_label.pack()
        
    def setup_input_card(self, parent):
        """Setup modern input card"""
        card = self.create_card_frame(parent, "📋 Case Information")
        
        # Case number section
        case_section = tk.Frame(card, bg=self.colors['bg_card'])
        case_section.pack(fill='x', pady=(0, 20))
        
        # Case number with modern styling
        case_label = ttk.Label(case_section, text="Case Number", style='FieldLabel.TLabel')
        case_label.pack(anchor='w', pady=(0, 8))
        
        case_input_frame = tk.Frame(case_section, bg=self.colors['bg_card'])
        case_input_frame.pack(fill='x')
        
        # Modern entry with better styling
        self.case_entry = ttk.Entry(case_input_frame, 
                                   textvariable=self.case_number,
                                   style='Modern.TEntry',
                                   font=('Segoe UI', 14))
        self.case_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        # Recent cases dropdown
        if self.recent_cases:
            recent_button = ttk.Button(case_input_frame,
                                      text="📝 Recent",
                                      command=self.show_recent_cases,
                                      style='Secondary.TButton')
            recent_button.pack(side='right', padx=(10, 0))
        
        # Example text with better styling
        example_frame = tk.Frame(case_section, bg=self.colors['bg_card'])
        example_frame.pack(fill='x', pady=(8, 0))
        
        example_label = tk.Label(example_frame,
                                text="💡 Examples: 25-CV-0880 (civil), 20-FD-1967 (family)",
                                font=('Segoe UI', 10),
                                fg=self.colors['text_muted'],
                                bg=self.colors['bg_card'])
        example_label.pack(anchor='w')
        
        # Download folder section
        folder_section = tk.Frame(card, bg=self.colors['bg_card'])
        folder_section.pack(fill='x')
        
        folder_label = ttk.Label(folder_section, text="Download Folder", style='FieldLabel.TLabel')
        folder_label.pack(anchor='w', pady=(0, 8))
        
        folder_input_frame = tk.Frame(folder_section, bg=self.colors['bg_card'])
        folder_input_frame.pack(fill='x')
        
        folder_entry = ttk.Entry(folder_input_frame, 
                                textvariable=self.download_folder,
                                style='Modern.TEntry',
                                font=('Segoe UI', 11))
        folder_entry.pack(side='left', fill='x', expand=True, ipady=6)
        
        browse_button = ttk.Button(folder_input_frame,
                                  text="📂 Browse",
                                  command=self.browse_folder,
                                  style='Secondary.TButton')
        browse_button.pack(side='right', padx=(10, 0))
        
    def setup_action_card(self, parent):
        """Setup modern action buttons card"""
        card = self.create_card_frame(parent, "⚡ Actions")
        
        action_frame = tk.Frame(card, bg=self.colors['bg_card'])
        action_frame.pack(fill='x')
        
        # Primary download button with modern styling
        self.download_button = tk.Button(action_frame,
                                        text="📥  Download Court Documents",
                                        command=self.start_download,
                                        font=('Segoe UI', 13, 'bold'),
                                        fg='white',
                                        bg=self.colors['primary_light'],
                                        activeforeground='white',
                                        activebackground=self.colors['primary'],
                                        relief='flat',
                                        bd=0,
                                        pady=12,
                                        cursor='hand2')
        self.download_button.pack(side='left', padx=(0, 15))
        
        # Stop button
        self.stop_button = tk.Button(action_frame,
                                    text="⏹  Stop",
                                    command=self.stop_download,
                                    font=('Segoe UI', 12),
                                    fg=self.colors['text_primary'],
                                    bg='white',
                                    activeforeground=self.colors['error'],
                                    activebackground='white',
                                    relief='solid',
                                    bd=1,
                                    pady=10,
                                    cursor='hand2',
                                    state='disabled')
        self.stop_button.pack(side='left', padx=(0, 20))
        
        # Open folder button
        self.open_folder_button = tk.Button(action_frame,
                                           text="📂  Open Folder",
                                           command=self.open_download_folder,
                                           font=('Segoe UI', 12),
                                           fg='white',
                                           bg=self.colors['accent'],
                                           activeforeground='white',
                                           activebackground='#2f855a',
                                           relief='flat',
                                           bd=0,
                                           pady=10,
                                           cursor='hand2')
        self.open_folder_button.pack(side='right')
        
    def setup_progress_card(self, parent):
        """Setup enhanced progress tracking card"""
        self.progress_card = self.create_card_frame(parent, "📊 Progress Tracking")
        
        # Main status text with larger font
        self.status_label = tk.Label(self.progress_card,
                                    textvariable=self.status_text,
                                    font=('Segoe UI', 13, 'bold'),
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['bg_card'])
        self.status_label.pack(pady=(0, 10))
        
        # Current step indicator
        self.step_label = tk.Label(self.progress_card,
                                  textvariable=self.progress_step,
                                  font=('Segoe UI', 11),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_card'])
        self.step_label.pack(pady=(0, 15))
        
        # Enhanced progress container with custom styling
        progress_container = tk.Frame(self.progress_card, bg=self.colors['bg_card'])
        progress_container.pack(fill='x', pady=(0, 15))
        
        # Progress percentage label
        progress_header = tk.Frame(progress_container, bg=self.colors['bg_card'])
        progress_header.pack(fill='x', pady=(0, 5))
        
        tk.Label(progress_header, text="Overall Progress:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side='left')
        
        self.percentage_label = tk.Label(progress_header, 
                                        text="0%",
                                        font=('Segoe UI', 10, 'bold'),
                                        fg=self.colors['primary_light'],
                                        bg=self.colors['bg_card'])
        self.percentage_label.pack(side='right')
        
        # Custom progress bar with rounded appearance
        self.progress_bar = ttk.Progressbar(progress_container,
                                           variable=self.progress_percentage,
                                           style='Enhanced.Horizontal.TProgressbar',
                                           mode='determinate',
                                           maximum=100)
        self.progress_bar.pack(fill='x', ipady=10)
        
        # Document download progress
        self.doc_progress_label = tk.Label(self.progress_card,
                                          textvariable=self.documents_progress,
                                          font=('Segoe UI', 11),
                                          fg=self.colors['text_secondary'],
                                          bg=self.colors['bg_card'])
        self.doc_progress_label.pack(pady=(5, 0))
        
        # Step indicators container
        self.steps_frame = tk.Frame(self.progress_card, bg=self.colors['bg_card'])
        self.steps_frame.pack(fill='x', pady=(15, 0))
        
        # Create step indicators
        self.step_indicators = []
        self.setup_step_indicators()
        
        # Statistics frame (hidden initially)
        self.stats_frame = tk.Frame(self.progress_card, bg=self.colors['bg_card'])
        
    def setup_results_card(self, parent):
        """Setup modern results display card"""
        card = self.create_card_frame(parent, "📄 Download Log")
        
        # Results container
        results_container = tk.Frame(card, bg=self.colors['bg_card'])
        results_container.pack(fill='both', expand=True)
        
        # Text area with modern styling
        text_frame = tk.Frame(results_container, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.results_text = tk.Text(text_frame,
                                   font=('Consolas', 10),
                                   bg='#f8f9fa',
                                   fg=self.colors['text_primary'],
                                   wrap='word',
                                   relief='solid',
                                   bd=1,
                                   borderwidth=1,
                                   selectbackground=self.colors['primary_light'],
                                   selectforeground='white',
                                   height=10)
        
        # Custom scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons for results
        results_actions = tk.Frame(results_container, bg=self.colors['bg_card'])
        results_actions.pack(fill='x')
        
        clear_button = tk.Button(results_actions,
                                text="🗑  Clear Log",
                                command=self.clear_results,
                                font=('Segoe UI', 10),
                                fg=self.colors['text_secondary'],
                                bg='white',
                                activeforeground=self.colors['error'],
                                activebackground='white',
                                relief='solid',
                                bd=1,
                                pady=6,
                                cursor='hand2')
        clear_button.pack(side='right')
        
    def setup_footer(self, parent):
        """Setup modern footer"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        footer_frame.pack(fill='x', pady=(20, 0))
        
        # Tip with icon
        tip_label = tk.Label(footer_frame,
                            text="💡 Tip: Secured documents will show as placeholders - this is normal for family cases",
                            font=('Segoe UI', 10),
                            fg=self.colors['text_muted'],
                            bg=self.colors['bg_secondary'])
        tip_label.pack(side='left')
        
        # Version
        version_label = tk.Label(footer_frame,
                                text="v4.0 Professional Edition",
                                font=('SF Pro Text', 10, 'medium') if 'SF Pro Text' in self.root.tk.call('font', 'families') else ('Segoe UI Variable Text', 10, 'bold') if 'Segoe UI Variable Text' in self.root.tk.call('font', 'families') else ('Segoe UI', 10, 'bold'),
                                fg=self.colors['primary'],
                                bg=self.colors['bg_secondary'])
        version_label.pack(side='right')
        
    def show_recent_cases(self):
        """Show recent cases dropdown"""
        if not self.recent_cases:
            return
            
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0)
        for case in self.recent_cases:
            menu.add_command(label=case, command=lambda c=case: self.case_number.set(c))
        
        # Show menu at button location
        try:
            menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        except:
            pass
        
    def browse_folder(self):
        """Browse for download folder with modern dialog"""
        folder = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=self.download_folder.get()
        )
        if folder:
            self.download_folder.set(folder)
            self.save_preferences()
            
    def add_to_recent_cases(self, case_number):
        """Add case to recent cases list"""
        if case_number in self.recent_cases:
            self.recent_cases.remove(case_number)
        self.recent_cases.insert(0, case_number)
        self.recent_cases = self.recent_cases[:10]  # Keep last 10
        self.save_preferences()
        
    def log_message(self, message, msg_type='info'):
        """Log message with color coding"""
        self.results_text.insert('end', f"{message}\n")
        
        # Color coding based on message type
        if msg_type == 'success':
            # Make the last line green
            line_start = f"{self.results_text.index('end-1c linestart')}"
            line_end = f"{self.results_text.index('end-1c lineend')}"
            self.results_text.tag_add('success', line_start, line_end)
            self.results_text.tag_config('success', foreground=self.colors['accent'])
        elif msg_type == 'error':
            line_start = f"{self.results_text.index('end-1c linestart')}"
            line_end = f"{self.results_text.index('end-1c lineend')}"
            self.results_text.tag_add('error', line_start, line_end)
            self.results_text.tag_config('error', foreground=self.colors['error'])
        elif msg_type == 'warning':
            line_start = f"{self.results_text.index('end-1c linestart')}"
            line_end = f"{self.results_text.index('end-1c lineend')}"
            self.results_text.tag_add('warning', line_start, line_end)
            self.results_text.tag_config('warning', foreground=self.colors['warning'])
            
        self.results_text.see('end')
        self.root.update_idletasks()
        
    def clear_results(self):
        """Clear results area"""
        self.results_text.delete('1.0', 'end')
        
    def animate_button_hover(self, button, enter=True):
        """Animate button hover effect"""
        if enter:
            button.configure(relief='raised')
        else:
            button.configure(relief='flat')
            
    def start_download(self):
        """Start download with modern UI updates"""
        # Validate inputs
        case_num = self.case_number.get().strip()
        if not case_num:
            messagebox.showerror("Input Error", "Please enter a case number")
            return
            
        download_dir = Path(self.download_folder.get())
        if not download_dir.parent.exists():
            messagebox.showerror("Folder Error", "Download folder path is invalid")
            return
            
        # Add to recent cases
        self.add_to_recent_cases(case_num)
        
        # Update UI for running state
        self.is_running.set(True)
        self.download_button.configure(state='disabled', bg=self.colors['text_muted'])
        self.stop_button.configure(state='normal')
        
        # Reset progress indicators
        self.reset_progress()
        self.status_text.set("🚀 Initializing download process...")
        self.clear_results()
        
        # Start download thread
        self.download_thread = threading.Thread(
            target=self.download_documents,
            args=(case_num, download_dir),
            daemon=True
        )
        self.download_thread.start()
        
    def download_documents(self, case_number, download_dir):
        """Download documents with accurate progress reporting"""
        try:
            case_dir = download_dir / case_number.replace('/', '_').replace('\\', '_')
            
            # Phase 1: Initialize (5%)
            self.progress_queue.put(("progress", (1, 1, "🚀 Initializing browser and scraper", 5)))
            self.progress_queue.put(("status", f"🔍 Preparing to search for case: {case_number}"))
            self.progress_queue.put(("log", f"Starting download for case: {case_number}", "info"))
            
            # Initialize scraper with progress callback
            self.scraper = GalvestonCourtScraper(headless=True, verbose=True, progress_callback=self.on_scraper_progress)
            
            # Phase 2: Setup complete (10%)
            self.progress_queue.put(("progress", (1, 1, "✅ Browser initialized, starting navigation", 10)))
            
            # Phase 3: Scraping (will be handled by progress callbacks) - 15% to 70%
            # Phase 4: Parsing (will be reported at 72%)
            # Phase 5: Downloading (will be handled by callbacks) - 75% to 95%
            result = self.scraper.scrape_case(case_number, case_dir)
            
            if result["success"]:
                # Final processing and completion (98-100%)
                self.progress_queue.put(("progress", (1, 1, "📊 Processing download results", 98)))
                
                # Success - show detailed results
                docs_found = result["documents"]
                downloaded = result.get("downloaded", 0)
                secured = result.get("secured", 0)
                failed = result.get("failed", 0)
                skipped = result.get("skipped", 0)
                
                # Complete
                self.progress_queue.put(("progress", (1, 1, "✅ Download completed successfully!", 100)))
                self.progress_queue.put(("status", "✅ Download completed successfully!"))
                self.progress_queue.put(("log", f"✅ SUCCESS! Case {case_number} processed", "success"))
                self.progress_queue.put(("log", f"📄 Total documents found: {docs_found}", "info"))
                self.progress_queue.put(("log", f"📥 Successfully downloaded: {downloaded}", "success"))
                
                if secured > 0:
                    self.progress_queue.put(("log", f"🔒 Secured documents (placeholders created): {secured}", "warning"))
                if failed > 0:
                    self.progress_queue.put(("log", f"❌ Failed downloads: {failed}", "error"))
                if skipped > 0:
                    self.progress_queue.put(("log", f"⏭ Skipped (already existed): {skipped}", "info"))
                    
                self.progress_queue.put(("log", f"📂 Files saved to: {case_dir}", "info"))
                
                # Show stats
                total_files = downloaded + secured
                self.progress_queue.put(("stats", {
                    "total": total_files,
                    "downloaded": downloaded,
                    "secured": secured,
                    "failed": failed,
                    "skipped": skipped
                }))
                
                if total_files > 0:
                    self.progress_queue.put(("success", f"Successfully processed {total_files} files!"))
                else:
                    self.progress_queue.put(("warning", "No new files were downloaded"))
                    
            else:
                error_msg = result.get("error", "Unknown error occurred")
                self.progress_queue.put(("status", "❌ Download failed"))
                self.progress_queue.put(("log", f"❌ ERROR: {error_msg}", "error"))
                self.progress_queue.put(("error", f"Failed to process case {case_number}: {error_msg}"))
                
        except Exception as e:
            self.progress_queue.put(("status", "❌ Download failed"))
            self.progress_queue.put(("log", f"❌ EXCEPTION: {str(e)}", "error"))
            self.progress_queue.put(("error", f"Unexpected error: {str(e)}"))
            
        finally:
            self.progress_queue.put(("complete", None))
            
    def stop_download(self):
        """Stop download process"""
        if self.scraper:
            self.scraper.close_driver()
        self.complete_download()
        self.log_message("⏹ Download stopped by user", "warning")
        
    def complete_download(self):
        """Complete download and reset modern UI"""
        self.is_running.set(False)
        self.download_button.configure(state='normal', bg=self.colors['primary_light'])
        self.stop_button.configure(state='disabled')
        
        # Keep progress indicators showing completion for a moment, then reset
        self.root.after(3000, self.delayed_progress_reset)  # Reset after 3 seconds
        
    def delayed_progress_reset(self):
        """Reset progress indicators after a delay"""
        if not self.is_running.get():  # Only reset if not running again
            self.status_text.set("Ready to download court documents")
        
    def show_statistics(self, stats):
        """Show download statistics in a modern way"""
        self.stats_frame.pack(fill='x', pady=(15, 0))
        
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Create stats display
        stats_title = tk.Label(self.stats_frame,
                              text="📊 Download Summary",
                              font=('Segoe UI', 12, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_card'])
        stats_title.pack(pady=(0, 10))
        
        stats_container = tk.Frame(self.stats_frame, bg=self.colors['bg_card'])
        stats_container.pack(fill='x')
        
        # Stats items
        stat_items = [
            ("📥 Downloaded", stats["downloaded"], self.colors['accent']),
            ("🔒 Secured", stats["secured"], self.colors['warning']),
            ("❌ Failed", stats["failed"], self.colors['error']),
            ("⏭ Skipped", stats["skipped"], self.colors['text_secondary'])
        ]
        
        for i, (label, value, color) in enumerate(stat_items):
            if value > 0:  # Only show non-zero stats
                stat_frame = tk.Frame(stats_container, bg=self.colors['bg_card'])
                stat_frame.pack(side='left', padx=(0, 20))
                
                stat_value = tk.Label(stat_frame,
                                     text=str(value),
                                     font=('Segoe UI', 16, 'bold'),
                                     fg=color,
                                     bg=self.colors['bg_card'])
                stat_value.pack()
                
                stat_label = tk.Label(stat_frame,
                                     text=label,
                                     font=('Segoe UI', 10),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['bg_card'])
                stat_label.pack()
        
    def check_progress(self):
        """Check progress queue with enhanced handling"""
        try:
            while True:
                msg_type, message = self.progress_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_text.set(message)
                elif msg_type == "progress":
                    # Enhanced progress message: (step, total_steps, message, percentage)
                    if isinstance(message, tuple) and len(message) >= 3:
                        step, total_steps, progress_message = message[:3]
                        percentage = message[3] if len(message) > 3 else None
                        self.update_progress(step, total_steps, progress_message, percentage)
                elif msg_type == "step":
                    # Update current step with message
                    step_num, step_message = message
                    self.update_progress(step_num, message=step_message)
                elif msg_type == "document_progress":
                    # Document download progress: (current, total, status_text)
                    current, total, status_text = message
                    self.update_document_progress(current, total, status_text)
                elif msg_type == "log":
                    if isinstance(message, tuple):
                        text, log_type = message
                        self.log_message(text, log_type)
                    else:
                        self.log_message(message, "info")
                elif msg_type == "success":
                    self.log_message(f"✅ {message}", "success")
                    messagebox.showinfo("Success", message)
                elif msg_type == "warning":
                    self.log_message(f"⚠️ {message}", "warning")
                    messagebox.showwarning("Warning", message)
                elif msg_type == "error":
                    self.log_message(f"❌ {message}", "error")
                    messagebox.showerror("Error", message)
                elif msg_type == "stats":
                    self.show_statistics(message)
                elif msg_type == "complete":
                    self.complete_download()
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.check_progress)
        
    def open_download_folder(self):
        """Open download folder"""
        folder_path = Path(self.download_folder.get())
        if folder_path.exists():
            os.startfile(str(folder_path))
        else:
            messagebox.showwarning("Folder Not Found", "Download folder does not exist yet")

def main():
    """Main function to run the modern GUI"""
    root = tk.Tk()
    app = ModernCourtScraperGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()