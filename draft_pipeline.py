from doc_scraper import extract_first_table_as_dict
from screenshoter import get_screenshot
from parser_llm_agent import extract_name_and_price_from_images
from doc_llm_agent import compile_images_and_text_to_doc
from PIL import Image

def process_document_pipeline(doc_path):
    # Step 1: Scrape the first table from the document
    scraped_data = extract_first_table_as_dict(doc_path)

    # Step 2: Take screenshots of links present in the scraped dictionaries
    pil_images = []
    for data in scraped_data:
        link = data.get("Link")
        if link:
            screenshot = get_screenshot(link)
            pil_images.append(screenshot)

    # Step 3: Extract Name and Price from the images
    extracted_data = extract_name_and_price_from_images(pil_images)

    # Step 4: Mix each dictionary with extracted Name and Price
    final_data = []
    for original_data, extracted_info in zip(scraped_data, extracted_data):
        mixed_data = {
            "Name": extracted_info.get("Name", "NONE"),
            "Price": extracted_info.get("Price", "NONE"),
            "Quantity": original_data.get("Quantity", "NONE")
        }
        final_data.append(mixed_data)

    # Step 5: Compile the images and final data into a document
    compiled_doc_path = "compiled_output_with_images.docx"
    compile_images_and_text_to_doc(pil_images, final_data)

    return pil_images, final_data, compiled_doc_path

# Example usage
if __name__ == "__main__":
    doc_path = "sample.docx"  # Path to the uploaded document
    images, dictionaries, compiled_doc = process_document_pipeline(doc_path)
    print("Processed Images:", images)
    print("Processed Data:", dictionaries)
    print("Compiled Document Path:", compiled_doc)