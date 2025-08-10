# Court Document Downloader - User Guide

## For Legal Professionals, Secretaries, and Office Staff

This application automatically downloads court documents from Galveston County Public Access system with a simple, user-friendly interface.

## 🚀 Quick Start

### Option 1: Double-click the launcher
1. Double-click `launch_gui.bat`
2. The application will open automatically

### Option 2: Run directly (if you have Python installed)
1. Double-click `court_scraper_gui.py`
2. Or open command prompt and run: `python court_scraper_gui.py`

## 📋 How to Use

### Step 1: Enter Case Information
- **Case Number**: Enter the case number (e.g., `25-CV-0880` or `20-FD-1967`)
- **Download Folder**: Choose where to save documents (default: `downloads` folder)

### Step 2: Download Documents
1. Click the **"📥 Download Court Documents"** button
2. Wait for the process to complete
3. View progress and results in the log area

### Step 3: Access Your Files
- Click **"📂 Open Download Folder"** to see downloaded documents
- Documents are organized by case number in separate folders

## 📄 Understanding Results

### File Types You'll See:
- **Regular Documents**: Full-size PDF files (court documents)
- **Placeholder Documents**: Small PDF files (~1KB) for secured/sealed documents

### Status Messages:
- ✅ **Success**: Document downloaded successfully  
- 🔒 **Secured**: Document is protected/sealed (placeholder created)
- ❌ **Failed**: Document could not be downloaded
- ⏭ **Skipped**: Document already exists (not re-downloaded)

## 🔒 Secured/Sealed Documents

Some court documents are protected by law (especially in family cases). When this happens:
- The program will create a **placeholder PDF** file
- The placeholder shows the document name and explains it's secured
- This is normal and expected for sensitive documents

## 💡 Tips for Success

### Case Number Format:
- **Civil Cases**: `25-CV-0880`, `24-CV-1234`
- **Family Cases**: `20-FD-1967`, `21-FD-5678`
- **Other Types**: Follow the same pattern `YY-TYPE-NUMBER`

### Best Practices:
- Run one case at a time for best results
- Choose a dedicated folder for court documents
- Check the log messages to understand what happened
- Be patient - some cases have hundreds of documents

## 🛠 Troubleshooting

### Common Issues:

**"Case not found"**
- Check the case number format
- Verify the case exists in Galveston County system
- Contact IT support if the problem persists

**"No documents downloaded"**
- Case may exist but have no available documents
- Documents may all be secured/sealed
- Check the log for specific error messages

**"Download folder error"**
- Make sure the folder path exists
- Choose a different location if needed
- Ensure you have write permissions to the folder

### Getting Help:
- Read the detailed log messages in the Results area
- Take a screenshot of any error messages
- Contact your IT support if technical issues persist

## 📁 File Organization

Downloaded documents are organized like this:
```
downloads/
├── 25-CV-0880/
│   ├── 2025.05.22_Original Petition.pdf
│   ├── 2025.05.23_Status Conference.pdf
│   └── MANIFEST.txt
└── 20-FD-1967/
    ├── 2020.09.25_Original Petition for Divorce.pdf (placeholder)
    ├── 2020.09.25_Status Conference Sheet.pdf
    └── MANIFEST.txt
```

Each case gets its own folder with:
- All downloaded documents
- A `MANIFEST.txt` file listing all files and their sizes

## ⚡ Features

- **Automatic Navigation**: No manual clicking required
- **Smart File Naming**: Documents named with dates and descriptions  
- **Secured Document Handling**: Creates placeholders for protected files
- **Progress Tracking**: Real-time status updates
- **Error Recovery**: Automatically retries failed downloads
- **Duplicate Prevention**: Won't re-download existing files

---

*This application is designed to be simple and reliable for daily use in legal offices.*