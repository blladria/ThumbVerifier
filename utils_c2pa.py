import subprocess
import os
import tempfile
import json
from PIL import Image
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_thumbnail(image_path):
    """
    Extrae la miniatura firmada de una imagen usando c2patool.exe
    Método: Extracción por directorio temporal
    
    Args:
        image_path (str): Ruta a la imagen de entrada
        
    Returns:
        PIL.Image: Imagen de la miniatura extraída o None si falla
    """
    try:
        # Crear directorio temporal para archivos extraídos
        temp_dir = tempfile.mkdtemp()
        
        # Ejecutar c2patool para extraer recursos al directorio temporal
        cmd = [
            "./c2patool.exe",
            image_path,
            "-o", temp_dir,
            "--force"
        ]
        
        logger.info(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            logger.error(f"c2patool falló: {result.stderr}")
            cleanup_temp_files(temp_dir)
            return None
            
        # Buscar la miniatura en el directorio temporal (búsqueda recursiva)
        thumbnail_path = find_thumbnail_in_directory(temp_dir)
        
        if thumbnail_path:
            thumbnail_img = Image.open(thumbnail_path)
            logger.info(f"Miniatura encontrada: {thumbnail_path}")
            
            # Limpiar archivos temporales
            cleanup_temp_files(temp_dir)
            return thumbnail_img
        else:
            logger.warning("No se encontró archivo de miniatura en el directorio temporal")
            cleanup_temp_files(temp_dir)
            return None
            
    except Exception as e:
        logger.error(f"Error extrayendo miniatura: {str(e)}")
        if 'temp_dir' in locals():
            cleanup_temp_files(temp_dir)
        return None

def find_thumbnail_in_directory(directory):
    """
    Busca recursivamente archivos de imagen que puedan ser la miniatura
    
    Args:
        directory (str): Directorio donde buscar
        
    Returns:
        str: Ruta al archivo de miniatura encontrado o None
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.webp'}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # Ignorar archivos que no sean imágenes
            if file_ext not in image_extensions:
                continue
                
            # Prioridad 1: Archivos con "thumbnail" en el nombre
            if 'thumbnail' in file.lower():
                logger.info(f"Thumbnail encontrado por nombre: {file_path}")
                return file_path
                
            # Prioridad 2: Imágenes pequeñas (probablemente miniaturas)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    # Si es pequeña (probablemente una miniatura)
                    if width <= 512 and height <= 512:
                        logger.info(f"Thumbnail encontrado por tamaño: {file_path} ({width}x{height})")
                        return file_path
            except:
                # Si no podemos abrir la imagen, continuar
                continue
    
    return None

def cleanup_temp_files(temp_dir):
    """
    Limpia los archivos temporales creados durante la extracción
    
    Args:
        temp_dir (str): Ruta del directorio temporal a limpiar
    """
    try:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info(f"Limpiado directorio temporal: {temp_dir}")
    except Exception as e:
        logger.warning(f"No se pudo limpiar {temp_dir}: {str(e)}")

def test_c2patool():
    """
    Función de prueba para verificar que c2patool funciona
    """
    try:
        result = subprocess.run(["./c2patool.exe", "--version"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            logger.info(f"c2patool versión: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"c2patool no disponible: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("c2patool.exe no encontrado en el directorio actual")
        return False
