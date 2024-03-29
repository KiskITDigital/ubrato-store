import os
import hashlib

from fastapi import Depends, UploadFile

from config import Config, get_config


class S3Service:
    s3_folder: str

    def __init__(
        self, config: Config = Depends(get_config)
    ) -> None:
        self.s3_folder = config.S3.FODLER

    async def save_file(
        self, user_id: str, file: UploadFile, private: bool
    ) -> str:
        prefix = "private/" if private else ""
        h = hashlib.new('sha256')

        body = await file.read()
        h.update(body)
        path = f"{self.s3_folder}{prefix}{user_id}/{h.hexdigest()}"

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w+b") as f:
            f.write(body)

        await file.close()

        return path

    async def load_file(self, path: str) -> bytes:
        with open(self.s3_folder + path, "rb") as f:
            contents = f.read()
        return contents
