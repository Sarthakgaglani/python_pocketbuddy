import cloudinary
from cloudinary.uploader import upload

cloudinary.config(
    cloud_name="dtahqx61d",
    api_key="694342862599373",
    api_secret="Ekd2RGWt792yGf1JujfNRK2skAk",
)

async def upload_image(image):
    result = upload(image)
    print("cloudinary response,",result)
    return result["secure_url"]