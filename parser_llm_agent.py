from gradio_client import Client, handle_file
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain_groq import ChatGroq
import re
import ast
from dotenv import load_dotenv
from PIL import Image
import os
import tempfile

load_dotenv()

def ocr_tool(image_path: str) -> str:
    try:
        client = Client("IotaCluster/OCR")
        # Accept both local file paths and URLs
        image_input = image_path
        if not (image_path.startswith('http://') or image_path.startswith('https://')):
            # Convert PIL image object to a temporary file for compatibility
            if isinstance(image_path, Image.Image):
                # Save PIL image to a temporary file
                temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                image_path.save(temp_file.name, format="PNG")
                temp_file.close()
                image_input = temp_file.name
                print(f"🔍 Processing: {image_input}")
            else:
                image_input = handle_file(image_path)
        else:
            image_input = handle_file(image_path)  # handle_file also works with URLs
        print("Image path or input for OCR:", image_input)  # Debugging image input
        result = client.predict(
            image=image_input,
            language=["eng"],
            api_name="/predict"
        )
        return str(result)
    except Exception as e:
        return f"OCR failed: {str(e)}"

def extract_name_and_price_from_image(image):
    # Process the image outside the tool, similar to doc_llm_agent
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image.save(temp_file.name, format="PNG")
    temp_file.close()
    image_input = temp_file.name
    print(f"🔍 Processing: {image_input}")

    ocr_text = agent.run(f"Use ImageOCR to extract text from image: {image_input}")
    print("OCR Text:", ocr_text)  # Debugging OCR output

    prompt = (
        f"You are a helpful AI. Here is some OCR text extracted from an image:\n{ocr_text}\n\n"
        f"Your task is to extract the Name and Price from the text. Generalize the Name to make it more small if possible. If no Name or Price is found, return NONE for each."
        f" Return the result as a raw list of Python dictionaries with keys 'Name' and 'Price'."
    )

    llm_response = agent.run(prompt)

    # Extract the dictionary from the LLM output using regex
    dict_match = re.search(r'\{[^\{\}]*\}', llm_response, re.DOTALL)
    if dict_match:
        dict_str = dict_match.group(0)
        try:
            result_dict = ast.literal_eval(dict_str)
        except Exception:
            result_dict = {"Name": "NONE", "Price": "NONE"}
    else:
        result_dict = {"Name": "NONE", "Price": "NONE"}

    return result_dict

def extract_name_and_price_from_images(image_list):
    results = []
    
    # Initialize the agent locally
    ocr_tool_instance = Tool(
        name="ImageOCR",
        func=ocr_tool,
        description="Extracts text content from an image using OCR via Gradio"
    )

    llm = ChatGroq(temperature=0, model_name="qwen/qwen3-32b")
    agent = initialize_agent(
        tools=[ocr_tool_instance],
        llm=llm,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5  # Reduce iterations to prevent infinite loops
    )

    for image in image_list:
        # Process each image
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        image.save(temp_file.name, format="PNG")
        temp_file.close()
        image_input = temp_file.name
        print(f"🔍 Processing: {image_input}")

        ocr_text = agent.run(f"Use ocr tool to extract text from image: {image_input}")
        print("OCR Text:", ocr_text)  # Debugging OCR output

        prompt = (
            f"You are a helpful AI. Here is some OCR text extracted from an image:\n{ocr_text}\n\n"
            f"Your task is to extract the Name and Price from the text. Generalize the Name to make it more small if possible. If no Name or Price is found, return NONE for each."
            f" Return the result as a raw list of Python dictionaries with keys 'Name' and 'Price'."
        )

        llm_response = agent.run(prompt)

        # Extract the dictionary from the LLM output using regex
        dict_match = re.search(r'\{[^\{\}]*\}', llm_response, re.DOTALL)
        if dict_match:
            dict_str = dict_match.group(0)
            try:
                result_dict = ast.literal_eval(dict_str)
            except Exception:
                result_dict = {"Name": "NONE", "Price": "NONE"}
        else:
            result_dict = {"Name": "NONE", "Price": "NONE"}

        results.append(result_dict)

    return results

# Example usage
if __name__ == "__main__":
    from PIL import Image
    image_list = [Image.open("4090.png"), Image.open("eg_img.png"), Image.open("5080.png")]
    result = extract_name_and_price_from_images(image_list)
    print(result)
