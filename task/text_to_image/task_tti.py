import asyncio
from datetime import datetime
from pathlib import Path
from io import BytesIO

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'

class Style:
    natural: str = "natural"
    vivid: str = "vivid"

class Quality:
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    """
    Download and save all attachments locally.
    """
    output_dir = Path(__file__).parent / "generated_images"
    output_dir.mkdir(exist_ok=True)

    for attachment in attachments:
        bucket_client = DialBucketClient(api_key=API_KEY, base_url=DIAL_URL)
        image_bytes = await bucket_client.download_file(attachment.url)

        file_name = f"{attachment.title}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        file_path = output_dir / file_name
        with open(file_path, 'wb') as f:
            f.write(image_bytes)
        print(f"Saved image: {file_path}")


def start() -> None:
    async def _main():
        # 1️⃣ Create DialModelClient
        client = DialModelClient(api_key=API_KEY, endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT)

        # 2️⃣ Generate image for prompt
        message = Message(
            role=Role.USER,
            content="Sunny day on Bali",
            custom_content=CustomContent(
                custom_fields={
                    "size": Size.square,
                    "style": Style.natural,
                    "quality": Quality.hd
                }
            )
        )

        response = client.chat_completion(
            messages=[message],
            deployment_name="imagegeneration@005"  # Google image generation model
        )

        # 3️⃣ Get attachments from response
        attachments = []
        for choice in response.choices:
            if choice.message.custom_content and choice.message.custom_content.attachments:
                attachments.extend(choice.message.custom_content.attachments)

        # 4️⃣ Save generated images locally
        await _save_images(attachments)

    asyncio.run(_main())


if __name__ == "__main__":
    start()
