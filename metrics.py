import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity


def prepare_images(imageA, imageB):
    """
    Prepara dos imágenes para comparación.
    Identifica la imagen más pequeña y la redimensiona al tamaño de la grande
    usando interpolación BICUBIC.
    
    Args:
        imageA: PIL Image
        imageB: PIL Image
    
    Returns:
        tuple: (imageA_array, imageB_array) - arrays numpy del mismo tamaño
    """
    # Convertir a arrays numpy
    imgA_array = np.array(imageA)
    imgB_array = np.array(imageB)
    
    # Identificar cuál es más pequeña
    sizeA = imgA_array.shape[:2]  # (alto, ancho)
    sizeB = imgB_array.shape[:2]
    
    # Calcular áreas para determinar cuál es más pequeña
    areaA = sizeA[0] * sizeA[1]
    areaB = sizeB[0] * sizeB[1]
    
    # Si B es más pequeña, redimensionar B al tamaño de A
    if areaB < areaA:
        target_size = (sizeA[1], sizeA[0])  # PIL usa (ancho, alto)
        imgB_resized = Image.fromarray(imgB_array).resize(target_size, Image.Resampling.BICUBIC)
        imgB_array = np.array(imgB_resized)
    
    # Si A es más pequeña, redimensionar A al tamaño de B
    elif areaA < areaB:
        target_size = (sizeB[1], sizeB[0])  # PIL usa (ancho, alto)
        imgA_resized = Image.fromarray(imgA_array).resize(target_size, Image.Resampling.BICUBIC)
        imgA_array = np.array(imgA_resized)
    
    # Asegurar que ambas imágenes tengan el mismo número de canales
    if len(imgA_array.shape) == 2 and len(imgB_array.shape) == 3:
        imgA_array = np.stack([imgA_array] * 3, axis=-1)
    elif len(imgB_array.shape) == 2 and len(imgA_array.shape) == 3:
        imgB_array = np.stack([imgB_array] * 3, axis=-1)
    elif len(imgA_array.shape) == 2 and len(imgB_array.shape) == 2:
        imgA_array = np.stack([imgA_array] * 3, axis=-1)
        imgB_array = np.stack([imgB_array] * 3, axis=-1)
    
    return imgA_array, imgB_array


def calculate_mse(imageA, imageB):
    """
    Calcula el Error Cuadrático Medio (Mean Squared Error) entre dos imágenes.
    
    Args:
        imageA: PIL Image
        imageB: PIL Image
    
    Returns:
        float: Valor MSE
    """
    # Preparar imágenes para comparación
    imgA_array, imgB_array = prepare_images(imageA, imageB)
    
    # Calcular MSE
    mse = np.mean((imgA_array.astype(float) - imgB_array.astype(float)) ** 2)
    
    return float(mse)


def calculate_ssim(imageA, imageB):
    """
    Calcula el Structural Similarity Index (SSIM) entre dos imágenes.
    Convierte ambas imágenes a escala de grises antes del cálculo.
    
    Args:
        imageA: PIL Image
        imageB: PIL Image
    
    Returns:
        float: Valor SSIM (entre -1 y 1, donde 1 es identidad perfecta)
    """
    # Preparar imágenes para comparación
    imgA_array, imgB_array = prepare_images(imageA, imageB)
    
    # Convertir a escala de grises si son RGB
    if len(imgA_array.shape) == 3:
        imgA_gray = np.dot(imgA_array[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        imgA_gray = imgA_array
    
    if len(imgB_array.shape) == 3:
        imgB_gray = np.dot(imgB_array[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        imgB_gray = imgB_array
    
    # Calcular SSIM con data_range=255 para imágenes de 8 bits
    ssim = structural_similarity(
        imgA_gray, 
        imgB_gray, 
        data_range=255
    )
    
    return float(ssim)
