#!/usr/bin/python3
from gradio_client import Client
from PIL import Image
import io
import base64

def get_screenshot(url):
    try:
        # Connect to the Gradio HF Space
        client = Client("IotaCluster/ScreenShot")
        result = client.predict(
            url=url,
            api_name="/predict"
        )

        # If result is a base64-encoded image or image path
        if isinstance(result, str):
            if result.startswith("data:image"):
                # Base64 encoded image
                base64_image = result.split(',', maxsplit=1)[1]
                image_data = base64.b64decode(base64_image)
            elif result.endswith(".png") or result.endswith(".jpg"):
                # Image path returned
                image_data = requests.get(result).content
            else:
                print("Unexpected image format.")
                return None

            image = Image.open(io.BytesIO(image_data))
            return image
        else:
            print("Unexpected result type:", type(result))
            return None

    except Exception as e:
        print(f"Error occurred while getting screenshot: {e}")
        return None


def main():
    url = "https://robu.in/product/1-channel-isolated-5v-relay-module-opto-coupler-for-arduino-pic-avr-dsp-arm/"
    image = get_screenshot(url)

    if image:
        image.save("gradio_screenshot.png")
        image.show()
        print("Screenshot saved and displayed.")
    else:
        print("Screenshot could not be retrieved.")


main()
