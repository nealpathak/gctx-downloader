# Installation Guide for IT Administrators

## Setting Up the Court Document Downloader

### System Requirements
- Windows 10 or newer
- Python 3.8 or newer
- Chrome browser (installed automatically with most Windows systems)
- Internet connection

### Installation Steps

#### Step 1: Install Python (if not already installed)
1. Download Python from https://python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Complete the installation

#### Step 2: Install Required Packages
Open Command Prompt as Administrator and run:
```bash
pip install selenium requests beautifulsoup4 lxml
```

#### Step 3: Set Up the Application
1. Copy the entire `gctx-downloader` folder to a location accessible by users
2. Recommended location: `C:\Program Files\Court Document Downloader\`
3. Ensure all users have read access to the folder

#### Step 4: Create Desktop Shortcuts (Optional)
1. Right-click on `launch_gui.bat`
2. Select "Create shortcut"
3. Move shortcut to user desktops
4. Rename to "Court Document Downloader"

### User Training
- Provide users with `GUI_README.md`
- Show them how to enter case numbers correctly
- Explain the difference between regular and secured documents
- Demonstrate opening the download folder

### Troubleshooting for IT

#### Common Installation Issues:

**"Python is not recognized"**
- Python not added to PATH during installation
- Reinstall Python with "Add to PATH" checked

**"pip is not recognized"**
- Same as above - Python PATH issue
- Or pip not installed with Python (rare)

**"Chrome not found" errors**
- Chrome browser not installed
- Install Google Chrome from google.com/chrome

**Permission errors**
- Users don't have write access to download folder
- Set appropriate folder permissions
- Or guide users to choose a folder in their Documents

#### Browser Driver Updates:
- The application automatically manages Chrome drivers
- No manual driver installation needed
- If Chrome updates cause issues, update the application

### Network Considerations
- Application needs access to: `publicaccess.galvestoncountytx.gov`
- Standard HTTPS traffic on ports 80/443
- No special firewall rules needed

### Maintenance
- Check for application updates periodically
- Monitor user download folders for disk space
- Clear old downloads if needed (users should archive important files)

### Security Notes
- Application only accesses public court records
- No sensitive credentials are stored
- All downloads are from official court website
- Browser runs in secure, sandboxed mode

---

*For technical support, contact your system administrator or the application developer.*