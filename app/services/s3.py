import hashlib
import os

from config import Config, get_config
from fastapi import Depends, UploadFile


class S3Service:
    s3_folder: str

    def __init__(self, config: Config = Depends(get_config)) -> None:
        self.s3_folder = config.S3.FODLER

    async def save_file(self, user_id: str, file: UploadFile, private: bool) -> str:
        prefix = "private/" if private else ""
        h = hashlib.new("sha256")

        body = await file.read()
        h.update(body)
        file_name = file.filename if file.filename else ""
        path = f"{prefix}{user_id}/{h.hexdigest()[:15]}"

        os.makedirs(os.path.dirname(f"{self.s3_folder}{path}"), exist_ok=True)
        with open(f"{self.s3_folder}{path}.{file_name}", "w+b") as f:
            f.write(body)

        await file.close()

        return f"/{path}/{file_name}"

    async def load_file(self, path: str) -> bytes:
        with open(self.s3_folder + path, "rb") as f:
            contents = f.read()
        return contents
