# Cisalhamento Geométrico — API REST v2.0.0

![Status](https://img.shields.io/badge/Status-✅%20Online-brightgreen)
![Versão](https://img.shields.io/badge/Versão-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![API](https://img.shields.io/badge/API-FastAPI-09a031)

## 🎯 Objetivo

API REST para calcular e visualizar transformações geométricas de cisalhamento (shear) horizontal e vertical em figuras 2D.

---

## 🚀 LINK PRINCIPAL

### **→ [http://localhost:8000/docs](http://localhost:8000/docs) ←**

Acesse este link no navegador para:
- ✅ Documentação interativa Swagger UI
- ✅ Testar todos os endpoints
- ✅ Ver exemplos de requisição/resposta
- ✅ Visualizar schemas de dados

---

## 📋 Começando Rápido

### 1. Instalar Dependências
```bash
pip install fastapi uvicorn numpy
```

### 2. Rodar o Servidor
```bash
python api.py
```

**Output esperado:**
```
🌐 Servidor rodando em http://0.0.0.0:8000
📚 Documentação Swagger em http://localhost:8000/docs
📖 Documentação ReDoc em http://localhost:8000/redoc
```

### 3. Abrir no Navegador
```
http://localhost:8000/docs
```

---

## 📡 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Info da API |
| `GET` | `/figuras` | Listar figuras |
| `GET` | `/horizontal/{shx}` | Cisalhamento horizontal |
| `GET` | `/vertical/{shy}` | Cisalhamento vertical |
| `POST` | `/transformar-figura` | Transformar figura nomeada |
| `POST` | `/transformar` | Transformar pontos |
| `GET` | `/matriz` | Calcular matriz |

---

## 💡 Exemplos de Uso

### Exemplo 1: Cisalhamento Horizontal (GET)
```bash
curl http://localhost:8000/horizontal/1.5
```

**Resposta:**
```json
{
  "figura": "Quadrado",
  "modo": "Horizontal",
  "shx": 1.5,
  "pontos_originais": [{"x": -2.0, "y": -2.0}, ...],
  "pontos_transformados": [{"x": -5.0, "y": -2.0}, ...]
}
```

### Exemplo 2: Transformar Figura (POST)
```bash
curl -X POST http://localhost:8000/transformar-figura \
  -H "Content-Type: application/json" \
  -d '{
    "figura": "Casa",
    "shx": 1.0,
    "shy": 0.5,
    "modo": "Ambos"
  }'
```

### Exemplo 3: Calcular Matriz (GET)
```bash
curl "http://localhost:8000/matriz?modo=Ambos&shx=1.5&shy=0.5"
```

---

## 📐 Fórmulas Implementadas

### Cisalhamento Horizontal
```
x' = x + shx · y
y' = y
```

### Cisalhamento Vertical
```
x' = x
y' = y + shy · x
```

### Combinado (Ambos)
```
x' = x + shx · y
y' = y + shy · x'
```

---

## 🎨 Figuras Disponíveis

1. **Quadrado** — 4 vértices
2. **Triângulo** — 3 vértices  
3. **Casa** — 5 vértices

```bash
# Listar todas as figuras
curl http://localhost:8000/figuras
```

---

## 📊 Documentação Adicional

- [CORRECOES.md](CORRECOES.md) — Análise de erros corrigidos
- [API.md](API.md) — Documentação completa dos endpoints
- [CLAUDE.md](CLAUDE.md) — Contexto do projeto

---

## ✅ Validações Implementadas

- ✅ Coordenadas no intervalo [-1e7, 1e7]
- ✅ Fatores de cisalhamento [-100, 100]
- ✅ Máximo 1000 pontos por requisição
- ✅ Validação de NaN/Inf
- ✅ Modo deve ser: Horizontal, Vertical ou Ambos
- ✅ Figura deve ser: Quadrado, Triângulo ou Casa

---

## 🔐 Segurança

- ✅ Validação robusta de entrada
- ✅ Tratamento de exceções completo
- ✅ Limites de recursos
- ✅ Logging de operações
- ✅ CORS configurado

---

## 📊 Status da API

- ✅ v2.0.0 — Production Ready
- ✅ Sem erros ou warnings
- ✅ Totalmente documentada
- ✅ Testada e validada

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| FastAPI | latest | Framework REST |
| Uvicorn | latest | Servidor ASGI |
| NumPy | latest | Cálculos matriciais |
| Pydantic v2 | latest | Validação de dados |

---

## 📝 Licença

Projeto Acadêmico — CIESA (Computação Gráfica)

---

**Última atualização:** 3 de maio de 2026  
**Status:** ✅ Online e funcionando perfeitamente
