import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    # Initialize bucket client
    bucket_client = DialBucketClient(api_key=API_KEY, base_url=DIAL_URL)

    # Read image bytes
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # Upload image to DIAL bucket
    file_io = BytesIO(image_bytes)
    upload_response = await bucket_client.upload_file(file_name=file_name, file_bytes=file_io.read(), mime_type=mime_type_png)

    # Build attachment object
    attachment = Attachment(
        title=file_name,
        url=upload_response['url'],  # DIAL returns uploaded file URL
        type=mime_type_png
    )
    return attachment


def start() -> None:
    async def _main():
        # Create DialModelClient
        client = DialModelClient(api_key=API_KEY, endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT)

        # Upload image
        attachment = await _put_image()
        print("Uploaded Attachment:", attachment)

        # Prepare message with attachment
        message = Message(
            role=Role.USER,
            content="What do you see on this picture?",
            custom_content=CustomContent(attachments=[attachment])
        )

        # Send chat completion request
        response = client.chat_completion(messages=[message])
        print("Chat Completion Response:\n", response)

    asyncio.run(_main())


if __name__ == "__main__":
    start()
