import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    # Read and encode image to base64
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # Initialize the DIAL client
    client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT
    )

    # Create a message with base64 image
    msg_base64 = ContentedMessage(
        role=Role.USER,
        content=[ImgContent(src=f"data:image/png;base64,{base64_image}", description="DialX Banner")]
    )

    # Send the request and print the result
    response_base64 = client.chat_completion(messages=[msg_base64])
    print("Response for base64 image:\n", response_base64)

    # Create a message with image URL
    msg_url = ContentedMessage(
        role=Role.USER,
        content=[ImgUrl(src="https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg", description="Elephant")]
    )

    # Send the request and print the result
    response_url = client.chat_completion(messages=[msg_url])
    print("\nResponse for image URL:\n", response_url)


if __name__ == "__main__":
    start()
