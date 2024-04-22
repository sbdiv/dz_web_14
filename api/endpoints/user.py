from fastapi import APIRouter, File, UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
import os

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@router.post("/upload_avatar/")
async def upload_avatar(file: UploadFile = File(...)):
    """
    Завантажує аватар користувача на сервер Cloudinary.

    Args:
        file (UploadFile): Файл зображення, який потрібно завантажити.

    Returns:
        dict: Словник із URL завантаженого аватара користувача.
    """


    response = cloudinary.uploader.upload(file.file)

    if response.get("secure_url"):
        return {"avatar_url": response["secure_url"]}
    else:
        raise HTTPException(status_code=500, detail="Failed to upload avatar")
