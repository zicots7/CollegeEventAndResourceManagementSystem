import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
# Configure Cloudinary (Put your actual credentials here)
load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('NAME_CLOUDINARY_DB'),
    api_key=os.getenv('API_KEY_CLOUDINARY'),
    api_secret=os.getenv('API_SECRET_CLOUDINARY'),
    secure=True
)

def upload_file_to_cloudinary(file_obj, unique_name):
    try:
        result = cloudinary.uploader.upload(
            file_obj,
            public_id=unique_name,
            resource_type="raw"  # Automatically detects if it's a PDF or Image
        )
        # Return the secure URL string
        return result.get('secure_url')
    except Exception as e:
        print(f"Cloudinary Error: {e}")
        return None

def delete_file_from_cloudinary(public_id):
    """
    public_id: The unique name used during upload (without the extension)
    resource_type: 'image', 'video', or 'raw' (use 'raw' for PDFs/Docs)
    """
    try:
        # PDFs must specify resource_type='raw' or Cloudinary won't find them
        result = cloudinary.uploader.destroy(public_id, resource_type='raw')
        return result.get('result') == 'ok'
    except Exception as e:
        print(f"Cloudinary Deletion Error: {e}")
        return False