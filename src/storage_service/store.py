import uuid
from decouple import config
from contextlib import contextmanager

from fastapi import UploadFile
from minio import Minio, S3Error


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint: str,
        bucket_name: str,
    ) -> None:
        self.config = {
            'access_key': access_key,
            'secret_key': secret_key,
            'endpoint': endpoint
        }
        self.bucket_name = bucket_name

    @contextmanager
    def get_client(self):
        client = Minio(**self.config)

        if not client.bucket_exists(self.bucket_name):
            client.make_bucket(self.bucket_name)

        yield client

    def add_image(self, file: UploadFile):
        if file is None:
            return None

        object_name = f'{uuid.uuid4()}.{file.filename.split('.')[-1]}'

        with self.get_client() as client:
            client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file.file,
                length=file.size,
            )

        return object_name

    def get_image(self, file_name: str):
        try:
            with self.get_client() as client:
                response = client.get_object(
                    self.bucket_name,
                    object_name=file_name
                )

                file = response.read()
                return file

        except (S3Error, TypeError):
            return 'нет картинки :('

    def delete_image(self, file_name: str):
        with self.get_client() as client:
            client.remove_object(self.bucket_name, object_name=file_name)

    def update_image(self, old_file: UploadFile, new_file: UploadFile):
        if new_file is None:
            return old_file

        self.delete_image(old_file)
        object_name = self.add_image(new_file)

        return object_name


endpoint = config('MINIO_ENDPOINT')
access_key = config('MINIO_ACCESS_KEY')
secret_key = config('MINIO_SECRET_KEY')
bucket_name = config('MINIO_BUCKET_NAME')

client = S3Client(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            bucket_name=bucket_name,
        )
