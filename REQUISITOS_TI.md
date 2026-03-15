# Requisitos Não Funcionais - SmartEstoque
**Responsável:** Jessé Benício
**Data de Início:** 15/03/2026

## 1. Segurança (Alta Prioridade)
- **Proteção de Credenciais:** O sistema não deve expor senhas de banco de dados no código principal. Utilizaremos variáveis de ambiente (.env).
- **Controle de Acesso:** Apenas usuários autenticados podem acessar as rotas de edição e exclusão de produtos.
- **Integridade:** O banco de dados MySQL deve garantir que não existam registros de saída sem um produto vinculado.

## 2. Desempenho
- **Tempo de Resposta:** As consultas de estoque devem retornar resultados em menos de 2 segundos.
- **Escalabilidade:** O motor Flask deve ser configurado para suportar múltiplos acessos simultâneos sem travar a conexão com o MySQL.

## 3. Disponibilidade
- O sistema deve ser projetado para operar em ambiente web com 99% de disponibilidade para o pequeno comerciante.