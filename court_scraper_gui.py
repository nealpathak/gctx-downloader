#!/usr/bin/env python3
"""
Galveston County Court Document Scraper - GUI Version
Modern, user-friendly interface for legal professionals
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import os
import webbrowser
from pathlib import Path
from court_scraper import GalvestonCourtScraper

class CourtScraperGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.setup_ui()
        self.scraper = None
        self.progress_queue = queue.Queue()
        self.check_progress()
        
    def setup_window(self):
        """Setup main window"""
        self.root.title("Galveston County Court Document Downloader")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Set window icon and styling
        self.root.configure(bg='#f8f9fa')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"800x650+{x}+{y}")
        
    def setup_variables(self):
        """Setup tkinter variables"""
        self.case_number = tk.StringVar(value="25-CV-0880")
        self.download_folder = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.show_browser = tk.BooleanVar(value=False)  # Always headless
        self.is_running = tk.BooleanVar(value=False)
        
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        
        # Configure styles for modern look
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground='#2c3e50',
                       background='#f8f9fa')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground='#7f8c8d',
                       background='#f8f9fa')
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       foreground='#34495e',
                       background='#f8f9fa')
        
        style.configure('Modern.TFrame',
                       background='#ffffff',
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Action.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground='white',
                       background='#3498db')
        
        style.map('Action.TButton',
                 background=[('active', '#2980b9')])
        
        style.configure('Success.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#27ae60',
                       background='#ffffff')
        
        style.configure('Warning.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#f39c12',
                       background='#ffffff')
        
        style.configure('Error.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#e74c3c',
                       background='#ffffff')
        
    def setup_ui(self):
        """Setup user interface"""
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.setup_header(main_container)
        
        # Input section
        self.setup_input_section(main_container)
        
        # Options section  
        self.setup_options_section(main_container)
        
        # Action section
        self.setup_action_section(main_container)
        
        # Progress section
        self.setup_progress_section(main_container)
        
        # Results section
        self.setup_results_section(main_container)
        
        # Footer
        self.setup_footer(main_container)
        
    def setup_header(self, parent):
        """Setup header with title and description"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="Court Document Downloader",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Automatically download court documents from Galveston County Public Access",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
        
    def setup_input_section(self, parent):
        """Setup case number input section"""
        input_frame = ttk.LabelFrame(parent, text="Case Information", padding=20)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Case number row
        case_row = ttk.Frame(input_frame)
        case_row.pack(fill='x', pady=(0, 15))
        
        ttk.Label(case_row, text="Case Number:", style='Heading.TLabel').pack(side='left')
        
        case_entry = ttk.Entry(case_row, textvariable=self.case_number, 
                              font=('Segoe UI', 11), width=20)
        case_entry.pack(side='left', padx=(10, 20))
        
        # Example text
        example_label = ttk.Label(case_row, 
                                 text="Examples: 25-CV-0880, 20-FD-1967",
                                 foreground='#7f8c8d',
                                 background='#ffffff')
        example_label.pack(side='left')
        
        # Download folder row
        folder_row = ttk.Frame(input_frame)
        folder_row.pack(fill='x')
        
        ttk.Label(folder_row, text="Download Folder:", style='Heading.TLabel').pack(side='left')
        
        folder_entry = ttk.Entry(folder_row, textvariable=self.download_folder,
                                font=('Segoe UI', 10), width=50)
        folder_entry.pack(side='left', padx=(10, 10), fill='x', expand=True)
        
        browse_button = ttk.Button(folder_row, text="Browse...",
                                  command=self.browse_folder)
        browse_button.pack(side='right')
        
    def setup_options_section(self, parent):
        """Setup options section - simplified"""
        # Options section removed for simplicity
        # Browser always runs hidden for better user experience
        pass
        
    def setup_action_section(self, parent):
        """Setup action buttons"""
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill='x', pady=(0, 20))
        
        # Download button
        self.download_button = ttk.Button(action_frame,
                                         text="📥 Download Court Documents",
                                         command=self.start_download,
                                         style='Action.TButton')
        self.download_button.pack(side='left', padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(action_frame,
                                     text="⏹ Stop Download",
                                     command=self.stop_download,
                                     state='disabled')
        self.stop_button.pack(side='left', padx=(0, 20))
        
        # Open folder button
        self.open_folder_button = ttk.Button(action_frame,
                                            text="📂 Open Download Folder",
                                            command=self.open_download_folder)
        self.open_folder_button.pack(side='right')
        
    def setup_progress_section(self, parent):
        """Setup progress tracking"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding=20)
        progress_frame.pack(fill='x', pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var,
                                           mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(progress_frame,
                                     text="Ready to download documents",
                                     font=('Segoe UI', 10))
        self.status_label.pack()
        
    def setup_results_section(self, parent):
        """Setup results display"""
        results_frame = ttk.LabelFrame(parent, text="Results", padding=20)
        results_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Results text area with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.results_text = tk.Text(text_frame, 
                                   font=('Consolas', 9),
                                   bg='#f8f9fa',
                                   fg='#2c3e50',
                                   wrap='word',
                                   height=8)
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Clear button
        clear_button = ttk.Button(results_frame,
                                 text="Clear Log",
                                 command=self.clear_results)
        clear_button.pack(anchor='e', pady=(10, 0))
        
    def setup_footer(self, parent):
        """Setup footer with help information"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill='x')
        
        help_label = ttk.Label(footer_frame,
                              text="💡 Tip: Some documents may be secured/sealed and will show as placeholders",
                              font=('Segoe UI', 9),
                              foreground='#7f8c8d',
                              background='#ffffff')
        help_label.pack(side='left')
        
        version_label = ttk.Label(footer_frame,
                                 text="v2.0",
                                 font=('Segoe UI', 9),
                                 foreground='#7f8c8d',
                                 background='#ffffff')
        version_label.pack(side='right')
        
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_folder.get())
        if folder:
            self.download_folder.set(folder)
            
    def log_message(self, message, msg_type='info'):
        """Log message to results area"""
        self.results_text.insert('end', f"{message}\n")
        self.results_text.see('end')
        self.root.update_idletasks()
        
    def clear_results(self):
        """Clear results area"""
        self.results_text.delete('1.0', 'end')
        
    def start_download(self):
        """Start the download process"""
        # Validate inputs
        case_num = self.case_number.get().strip()
        if not case_num:
            messagebox.showerror("Error", "Please enter a case number")
            return
            
        download_dir = Path(self.download_folder.get())
        if not download_dir.parent.exists():
            messagebox.showerror("Error", "Download folder path is invalid")
            return
            
        # Update UI for running state
        self.is_running.set(True)
        self.download_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.progress_bar.configure(mode='indeterminate')
        self.progress_bar.start()
        
        self.status_label.configure(text="Starting download...")
        self.clear_results()
        
        # Start download in separate thread
        self.download_thread = threading.Thread(
            target=self.download_documents,
            args=(case_num, download_dir),
            daemon=True
        )
        self.download_thread.start()
        
    def download_documents(self, case_number, download_dir):
        """Download documents in background thread"""
        try:
            # Create case-specific download directory
            case_dir = download_dir / case_number.replace('/', '_').replace('\\', '_')
            
            self.progress_queue.put(("status", f"Processing case: {case_number}"))
            self.progress_queue.put(("log", f"🔍 Searching for case: {case_number}"))
            
            # Initialize scraper
            self.scraper = GalvestonCourtScraper(
                headless=not self.show_browser.get(),
                verbose=True
            )
            
            # Run scraper
            result = self.scraper.scrape_case(case_number, case_dir)
            
            if result["success"]:
                # Success - show results
                docs_found = result["documents"]
                downloaded = result.get("downloaded", 0)
                secured = result.get("secured", 0)
                failed = result.get("failed", 0)
                skipped = result.get("skipped", 0)
                
                self.progress_queue.put(("status", "Download completed successfully!"))
                self.progress_queue.put(("log", f"✅ SUCCESS! Case {case_number} processed"))
                self.progress_queue.put(("log", f"📄 Documents found: {docs_found}"))
                self.progress_queue.put(("log", f"📥 Successfully downloaded: {downloaded}"))
                
                if secured > 0:
                    self.progress_queue.put(("log", f"🔒 Secured documents (placeholders): {secured}"))
                if failed > 0:
                    self.progress_queue.put(("log", f"❌ Failed downloads: {failed}"))
                if skipped > 0:
                    self.progress_queue.put(("log", f"⏭ Skipped (existing): {skipped}"))
                    
                self.progress_queue.put(("log", f"📂 Files saved to: {case_dir}"))
                
                # Show completion message
                total_files = downloaded + secured
                if total_files > 0:
                    self.progress_queue.put(("success", f"Downloaded {total_files} files ({downloaded} regular, {secured} secured)"))
                else:
                    self.progress_queue.put(("warning", "No new files were downloaded"))
                    
            else:
                # Failed
                error_msg = result.get("error", "Unknown error occurred")
                self.progress_queue.put(("status", "Download failed"))
                self.progress_queue.put(("log", f"❌ ERROR: {error_msg}"))
                self.progress_queue.put(("error", f"Failed to process case {case_number}"))
                
        except Exception as e:
            self.progress_queue.put(("status", "Download failed"))
            self.progress_queue.put(("log", f"❌ EXCEPTION: {str(e)}"))
            self.progress_queue.put(("error", f"Unexpected error: {str(e)}"))
            
        finally:
            self.progress_queue.put(("complete", None))
            
    def stop_download(self):
        """Stop the download process"""
        if self.scraper:
            self.scraper.close_driver()
        self.complete_download()
        self.log_message("⏹ Download stopped by user")
        
    def complete_download(self):
        """Complete download and reset UI"""
        self.is_running.set(False)
        self.download_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.progress_bar.stop()
        self.progress_bar.configure(mode='determinate', value=0)
        self.status_label.configure(text="Ready to download documents")
        
    def check_progress(self):
        """Check progress queue for updates"""
        try:
            while True:
                msg_type, message = self.progress_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.configure(text=message)
                elif msg_type == "log":
                    self.log_message(message)
                elif msg_type == "success":
                    self.log_message(f"✅ {message}")
                    messagebox.showinfo("Success", message)
                elif msg_type == "warning":
                    self.log_message(f"⚠️ {message}")
                    messagebox.showwarning("Warning", message)
                elif msg_type == "error":
                    self.log_message(f"❌ {message}")
                    messagebox.showerror("Error", message)
                elif msg_type == "complete":
                    self.complete_download()
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.check_progress)
        
    def open_download_folder(self):
        """Open the download folder in file explorer"""
        folder_path = Path(self.download_folder.get())
        if folder_path.exists():
            os.startfile(str(folder_path))
        else:
            messagebox.showwarning("Warning", "Download folder does not exist yet")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = CourtScraperGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()