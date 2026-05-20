# SQL Quest

SQL Quest é um jogo para praticar SQL com missões narrativas. O jogador recebe um contexto, consulta o esquema disponível e escreve uma consulta SQL real. O backend executa a consulta em SQLite e valida o resultado contra uma resposta esperada, sem comparar o texto da SQL.

## Stack

- Frontend: React + Vite
- Visual: Tailwind CSS, Motion, Lucide React e CodeMirror
- Backend: FastAPI
- Banco: SQLite

## Rodar o backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_databases.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
```

Backend fixo: http://localhost:8002

## Rodar o frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend fixo: http://localhost:5173

## Rodar a aplicação completa

```bash
npm run dev:app
```

Backend fixo: http://localhost:8002
Frontend fixo: http://localhost:5173

O script falha se alguma dessas portas já estiver ocupada, para evitar usar um servidor antigo por engano.

## MVP atual

- 3 categorias iniciais: Saúde, Logística e Games.
- 2 missões por categoria.
- Validação por resultado retornado.
- Bloqueio de comandos de escrita e comandos perigosos.
- SQLite em modo somente leitura para execução das consultas do jogo.
- HUD de jogador com nível, XP, sequência e vidas.
- Terminal SQL com CodeMirror e destaque de sintaxe.
- Animações de entrada e feedback com Motion.

## Crescimento planejado

Adicione novas situações em `backend/app/data/scenarios.json` e crie/alimente o banco correspondente em `backend/scripts/seed_databases.py`. Cada situação deve apontar para um arquivo SQLite em `backend/app/data/databases`.

Para padronizar novas situações, use o blueprint em `docs/blueprint-novas-situacoes.md`.
