from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pyzbar.pyzbar import decode
from PIL import Image
import io
import requests
import cv2
import numpy as np
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "localhost"],  # Tambahkan asal (origin) yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"message": "Selamat datang di server kami"}

@app.post('/scan-barcode/')
async def scan_barcode(file: UploadFile = File(...)):
    try:
        # Baca gambar dari file yang di-upload
        image = Image.open(io.BytesIO(await file.read()))
        
        # Konversi gambar ke format yang sesuai untuk OpenCV
        image_np = np.array(image)
        processed_image = preprocess_image(image_np)
        
        # Decode barcode dari gambar yang telah diproses
        decoded_objects = decode(processed_image)
        
        if not decoded_objects:
            raise HTTPException(status_code=400, detail="Tidak ada barcode yang terdeteksi")
        
        barcodes = []
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            product_info = get_product_info(barcode_data)
            
            barcodes.append({
                "type": obj.type,
                "data": barcode_data,
                "product_info": product_info
            })
        
        return JSONResponse(content={"barcodes": barcodes})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def preprocess_image(image):
    # Konversi gambar ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gunakan blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Gunakan threshold untuk membuat gambar menjadi biner
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Gunakan morfologi untuk menghilangkan noise kecil
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return processed_image

def get_product_info(barcode):
    # Gunakan Open Food Facts API untuk mendapatkan informasi produk berdasarkan barcode
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Produk tidak ditemukan"}
    
    product_data = response.json()
    if product_data.get("status") == 0:
        return {"error": "Produk tidak ditemukan"}
    
    product = product_data.get("product", {})
    
    product_info = {
        "Nama_produk": product.get("product_name", "Tidak diketahui"),
        "Merk": product.get("brands", "tidak didaftarka"),
        "kategory": product.get("categories", "tidak didaftarka"),
        "Nilai_nutrisi": product.get("nutriscore_grade", "Tidak diketahui"),
        "nutriments": product.get("nutriments", "tidak didaftarka"),
        "EcoLevel": product.get("ecoscore_grade", "tidak didaftarka"),
        "Gambar": product.get("image_url", "informasi gambar kosong")
    }
    
    return product_info


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
