import os
from typing import List

import aiofiles

from fastapi import HTTPException, UploadFile


async def save_input_file_to_storage(file: UploadFile, save_dir: str) -> str:
    file_path = os.path.join(save_dir, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File {file.filename} already exists! Rename the file and try again.")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return file_path

def is_directory_empty(dir: str, extensions: List[str]) -> bool:
    if not os.path.exists(dir):
        raise FileNotFoundError(f"The directory {dir} does not exist.")

    for file in os.listdir(dir):
        if not file.startswith('.') and os.path.isfile(os.path.join(dir, file)):
            if any(file.lower().endswith(ext) for ext in extensions):
                return False  # Directory is not empty (has matching file)

    return True  # No matching files found


async def delete_file(file_path: str):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {os.path.basename(file_path)} not found.")
    try:
        os.remove(file_path)
        return {"detail": f"File {os.path.basename(file_path)} has been deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


def delete_files_with_extensions(dir_path: str, extensions: List[str]):
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"The path '{dir_path}' is not a directory.")

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path) and any(file_name.endswith(ext) for ext in extensions):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_name}: {e}")