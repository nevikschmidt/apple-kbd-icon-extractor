
# MacOS Keyboard Input/Layout Icon Extractor

This project provides a script for extracting `.icns` icons from macOS keyboard layout `.dat` files. It is an enhanced version of the original script by [Philip Belemezov](https://github.com/phible), updated for Python 3 compatibility and improved usability.

---

## **Features**
- **Python 3 Compatibility:** Fully updated to work with Python 3.
- **Enhanced Error Handling:** Safeguards against empty files, malformed data, and permission issues.
- **Progress Bar:** Added a visual progress bar using `tqdm` for large files.
- **Dynamic Logging Levels:** Choose between `DEBUG`, `INFO`, `WARNING`, or `ERROR` for detailed control over output.
- **Automatic Output Directory Creation:** The script creates the specified output directory if it doesn’t already exist.
- **Modular Design:** Clean and testable code structure for future enhancements.

---

## **Usage**

### **Basic Command**
Extract icons from the default macOS `.dat` file:
```bash
python3 apple-kbd-dat-icon-extract.py -o icons
```

### **Specify a Custom DAT File**
To extract icons from a specific `.dat` file:
```bash
python3 apple-kbd-dat-icon-extract.py /path/to/DAT-file.dat -o icons
```

### **Set a Custom Logging Level**
For detailed debugging output:
```bash
python3 apple-kbd-dat-icon-extract.py -o icons --loglevel DEBUG
```

---

## **Installation**

### **Clone the Repository**
```bash
git clone https://github.com/nivekschmidt/apple-kbd-icon-extractor.git
cd apple-kbd-icon-extractor
```

### **Install Dependencies**
The script uses the `tqdm` library for the progress bar. Install it using pip:
```bash
pip install tqdm
```

### **Run the Script**
Execute the script as described in the [Usage](#usage) section.

---

## **License**
This script is released under the public domain, as per the original author's license.

---

## **Credits**
- Original script by [Philip Belemezov](https://github.com/phible)
- Updated and enhanced by [Nevik Schmidt](https://github.com/nevikkschmidt)

---

## **Contributions**
Contributions are welcome! If you have ideas for further improvements or find a bug, feel free to:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

Let's make this project even better together!
