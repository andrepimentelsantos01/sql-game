# Blueprint para novas situações

Use este blueprint sempre que for criar uma nova situação para o SQL Quest. A situação precisa funcionar como um caso profissional simulado: o jogador recebe um contexto, consulta um banco SQLite real e precisa escrever uma query que gere a resposta esperada.

## Elementos obrigatórios

### Categoria

Área profissional da situação.

Exemplos:

- Saúde
- Tecnologia
- Esporte
- Indústria
- Logística
- Finanças
- Educação
- Games
- Arte
- Agricultura

### Nível da situação

Complexidade esperada da consulta.

Use um destes níveis:

- Júnior: filtros simples, ordenação, `LIMIT`, agregações básicas ou uma única tabela.
- Pleno: `JOIN`, `GROUP BY`, métricas calculadas, filtros por data, subconsultas simples ou múltiplas tabelas.
- Sênior: múltiplos `JOINs`, CTEs, janelas analíticas, regras de negócio com várias etapas ou validações mais exigentes.

No arquivo `backend/app/data/scenarios.json`, o campo equivalente é `difficulty`. Se o app ainda estiver usando os valores antigos, mantenha consistência com a interface atual ou atualize a conversão antes de trocar a nomenclatura.

### Situação

Descrição narrativa da situação simulada. Ela deve explicar:

- Quem está pedindo a análise.
- Qual problema precisa ser investigado.
- Qual decisão será apoiada pela consulta SQL.
- Qual recorte deve ser considerado, quando houver datas, status ou filtros.

Boa situação:

> Uma rede de clínicas quer identificar quais especialidades têm maior tempo médio de espera em consultas realizadas, para priorizar a contratação de novos profissionais.

Situação fraca:

> Consulte as especialidades.

### Banco de dados

Banco SQLite simulado com schema e dados necessários para executar a situação.

Defina:

- Nome do arquivo `.db`, salvo em `backend/app/data/databases`.
- Tabelas necessárias.
- Colunas, tipos e chaves.
- Dados de exemplo suficientes para validar a consulta.
- Casos de borda que provem a regra da situação, como status cancelado, data fora do período ou registro que não deve entrar no cálculo.

Os bancos são criados e populados em `backend/scripts/seed_databases.py`. Sempre que criar ou alterar um banco, execute novamente o script de seed para regenerar os arquivos SQLite.

### Resposta adequada

Resposta esperada da situação, incluindo:

- Query correta em SQL.
- Colunas esperadas.
- Linhas esperadas.
- Ordenação esperada.
- Arredondamentos, aliases e limites necessários.

O jogo valida o resultado retornado, não apenas o texto da SQL. Mesmo assim, a `expected_sql` precisa ser uma consulta clara, determinística e representativa da solução ideal.

## Modelo de documentação da situação

Preencha este modelo antes de implementar:

````md
## [categoria] - [título da situação]

Categoria: [área profissional]

Nível da situação: [Júnior | Pleno | Sênior]

Situação:
[descrição narrativa do problema]

Objetivo da consulta:
[o que o jogador precisa retornar]

Banco de dados:
- Arquivo: [nome_do_banco.db]
- Tabelas:
  - [tabela_1]: [descrição]
  - [tabela_2]: [descrição]
- Schema:

```sql
CREATE TABLE exemplo (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);
```

Dados relevantes:

```sql
INSERT INTO exemplo (id, nome) VALUES
(1, 'Registro de exemplo');
```

Resposta adequada:

```sql
SELECT nome
FROM exemplo
ORDER BY nome;
```

Resultado esperado:

| nome |
| --- |
| Registro de exemplo |

Dica:
[dica curta para orientar sem entregar a resposta inteira]
````

## Como implementar no projeto

1. Adicione ou atualize o banco em `backend/scripts/seed_databases.py`.
2. Garanta que o banco seja salvo em `backend/app/data/databases`.
3. Adicione a nova situação em `backend/app/data/scenarios.json`.
4. Use um `id` único e previsível, como `tecnologia_001`.
5. Preencha `category`, `title`, `difficulty`, `database`, `story`, `objective`, `expected_sql`, `expected_answer` e `hint`.
6. Execute `python backend/scripts/seed_databases.py` a partir da raiz do projeto.
7. Teste a `expected_sql` no banco gerado e confirme se o resultado bate com a resposta adequada.

## Exemplo completo

### Tecnologia - Incidentes críticos

Categoria: Tecnologia

Nível da situação: Pleno

Situação:
Uma empresa SaaS quer descobrir quais serviços concentraram mais incidentes críticos no último mês fechado. O time de confiabilidade vai usar o resultado para priorizar ações de estabilidade.

Objetivo da consulta:
Retorne o nome do serviço e a quantidade de incidentes críticos abertos entre `2026-04-01` e `2026-05-01`, ordenando da maior quantidade para a menor.

Banco de dados:

- Arquivo: `tecnologia.db`
- Tabela `servicos`: catálogo de serviços monitorados.
- Tabela `incidentes`: registros de incidentes por serviço.

Schema:

```sql
CREATE TABLE servicos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    squad TEXT NOT NULL
);

CREATE TABLE incidentes (
    id INTEGER PRIMARY KEY,
    servico_id INTEGER NOT NULL,
    severidade TEXT NOT NULL,
    aberto_em TEXT NOT NULL,
    FOREIGN KEY (servico_id) REFERENCES servicos(id)
);
```

Dados relevantes:

```sql
INSERT INTO servicos (id, nome, squad) VALUES
(1, 'Pagamentos', 'Core'),
(2, 'Autenticação', 'Plataforma'),
(3, 'Relatórios', 'Dados');

INSERT INTO incidentes (servico_id, severidade, aberto_em) VALUES
(1, 'crítica', '2026-04-03'),
(1, 'crítica', '2026-04-18'),
(1, 'média', '2026-04-20'),
(2, 'crítica', '2026-04-12'),
(2, 'baixa', '2026-04-15'),
(3, 'crítica', '2026-03-29');
```

Resposta adequada:

```sql
SELECT s.nome AS servico, COUNT(*) AS incidentes_criticos
FROM servicos s
JOIN incidentes i ON i.servico_id = s.id
WHERE i.severidade = 'crítica'
  AND i.aberto_em >= '2026-04-01'
  AND i.aberto_em < '2026-05-01'
GROUP BY s.nome
ORDER BY incidentes_criticos DESC;
```

Resultado esperado:

| servico | incidentes_criticos |
| --- | ---: |
| Pagamentos | 2 |
| Autenticação | 1 |

Dica:
Junte serviços com incidentes, filtre severidade e período, depois agrupe por serviço.

Entrada equivalente em `scenarios.json`:

```json
{
  "id": "tecnologia_001",
  "category": "Tecnologia",
  "title": "Incidentes críticos",
  "difficulty": "Pleno",
  "database": "tecnologia.db",
  "story": "Uma empresa SaaS quer descobrir quais serviços concentraram mais incidentes críticos no último mês fechado. O time de confiabilidade vai usar o resultado para priorizar ações de estabilidade.",
  "objective": "Retorne o nome do serviço e a quantidade de incidentes críticos abertos entre 2026-04-01 e 2026-05-01, ordenando da maior quantidade para a menor.",
  "expected_sql": "SELECT s.nome AS servico, COUNT(*) AS incidentes_criticos FROM servicos s JOIN incidentes i ON i.servico_id = s.id WHERE i.severidade = 'crítica' AND i.aberto_em >= '2026-04-01' AND i.aberto_em < '2026-05-01' GROUP BY s.nome ORDER BY incidentes_criticos DESC;",
  "expected_answer": {
    "query": "SELECT s.nome AS servico, COUNT(*) AS incidentes_criticos FROM servicos s JOIN incidentes i ON i.servico_id = s.id WHERE i.severidade = 'crítica' AND i.aberto_em >= '2026-04-01' AND i.aberto_em < '2026-05-01' GROUP BY s.nome ORDER BY incidentes_criticos DESC;",
    "result": {
      "columns": ["servico", "incidentes_criticos"],
      "rows": [
        ["Pagamentos", 2],
        ["Autenticação", 1]
      ]
    }
  },
  "hint": "Junte serviços com incidentes, filtre severidade e período, depois agrupe por serviço."
}
```

## Checklist de qualidade

- A categoria está clara e representa uma área profissional.
- O nível combina com a complexidade real da query.
- A situação parece um pedido de análise plausível.
- O banco contém todos os dados necessários para resolver o caso.
- Existem registros que testam filtros importantes.
- A query esperada retorna resultado determinístico.
- A ordenação está explícita quando houver múltiplas linhas.
- Aliases e arredondamentos estão definidos no objetivo.
- A dica ajuda sem entregar a query completa.
- O cenário foi testado no SQLite gerado.
