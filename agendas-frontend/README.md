# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## 📝 Backlog (Exemplo): Ideias para o Futuro!

Este é um exemplo de backlog, com algumas ideias para expandir e aprimorar o projeto:

1. **Backend:**

   * [X] Configurar projeto Django e Django REST Framework.
   * [X] Criar modelo `Agenda` com os campos especificados.
   * [X] Implementar serializers para o modelo `Agenda`.
   * [X] Implementar views (API endpoints) para CRUD de agendas.
   * [X] Implementar view para alteração de estado da agenda.
   * [X] Configurar paginação para a listagem de agendas.
   * [X] Adicionar documentação da API com Swagger/ReDoc.
   * [X] Escrever testes unitários para os endpoints da API.
   * [X] Criar script para popular o banco de dados com dados de teste.
   * [X] Dockerizar o backend.
   * [ ] **Adicionar Autenticação e Autorização:**  Implementar um sistema de autenticação e autorização usando JWT.
   * [X] **Adicionar Filtros para a Listagem de Agendas:**  Implementado com django-filter.
   * [X] **Adicionar Busca:** Implementado endpoint de busca por título e descrição.
   * [ ] **Adicionar Upload de Anexos:** Implementar sistema de upload de arquivos com AWS S3.
   * [X] **Logs:** Implementado sistema de logs com django-logging.
   * [X] **Validação Personalizada:** Implementada validação de conflitos de horário.
   * [ ] **Cache:** Implementar cache com Redis para melhorar performance.
   * [ ] **Testes de Integração:** Adicionar testes E2E com Cypress.
   * [ ] **Monitoramento:** Implementar monitoramento com Sentry.
   * [ ] **API Versioning:** Adicionar versionamento da API.

2. **Frontend:**

   * [X] Configurar projeto Nuxt 3.
   * [X] Criar layout básico da aplicação.
   * [X] Criar componente para listar agendas.
   * [X] Criar componente para exibir detalhes de uma agenda.
   * [X] Criar componente/formulário para criar uma nova agenda.
   * [X] Criar componente/formulário para editar uma agenda existente.
   * [X] Implementar a exclusão de agendas (com confirmação).
   * [X] Implementar a alteração de estado da agenda.
   * [X] Adicionar paginação à listagem de agendas.
   * [X] Adicionar tratamento de erros.
   * [X] Dockerizar o frontend.
   * [X] Adicionar calendário interativo.
   * [X] Implementar Dark Mode.
   * [X] Adicionar sistema de notificações.
   * [X] Adicionar busca e filtros.
   * [ ] **Testes Unitários:** Implementar com Vitest.
   * [ ] **Testes E2E:** Implementar com Cypress.
   * [ ] **Performance:** Otimizar carregamento e bundle size.
   * [ ] **PWA:** Implementar funcionalidades offline.
   * [X] **Acessibilidade:** Implementado seguindo WCAG.
   * [ ] **i18n:** Adicionar suporte a múltiplos idiomas.
   * [ ] **Analytics:** Implementar rastreamento de eventos.
   * [ ] **Micro-frontends:** Explorar arquitetura de micro-frontends.

3. **Integração:**

   * [X] Criar arquivo `docker-compose.yml`.
   * [X] Configurar o frontend para consumir a API.
   * [X] Configurar variáveis de ambiente.
   * [ ] **CI/CD:** Implementar pipeline com GitHub Actions.
   * [ ] **Monitoramento:** Implementar health checks.
   * [ ] **Backup:** Configurar backup automático do banco de dados.

4. **Documentação:**

   * [X] Escrever README.md detalhado.
   * [X] Documentar API com Swagger/ReDoc.
   * [X] Adicionar docstrings ao código.
   * [ ] **Guia de Contribuição:** Criar CONTRIBUTING.md.
   * [ ] **Changelog:** Manter CHANGELOG.md atualizado.
   * [ ] **Wiki:** Criar wiki com documentação extensa.

5. **DevOps:**

   * [X] Containerização com Docker.
   * [ ] **Kubernetes:** Preparar para deploy em K8s.
   * [ ] **Terraform:** Implementar IaC.
   * [ ] **Monitoramento:** Configurar Prometheus/Grafana.
   * [ ] **Logs:** Implementar ELK Stack.
   * [ ] **Security:** Realizar security scanning.
