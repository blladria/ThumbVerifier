# ==========================================
# SCRIPT DE INSTALACIÓN - PROYECTO THUMB VERIFIER
# ==========================================

Clear-Host
Write-Host "===================================================" -ForegroundColor Magenta
Write-Host "   🛠️  INSTALADOR AUTOMÁTICO - THUMB VERIFIER" -ForegroundColor Magenta
Write-Host "==================================================="
Write-Host "NOTA DE SEGURIDAD:" -ForegroundColor Yellow
Write-Host "Si este script da error de permisos (SecurityError),"
Write-Host "ciérralo y ejecútalo manualmente con este comando:"
Write-Host "PowerShell -ExecutionPolicy Bypass -File .\install.ps1" -ForegroundColor Cyan
Write-Host "===================================================`n"

# 0. Limpieza y Verificación
Write-Host "--- PASO 0: Verificando Python ---" -ForegroundColor Cyan
python --version

# 1. Crear el Entorno Virtual
Write-Host "`n--- PASO 1: Creando el entorno virtual (venv) ---" -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "El entorno 'venv' ya existe. Saltando creación." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Entorno 'venv' creado correctamente." -ForegroundColor Green
}

# 2. Actualizar pip
Write-Host "`n--- PASO 2: Actualizando pip ---" -ForegroundColor Cyan
.\venv\Scripts\python -m pip install --upgrade pip

# 3. Instalar PyTorch con CUDA (Para RTX 4070)
Write-Host "`n--- PASO 3: Instalando PyTorch (Versión GPU/CUDA) ---" -ForegroundColor Cyan
Write-Host "Descargando librerías grandes (Torch + CUDA). Esto dependerá de tu internet..." -ForegroundColor Yellow
.\venv\Scripts\pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. Instalar librerías de utilidades
Write-Host "`n--- PASO 4: Instalando Streamlit, LPIPS y herramientas de imagen ---" -ForegroundColor Cyan
.\venv\Scripts\pip install streamlit lpips numpy pillow matplotlib scikit-image

# 5. Instalar CLIP (OpenAI)
Write-Host "`n--- PASO 5: Instalando CLIP desde GitHub ---" -ForegroundColor Cyan
.\venv\Scripts\pip install git+https://github.com/openai/CLIP.git

# 6. Finalización
Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "¡INSTALACIÓN COMPLETADA CON ÉXITO!" -ForegroundColor Green
Write-Host "=========================================="
Write-Host "Para empezar a trabajar, ejecuta:"
Write-Host ".\venv\Scripts\activate" -ForegroundColor White
Write-Host "streamlit run app.py" -ForegroundColor White