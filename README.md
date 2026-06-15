# Automated Documentation Generator

A web-based tool that automatically generates structured technical documentation from a codebase or a circuit schematic image, powered by the Claude API.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Claude API](https://img.shields.io/badge/Claude-API-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

Writing documentation is one of the most time-consuming parts of any engineering project. This tool takes either a zipped codebase or an image of a circuit schematic and generates clean, structured Markdown documentation — covering project overview, architecture, file breakdowns, setup instructions, and suggested inline comments for code, or component lists, signal flow, and working principles for schematics.

---

## Features

- Upload a `.zip` codebase and receive a full technical documentation report
- Upload a circuit schematic image and get a structured component-level breakdown
- Real-time streaming output using Server-Sent Events (SSE)
- Markdown rendering of generated documentation directly in the browser
- One-click download of the generated documentation as a `.md` file
- Clean, minimal, dark-themed UI with no branding or distractions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Engine | Anthropic Claude API (text and vision) |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Streaming | Server-Sent Events (SSE) |
| Markdown Rendering | marked.js |

---

## How It Works

1. User uploads either a `.zip` file (codebase) or an image (circuit schematic)
2. Backend extracts and parses the codebase, or encodes the image for vision input
3. The parsed content is sent to Claude with a structured prompt tailored to the input type
4. Claude streams the generated documentation back to the frontend in real time
5. User can view the rendered documentation and download it as a file

---

## Project Structure

```
auto-doc-generator/
├── app.py
├── claude_service.py
├── file_processor.py
├── requirements.txt
├── .env
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

---

## Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/your-link.git
   cd auto-doc-generator
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Anthropic API key to a `.env` file
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser

---

## Usage

- **Codebase:** upload a `.zip` file containing your project's source code
- **Circuit:** upload a `.png`, `.jpg`, or `.webp` image of the schematic
- Click **Generate Documentation** and view the streamed output
- Download the result as a `.md` file for use in your repository or report

---

## Future Enhancements

- Support for multi-image schematic uploads
- PDF export of generated documentation
- Inline code annotation directly within source files
- Support for larger codebases via chunked processing

---

## Author

**Mehul Pramanik**
GitHub: [Mehul-8](https://github.com/Mehul-8)
LinkedIn: [mehul-pramanik8](https://linkedin.com/in/mehul-pramanik8)
