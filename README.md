# NeuralDrafter

NeuralDrafter is a Python tool that automates the extraction of text from images using OCR and compiles the results into a formatted Word document, matching extracted text to the most relevant product entries.

## Features
- **OCR Extraction**: Uses a Gradio-based multimodal OCR model to extract text from images.
- **LLM Matching**: Utilizes a language model to match OCR text to the best-fitting dictionary from a list of product entries.
- **Word Document Generation**: Automatically creates a Word document with images, matched data tables, and formatting.

## Requirements
- Python 3.8+
- [Gradio Client](https://pypi.org/project/gradio-client/)
- [python-docx](https://pypi.org/project/python-docx/)
- [langchain](https://pypi.org/project/langchain/)
- [langchain_groq](https://pypi.org/project/langchain-groq/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup
1. **Clone the repository** and navigate to the project folder.
2. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv dawker_env
   .\dawker_env\Scripts\Activate.ps1
   ```
3. **Install dependencies**:
   ```powershell
   pip install gradio_client python-docx langchain langchain_groq python-dotenv
   ```
4. **Add your .env file** if required for API keys or environment variables.

## Usage
1. Place your images (e.g., `4090.png`, `5080.png`) in the project directory.
2. Edit the `image_paths` and `text_objects` in `llm_agent.py` as needed.
3. Run the script:
   ```powershell
   python llm_agent.py
   ```
4. The output Word document (`output.docx`) will be generated in the project directory, containing the images and matched data tables.

## Example
```
image_paths = ["4090.png", "5080.png"]
text_objects = [
    {"Name": "RTX 5080 GPU", "Cost": "126999", "Quantity": 3},
    {"Name": "RTX 4090", "Cost": "292999", "Quantity": 5}
]
compile_images_and_text_to_doc(image_paths, text_objects)
```

## File Structure
- `llm_agent.py` — Main script for OCR, LLM matching, and document creation
- `output.docx` — Generated Word document
- `*.png` — Example image files
- `dawker_env/` — (Optional) Python virtual environment

## License
MIT License
