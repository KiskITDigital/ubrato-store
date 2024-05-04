import hashlib
import os
import time
from datetime import datetime, timedelta, timezone

from config import Config, get_config
from fastapi import Depends, HTTPException, UploadFile, status
from schemas.file_stats import FileStatsResponse


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
        try:
            with open(self.s3_folder + path, "rb") as f:
                contents = f.read()
            return contents
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )

    def get_info(self, path: str) -> FileStatsResponse:
        try:
            stat = os.stat(self.s3_folder + path)
            timestamp = datetime.fromtimestamp(stat.st_atime, tz=timezone.utc)
            local_timezone_offset = -(
                time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
            )
            local_timezone = timezone(timedelta(seconds=local_timezone_offset))
            local_timestamp = timestamp.replace(tzinfo=timezone.utc).astimezone(
                local_timezone
            )

            filename, file_extension = os.path.splitext(self.s3_folder + path)
            return FileStatsResponse(
                name=filename,
                format=file_extension,
                size=stat.st_size,
                ctime=local_timestamp,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
