# Build Instructions

## Creating Standalone Executables

You can create standalone executables using PyInstaller for easy distribution.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build Commands

**Windows:**
```cmd
pyinstaller --onefile --windowed --name "TypingRacer" main.py
```

**macOS:**
```bash
pyinstaller --onefile --windowed --name "TypingRacer" main.py
```

**Linux:**
```bash
pyinstaller --onefile --name "TypingRacer" main.py
```

### Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Hides console window (Windows/macOS)
- `--name`: Sets the executable name
- `main.py`: Entry point script

### Advanced Options

For smaller file sizes:
```bash
pyinstaller --onefile --windowed --strip --name "TypingRacer" main.py
```

To include additional data files:
```bash
pyinstaller --onefile --windowed --add-data "data:data" --name "TypingRacer" main.py
```

### Output

The executable will be created in the `dist/` directory.

### Distribution Notes

- Windows: `.exe` file can run on Windows 7+ (32/64-bit)
- macOS: `.app` bundle for macOS 10.13+ 
- Linux: Binary executable for most distributions

### Troubleshooting

If you encounter issues:

1. **Missing modules**: Add `--hidden-import module_name`
2. **Large file size**: Use `--exclude-module` for unused packages
3. **Antivirus detection**: Code-sign the executable or add to whitelist

### Testing

Always test the executable on clean systems without Python installed to ensure all dependencies are properly bundled.