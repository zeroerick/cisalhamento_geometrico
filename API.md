# Cisalhamento Geométrico — API REST (v2.0.0)

## 🚀 Link Principal para Rodar o Programa

### ✅ **API já está rodando em:** `http://localhost:8000`

**Documentação Interativa (Swagger UI):**
```
http://localhost:8000/docs
```

**Alternativa (ReDoc):**
```
http://localhost:8000/redoc
```

**Arquivo de especificação OpenAPI:**
```
http://localhost:8000/openapi.json
```

---

## Como usar com Postman

### 1. Dependências (já instaladas)

```bash
pip install fastapi uvicorn numpy
```

### 2. Iniciar o servidor

```bash
python api.py
```

O servidor está rodando em `http://localhost:8000`

- **Documentação interativa:** `http://localhost:8000/docs` (Swagger UI) ⭐ **RECOMENDADO**
- **Documentação alternativa:** `http://localhost:8000/redoc` (ReDoc)

---

## Endpoints da API

### 1. **GET / — Informações da API**
```
GET http://localhost:8000/
```

**Resposta:**
```json
{
  "nome": "Cisalhamento Geométrico API",
  "versao": "1.0.0",
  "descricao": "API para calcular transformações geométricas de cisalhamento",
  "documentacao": "/docs"
}
```

---

### 2. **GET /figuras — Listar figuras disponíveis**
```
GET http://localhost:8000/figuras
```

**Resposta:**
```json
{
  "figuras": {
    "Quadrado": [
      {"x": -2, "y": -2},
      {"x": 2, "y": -2},
      {"x": 2, "y": 2},
      {"x": -2, "y": 2}
    ],
    "Triângulo": [
      {"x": 0, "y": 3},
      {"x": -3, "y": -2},
      {"x": 3, "y": -2}
    ],
    "Casa": [
      {"x": -2, "y": -2},
      {"x": 2, "y": -2},
      {"x": 2, "y": 1},
      {"x": 0, "y": 3},
      {"x": -2, "y": 1}
    ]
  }
}
```

---

### 3. **POST /transformar — Transformar pontos customizados**
```
POST http://localhost:8000/transformar
Content-Type: application/json
```

**Body (exemplo):**
```json
{
  "pontos": [
    {"x": -2, "y": -2},
    {"x": 2, "y": -2},
    {"x": 2, "y": 2},
    {"x": -2, "y": 2}
  ],
  "shx": 1.5,
  "shy": 0.5,
  "modo": "Ambos"
}
```

**Resposta:**
```json
{
  "pontos_originais": [
    {"x": -2, "y": -2},
    {"x": 2, "y": -2},
    {"x": 2, "y": 2},
    {"x": -2, "y": 2}
  ],
  "pontos_transformados": [
    {"x": -5.0, "y": -3.0},
    {"x": 0.25, "y": 1.0},
    {"x": 4.75, "y": 5.0},
    {"x": -0.25, "y": 1.0}
  ],
  "modo": "Ambos",
  "shx": 1.5,
  "shy": 0.5,
  "matriz": [
    [1.0, 1.5, 0.0],
    [0.5, 1.75, 0.0],
    [0.0, 0.0, 1.0]
  ]
}
```

---

### 4. **POST /transformar-figura — Transformar figura nomeada**
```
POST http://localhost:8000/transformar-figura
Content-Type: application/json
```

**Body (exemplo):**
```json
{
  "figura": "Quadrado",
  "shx": 1.0,
  "shy": 0.0,
  "modo": "Horizontal"
}
```

**Resposta:**
```json
{
  "pontos_originais": [
    {"x": -2, "y": -2},
    {"x": 2, "y": -2},
    {"x": 2, "y": 2},
    {"x": -2, "y": 2}
  ],
  "pontos_transformados": [
    {"x": -4.0, "y": -2},
    {"x": 0.0, "y": -2},
    {"x": 4.0, "y": 2},
    {"x": 0.0, "y": 2}
  ],
  "modo": "Horizontal",
  "shx": 1.0,
  "shy": 0.0,
  "matriz": [
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
  ]
}
```

---

### 5. **POST /matriz — Calcular matriz de transformação**
```
POST http://localhost:8000/matriz
Content-Type: application/json
```

**Body (exemplo):**
```json
{
  "modo": "Ambos",
  "shx": 1.5,
  "shy": 0.5
}
```

**Query Parameters (alternativa):**
```
POST http://localhost:8000/matriz?modo=Ambos&shx=1.5&shy=0.5
```

**Resposta:**
```json
{
  "modo": "Ambos",
  "shx": 1.5,
  "shy": 0.5,
  "matriz": [
    [1.0, 1.5, 0.0],
    [0.5, 1.75, 0.0],
    [0.0, 0.0, 1.0]
  ]
}
```

---

### 6. **GET /horizontal/{shx} — Cisalhamento horizontal rápido**
```
GET http://localhost:8000/horizontal/1.5
```

**Resposta:**
```json
{
  "figura": "Quadrado",
  "modo": "Horizontal",
  "shx": 1.5,
  "pontos_originais": [
    {"x": -2, "y": -2},
    {"x": 2, "y": -2},
    {"x": 2, "y": 2},
    {"x": -2, "y": 2}
  ],
  "pontos_transformados": [
    {"x": -5.0, "y": -2},
    {"x": 0.0, "y": -2},
    {"x": 5.0, "y": 2},
    {"x": 0.0, "y": 2}
  ]
}
```

---

### 7. **GET /vertical/{shy} — Cisalhamento vertical rápido**
```
GET http://localhost:8000/vertical/0.8
```

**Resposta:**
```json
{
  "figura": "Quadrado",
  "modo": "Vertical",
  "shy": 0.8,
  "pontos_originais": [
    {"x": -2, "y": -2},
    {"x": 2, "y": -2},
    {"x": 2, "y": 2},
    {"x": -2, "y": 2}
  ],
  "pontos_transformados": [
    {"x": -2, "y": -3.6},
    {"x": 2, "y": -0.4},
    {"x": 2, "y": 3.6},
    {"x": -2, "y": 0.4}
  ]
}
```

---

## Como testar no Postman

### Passo 1: Importar a API
1. Abra o Postman
2. Clique em **Import** → **Link**
3. Cole: `http://localhost:8000/openapi.json`
4. Clique **Continue** → **Import**

### Passo 2: Testar um endpoint
1. Selecione uma requisição da coleção importada
2. Clique **Send**
3. Veja a resposta na aba **Body**

### Ou criar manualmente:

**Exemplo 1 — Transformar figura**
- Método: `POST`
- URL: `http://localhost:8000/transformar-figura`
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "figura": "Triângulo",
    "shx": 0.5,
    "shy": 0.3,
    "modo": "Ambos"
  }
  ```

---

## Modos de cisalhamento

| Modo | Descrição |
|------|-----------|
| **Horizontal** | Apenas `x' = x + shx·y` |
| **Vertical** | Apenas `y' = y + shy·x` |
| **Ambos** | Ambas as transformações aplicadas |

---

## Fórmulas matemáticas

### Cisalhamento Horizontal
```
x' = x + shx · y
y' = y

Matriz:
┌              ┐
│ 1   shx  0   │
│ 0   1    0   │
│ 0   0    1   │
└              ┘
```

### Cisalhamento Vertical
```
x' = x
y' = y + shy · x

Matriz:
┌              ┐
│ 1   0    0   │
│ shy 1    0   │
│ 0   0    1   │
└              ┘
```

### Cisalhamento Combinado (Ambos)
```
x' = x + shx · y
y' = y + shy · x'

Matriz:
┌                    ┐
│ 1   shx         0  │
│ shy 1 + shx·shy 0  │
│ 0   0           1  │
└                    ┘
```

---

## Exemplos de uso com curl

```bash
# Listar figuras
curl -X GET "http://localhost:8000/figuras"

# Cisalhamento horizontal do quadrado com shx = 1.0
curl -X GET "http://localhost:8000/horizontal/1.0"

# Cisalhamento vertical do quadrado com shy = 0.5
curl -X GET "http://localhost:8000/vertical/0.5"

# Transformar figura nomeada
curl -X POST "http://localhost:8000/transformar-figura" \
  -H "Content-Type: application/json" \
  -d '{
    "figura": "Casa",
    "shx": 1.2,
    "shy": 0.4,
    "modo": "Ambos"
  }'

# Transformar pontos customizados
curl -X POST "http://localhost:8000/transformar" \
  -H "Content-Type: application/json" \
  -d '{
    "pontos": [
      {"x": 0, "y": 0},
      {"x": 1, "y": 0},
      {"x": 1, "y": 1},
      {"x": 0, "y": 1}
    ],
    "shx": 0.5,
    "shy": 0.3,
    "modo": "Ambos"
  }'

# Calcular matriz
curl -X POST "http://localhost:8000/matriz?modo=Ambos&shx=1.5&shy=0.5"
```

---

## Documentação automática

Após iniciar o servidor, acesse:
- **Swagger UI (recomendado):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Ambas permitem testar os endpoints diretamente no navegador.
