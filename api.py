#!/usr/bin/env python3
"""
Cisalhamento Geométrico - API REST (CORRIGIDA)
API FastAPI para calcular transformações de cisalhamento 2D
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any
import numpy as np
import uvicorn
import math
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Cisalhamento Geométrico API",
    description="API para transformações geométricas de cisalhamento horizontal e vertical",
    version="2.0.0"
)

# Adicionar CORS de forma segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Figuras disponíveis
FIGURAS = {
    "Quadrado": [(-2, -2), (2, -2), (2, 2), (-2, 2)],
    "Triângulo": [(0, 3), (-3, -2), (3, -2)],
    "Casa": [(-2, -2), (2, -2), (2, 1), (0, 3), (-2, 1)]
}

# Modelos Pydantic
class Ponto(BaseModel):
    """Modelo para representar um ponto 2D"""
    x: float = Field(..., description="Coordenada X")
    y: float = Field(..., description="Coordenada Y")
    
    @field_validator('x', 'y')
    @classmethod
    def validar_coordenadas(cls, v):
        """Valida se a coordenada é um número finito"""
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Coordenada não pode ser NaN ou infinito")
        if abs(v) > 1e7:
            raise ValueError("Coordenada fora do intervalo permitido [-1e7, 1e7]")
        return v

class RequisicaoCisalhamento(BaseModel):
    """Modelo para requisição de cisalhamento"""
    pontos: List[Ponto] = Field(..., description="Lista de vértices", max_length=1000)
    shx: float = Field(default=0.0, ge=-100, le=100, description="Fator de cisalhamento horizontal")
    shy: float = Field(default=0.0, ge=-100, le=100, description="Fator de cisalhamento vertical")
    modo: str = Field(default="Ambos", description="Tipo: Horizontal, Vertical ou Ambos")
    
    @field_validator('pontos')
    @classmethod
    def validar_pontos_minimo(cls, v):
        """Valida que há pelo menos 1 ponto"""
        if len(v) == 0:
            raise ValueError("Deve haver pelo menos 1 ponto")
        return v

class RespostaPontos(BaseModel):
    """Modelo para resposta com pontos transformados"""
    pontos_originais: List[Ponto]
    pontos_transformados: List[Ponto]
    modo: str
    shx: float
    shy: float
    matriz: List[List[float]]

class RequisicaoFigura(BaseModel):
    """Modelo para requisição com figura nomeada"""
    figura: str = Field(..., description="Nome: Quadrado, Triângulo ou Casa")
    shx: float = Field(default=0.0, ge=-100, le=100, description="Cisalhamento horizontal")
    shy: float = Field(default=0.0, ge=-100, le=100, description="Cisalhamento vertical")
    modo: str = Field(default="Ambos", description="Tipo: Horizontal, Vertical ou Ambos")

class RespostaMatriz(BaseModel):
    """Modelo para resposta de matriz"""
    modo: str
    shx: float
    shy: float
    matriz: List[List[float]]

class RespostaFiguras(BaseModel):
    """Modelo para resposta de figuras disponíveis"""
    figuras: Dict[str, List[Ponto]]

class RespostaSaude(BaseModel):
    """Modelo para resposta de saúde"""
    status: str
    versao: str
    endpoint_docs: str

# Funções de transformação
def cisalhamento_horizontal(pontos: np.ndarray, shx: float) -> np.ndarray:
    """Aplica x' = x + shx·y para cada vértice"""
    matriz = np.array([
        [1, shx, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    transformados = pontos_homogeneos @ matriz.T
    
    return transformados[:, :2]

def cisalhamento_vertical(pontos: np.ndarray, shy: float) -> np.ndarray:
    """Aplica y' = y + shy·x para cada vértice"""
    matriz = np.array([
        [1, 0, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ])
    
    pontos_homogeneos = np.column_stack([pontos, np.ones(len(pontos))])
    transformados = pontos_homogeneos @ matriz.T
    
    return transformados[:, :2]

def aplicar_transformacao(pontos: np.ndarray, shx: float, shy: float, modo: str) -> np.ndarray:
    """Combina horizontal e vertical conforme o modo"""
    if modo == "Horizontal":
        return cisalhamento_horizontal(pontos, shx)
    elif modo == "Vertical":
        return cisalhamento_vertical(pontos, shy)
    elif modo == "Ambos":
        horizontal = cisalhamento_horizontal(pontos, shx)
        return cisalhamento_vertical(horizontal, shy)
    else:
        return pontos.copy()

def obter_matriz_transformacao(shx: float, shy: float, modo: str) -> np.ndarray:
    """Retorna a matriz de transformação atual"""
    if modo == "Horizontal":
        return np.array([
            [1, shx, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
    elif modo == "Vertical":
        return np.array([
            [1, 0, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ])
    elif modo == "Ambos":
        return np.array([
            [1, shx, 0],
            [shy, 1 + shx * shy, 0],
            [0, 0, 1]
        ])
    else:
        return np.eye(3)

# Endpoints

@app.get("/", response_model=RespostaSaude, tags=["Info"])
async def root():
    """Endpoint raiz - informações da API"""
    logger.info("Requisição para endpoint raiz")
    return RespostaSaude(
        status="online",
        versao="2.0.0",
        endpoint_docs="/docs"
    )

@app.get("/saude", response_model=RespostaSaude, tags=["Info"])
async def verificar_saude():
    """Verifica se a API está funcionando"""
    logger.info("Verificação de saúde")
    return RespostaSaude(
        status="online",
        versao="2.0.0",
        endpoint_docs="/docs"
    )

@app.get("/figuras", response_model=RespostaFiguras, tags=["Figuras"])
async def listar_figuras():
    """Lista todas as figuras disponíveis com seus vértices"""
    try:
        figuras_dict = {}
        for nome, pontos in FIGURAS.items():
            figuras_dict[nome] = [Ponto(x=p[0], y=p[1]) for p in pontos]
        
        logger.info("Figuras listadas com sucesso")
        return RespostaFiguras(figuras=figuras_dict)
    except Exception as e:
        logger.error(f"Erro ao listar figuras: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar figuras: {str(e)}")

@app.post("/transformar", response_model=RespostaPontos, tags=["Transformações"])
async def transformar_pontos(requisicao: RequisicaoCisalhamento):
    """
    Transforma uma lista de pontos customizados aplicando cisalhamento
    
    **Parâmetros:**
    - pontos: Lista de pontos {x, y} (máximo 1000)
    - shx: Fator horizontal [-100, 100]
    - shy: Fator vertical [-100, 100]
    - modo: Horizontal, Vertical ou Ambos
    """
    try:
        if requisicao.modo not in ["Horizontal", "Vertical", "Ambos"]:
            raise ValueError(f"Modo inválido: {requisicao.modo}")
        
        pontos_originais = np.array([[p.x, p.y] for p in requisicao.pontos])
        pontos_transformados = aplicar_transformacao(
            pontos_originais, 
            requisicao.shx, 
            requisicao.shy, 
            requisicao.modo
        )
        
        if np.any(np.isnan(pontos_transformados)) or np.any(np.isinf(pontos_transformados)):
            raise ValueError("Transformação resultou em valores inválidos")
        
        matriz = obter_matriz_transformacao(requisicao.shx, requisicao.shy, requisicao.modo)
        pts_transformados = [Ponto(x=float(p[0]), y=float(p[1])) for p in pontos_transformados]
        
        logger.info(f"Pontos transformados: modo={requisicao.modo}, n_pontos={len(requisicao.pontos)}")
        
        return RespostaPontos(
            pontos_originais=requisicao.pontos,
            pontos_transformados=pts_transformados,
            modo=requisicao.modo,
            shx=requisicao.shx,
            shy=requisicao.shy,
            matriz=matriz.tolist()
        )
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao transformar pontos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/transformar-figura", response_model=RespostaPontos, tags=["Transformações"])
async def transformar_figura(requisicao: RequisicaoFigura):
    """
    Transforma uma figura nomeada aplicando cisalhamento
    
    **Parâmetros:**
    - figura: Quadrado, Triângulo ou Casa
    - shx: Fator horizontal [-100, 100]
    - shy: Fator vertical [-100, 100]
    - modo: Horizontal, Vertical ou Ambos
    """
    try:
        if requisicao.figura not in FIGURAS:
            raise ValueError(
                f"Figura inválida '{requisicao.figura}'. Opções: {', '.join(FIGURAS.keys())}"
            )
        
        if requisicao.modo not in ["Horizontal", "Vertical", "Ambos"]:
            raise ValueError(f"Modo inválido: {requisicao.modo}")
        
        pontos_originais = np.array(FIGURAS[requisicao.figura])
        pontos_transformados = aplicar_transformacao(
            pontos_originais, 
            requisicao.shx, 
            requisicao.shy, 
            requisicao.modo
        )
        
        if np.any(np.isnan(pontos_transformados)) or np.any(np.isinf(pontos_transformados)):
            raise ValueError("Transformação resultou em valores inválidos")
        
        matriz = obter_matriz_transformacao(requisicao.shx, requisicao.shy, requisicao.modo)
        pts_originais = [Ponto(x=float(p[0]), y=float(p[1])) for p in pontos_originais]
        pts_transformados = [Ponto(x=float(p[0]), y=float(p[1])) for p in pontos_transformados]
        
        logger.info(f"Figura transformada: figura={requisicao.figura}, modo={requisicao.modo}")
        
        return RespostaPontos(
            pontos_originais=pts_originais,
            pontos_transformados=pts_transformados,
            modo=requisicao.modo,
            shx=requisicao.shx,
            shy=requisicao.shy,
            matriz=matriz.tolist()
        )
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao transformar figura: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/matriz", response_model=RespostaMatriz, tags=["Transformações"])
async def calcular_matriz(
    modo: str = Query("Ambos", description="Horizontal, Vertical ou Ambos"),
    shx: float = Query(0.0, ge=-100, le=100, description="Cisalhamento horizontal"),
    shy: float = Query(0.0, ge=-100, le=100, description="Cisalhamento vertical")
):
    """
    Calcula a matriz de transformação
    
    **Parâmetros:**
    - modo: Horizontal, Vertical ou Ambos
    - shx: Fator horizontal [-100, 100]
    - shy: Fator vertical [-100, 100]
    """
    try:
        if modo not in ["Horizontal", "Vertical", "Ambos"]:
            raise ValueError("Modo inválido. Use: Horizontal, Vertical ou Ambos")
        
        matriz = obter_matriz_transformacao(shx, shy, modo)
        logger.info(f"Matriz calculada: modo={modo}, shx={shx}, shy={shy}")
        
        return RespostaMatriz(
            modo=modo,
            shx=shx,
            shy=shy,
            matriz=matriz.tolist()
        )
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao calcular matriz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/horizontal/{shx}", tags=["Transformações"])
async def cisalhamento_h(
    shx: float = Path(..., ge=-100, le=100, description="Fator de cisalhamento horizontal")
):
    """
    Aplica cisalhamento horizontal ao quadrado
    
    **Fórmula:** x' = x + shx·y, y' = y
    
    - shx: Fator horizontal [-100, 100]
    """
    try:
        if math.isnan(shx) or math.isinf(shx):
            raise ValueError("shx não pode ser NaN ou infinito")
        
        pontos_originais = np.array(FIGURAS["Quadrado"])
        pontos_transformados = cisalhamento_horizontal(pontos_originais, shx)
        
        if np.any(np.isnan(pontos_transformados)) or np.any(np.isinf(pontos_transformados)):
            raise ValueError("Transformação resultou em valores inválidos")
        
        pts_originais = [{"x": float(p[0]), "y": float(p[1])} for p in pontos_originais]
        pts_transformados = [{"x": float(p[0]), "y": float(p[1])} for p in pontos_transformados]
        
        logger.info(f"Cisalhamento horizontal: shx={shx}")
        
        return {
            "figura": "Quadrado",
            "modo": "Horizontal",
            "shx": shx,
            "pontos_originais": pts_originais,
            "pontos_transformados": pts_transformados
        }
    except ValueError as e:
        logger.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro em horizontal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.get("/vertical/{shy}", tags=["Transformações"])
async def cisalhamento_v(
    shy: float = Path(..., ge=-100, le=100, description="Fator de cisalhamento vertical")
):
    """
    Aplica cisalhamento vertical ao quadrado
    
    **Fórmula:** x' = x, y' = y + shy·x
    
    - shy: Fator vertical [-100, 100]
    """
    try:
        if math.isnan(shy) or math.isinf(shy):
            raise ValueError("shy não pode ser NaN ou infinito")
        
        pontos_originais = np.array(FIGURAS["Quadrado"])
        pontos_transformados = cisalhamento_vertical(pontos_originais, shy)
        
        if np.any(np.isnan(pontos_transformados)) or np.any(np.isinf(pontos_transformados)):
            raise ValueError("Transformação resultou em valores inválidos")
        
        pts_originais = [{"x": float(p[0]), "y": float(p[1])} for p in pontos_originais]
        pts_transformados = [{"x": float(p[0]), "y": float(p[1])} for p in pontos_transformados]
        
        logger.info(f"Cisalhamento vertical: shy={shy}")
        
        return {
            "figura": "Quadrado",
            "modo": "Vertical",
            "shy": shy,
            "pontos_originais": pts_originais,
            "pontos_transformados": pts_transformados
        }
    except ValueError as e:
        logger.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro em vertical: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

def main():
    """Executa o servidor uvicorn"""
    try:
        logger.info("=" * 80)
        logger.info("Iniciando Cisalhamento Geométrico API v2.0.0")
        logger.info("=" * 80)
        logger.info("🌐 Servidor rodando em http://0.0.0.0:8000")
        logger.info("📚 Documentação Swagger em http://localhost:8000/docs")
        logger.info("📖 Documentação ReDoc em http://localhost:8000/redoc")
        logger.info("🔌 OpenAPI JSON em http://localhost:8000/openapi.json")
        logger.info("=" * 80)
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor: {str(e)}")
        raise

if __name__ == "__main__":
    main()
