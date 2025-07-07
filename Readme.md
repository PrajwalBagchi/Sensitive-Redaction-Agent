# 🔒 Sensitive Information Redactor Agent

A command-line Python application that redacts sensitive information (like names, emails, phone numbers, and URLs) from `.pdf`, `.txt`, `.png`, and `.jpg` files using **LangChain** with **Gemini 1.5 Flash** and **OCR via Tesseract**.

---

## 📌 Features

- ✅ Redacts emails, phone numbers, names, and URLs
- ✅ Supports input formats: `.pdf`, `.txt`, `.png`, `.jpg`, `.jpeg`
- ✅ Uses Google Gemini 1.5 Flash via LangChain
- ✅ OCR support for images using Tesseract and OpenCV
- ✅ Modular agent architecture (Runner, Redactor, Coordinator)

---

## ⚙️ How It Works

1. **RunnerAgent** loads the file and extracts text
2. **RedactorAgent** sends the text to Gemini Flash for sensitive data detection
3. Identified items are replaced with `[REDACTED_TYPE]` tags
4. A redacted `.txt` output is saved to disk

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PrajwalBagchi/sensitive-info-redactor.git
cd sensitive-info-redactor
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Install Tesseract OCR

```bash
Windows: Download Tesseract and add it to your PATH
Example path: C:\Program Files\Tesseract-OCR\tesseract.exe
```
### Linux/macOS:

```bash
sudo apt install tesseract-ocr    # Ubuntu
brew install tesseract            # macOS
```
### 4. Add Your API Key
Create a .env file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```
### 📄 Example Input
letter.txt

```kotlin
Hi, my name is John Doe.
Contact me at john@example.com or +1-123-456-7890.
Visit https://example.com for more.
```
### 📤 Usage
```python main.py

Then input the file path:
```
```java
Enter file path (.txt, .pdf, .jpg, .png): letter.txt
```
### 📁 Output
For letter.txt, the output will be saved as:

```bash
txt
Hi, my name is [REDACTED_NAME].
Contact me at [REDACTED_EMAIL] or [REDACTED_PHONE].
Visit [REDACTED_URL] for more.
```
### 🧠 Powered By
LangChain

Google Gemini 1.5 Flash

Tesseract OCR

OpenCV

PyPDF2

### 📜 License
MIT License

### 👨‍💻 Author
Prajwal Bagchi — @PrajwalBagchi

Feel free to contribute or open an issue.
