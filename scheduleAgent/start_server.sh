#!/bin/bash

# Script para iniciar el servidor Flask en scheduleAgent

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo "🚀 Schedule Agent - Iniciando..."
echo "=========================================="
echo ""

# Verificar directorio
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py no encontrado${NC}"
    echo "Por favor, ejecuta este script desde: /Users/ian.hdzzz/Prometheus/scheduleAgent"
    exit 1
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: .env no encontrado${NC}"
    echo "Copiando desde directorio padre..."
    cp ../.env . 2>/dev/null || echo -e "${RED}No se pudo copiar .env${NC}"
fi

# Verificar credenciales
if [ ! -f "hack-475720-a80832b916e2.json" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: Credenciales de Google no encontradas${NC}"
    echo "Copiando desde directorio padre..."
    cp ../hack-475720-a80832b916e2.json . 2>/dev/null || echo -e "${RED}No se pudieron copiar credenciales${NC}"
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo -e "${BLUE}🔄 Activando entorno virtual...${NC}"
    source venv/bin/activate
elif [ -d "../.venv" ]; then
    echo -e "${BLUE}🔄 Activando entorno virtual del directorio padre...${NC}"
    source ../.venv/bin/activate
fi

# Instalar dependencias
echo -e "${BLUE}🔄 Verificando dependencias...${NC}"
pip install -q -r requirements.txt 2>/dev/null || echo -e "${YELLOW}Algunas dependencias pueden faltar${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Listo para iniciar!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}📍 Iniciando servidor Flask...${NC}"
echo ""

# Iniciar Flask
python app.py
