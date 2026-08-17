---
name: dev-pipeline-6-planning-interface-design
description: Create an implementation-ready specification for human-facing interaction surfaces after a feature spec and technical plan are clear. Use for new or changed web, responsive web, desktop, Android, iOS, CLI, or TUI experiences that need screen or command inventories, behavior and state definitions, responsive/adaptive rules, accessibility, contract mapping, conditional wireframes, and traceability before checklist and task creation. Skip for headless features, API/event contracts without human interaction, implementation, and visual-only review of finished code.
---

# Dev Pipeline - 6. Planning - Interface Design

## Overview

Produzir o contrato técnico de interação de uma feature sem implementar código. Converter a cobertura funcional da spec e as decisões arquiteturais do plan em telas, comandos, estados e regras verificáveis.

## Pré-requisitos

Exigir:

- `docs/specs/{feature-short-name}/spec.md` claro;
- `docs/specs/{feature-short-name}/plan.md` com stack e contratos definidos.

Carregar, quando existirem:

- `docs/architecture/interaction-surfaces.md`;
- `docs/constitution.md`;
- `docs/specs/{feature-short-name}/contracts/*.md`;
- `docs/specs/{feature-short-name}/data-model.md`;
- telas, componentes, rotas e comandos existentes afetados.

Se faltar decisão funcional, retornar à `Dev Pipeline - 4. Specification - Clarify`. Se faltar decisão de tecnologia, arquitetura, design system ou contrato, retornar à `Dev Pipeline - 5. Planning - Plan`.

## Output Contract

Quando houver superfície humana afetada, criar:

```text
docs/specs/{feature-short-name}/interface-spec.md
```

Usar `templates/interface-spec.md`. Permitir wireframes em `docs/specs/{feature-short-name}/wireframes/` quando exigidos.

Quando a feature for headless, reportar `N/A — sem superfície de interação humana` e não criar `interface-spec.md` vazio.

Tratar o texto de `interface-spec.md` como fonte de verdade. Wireframes ilustram o texto e nunca o substituem.

## Workflow

1. **Aplicabilidade**: determinar se a feature cria, altera ou remove uma interação humana.
2. **Contexto**: carregar spec, plan, catálogo de superfícies, contratos e implementação existente.
3. **Inventário**: mapear superfícies e itens de interação afetados.
4. **Clarificação**: perguntar apenas decisões materiais ainda não inferíveis.
5. **Especificação**: detalhar cada item e sua rastreabilidade.
6. **Validação**: executar o gate determinístico e revisar consistência semântica.
7. **Relatório**: listar artefato, cobertura, wireframes e próximos passos.

## 1. Aplicabilidade

Considerar superfície humana:

- CLI ou TUI;
- aplicativo desktop;
- web desktop;
- web responsiva ou mobile web;
- aplicativo Android;
- aplicativo iOS;
- outra interface operada diretamente por pessoa.

Não considerar superfície humana:

- API, webhook, evento ou fila consumidos apenas por sistemas;
- scheduler ou job sem comando/tela operacional;
- alteração interna sem efeito observável por usuário.

APIs, eventos e webhooks permanecem em `contracts/`; apenas referenciá-los na interação que os consome.

## 2. Contexto e Estado Atual

Antes de especificar alteração em interface existente:

1. localizar a rota, tela, componente, menu, comando ou handler real;
2. registrar o path ou identificador atual;
3. distinguir explicitamente comportamento atual e comportamento desejado;
4. capturar screenshot de referência quando o sistema puder ser executado; caso contrário, registrar evidência textual e paths;
5. reutilizar componentes e padrões existentes antes de propor novos.

Não inventar uma segunda arquitetura de navegação, design system ou convenção de comandos quando o projeto já possuir padrão compatível.

## 3. Cobertura e Identificadores

Usar um ID estável do catálogo, por exemplo `SURF-WEB-ADMIN` ou `SURF-IOS-CUSTOMER`.

Classificar a cobertura da feature por superfície:

- `FULL`: todo o escopo da feature entra nesta entrega;
- `PARTIAL`: somente o subconjunto explicitado entra nesta entrega;
- `DEFERRED`: a superfície é relevante, mas ficou para entrega futura;
- `N/A`: a feature não se aplica à superfície.

Não presumir paridade entre superfícies. Explicar o subconjunto de `PARTIAL` e a razão de `DEFERRED`.

Identificar cada tela, diálogo, painel, notificação, comando ou fluxo com `INT-<SURFACE>-NNN`, por exemplo `INT-WEB-001` e `INT-CLI-001`.

Classificar a mudança como `NEW`, `MODIFIED`, `REMOVED` ou `UNCHANGED`.

## 4. Clarificação

Perguntar uma decisão por vez, no máximo 7, somente quando a resposta alterar comportamento, arquitetura já aprovada, acessibilidade, decomposição de tarefas ou estratégia de validação.

Priorizar:

1. superfícies e cobertura;
2. atores, permissões e ações críticas;
3. navegação e transições;
4. estados de erro, vazio, offline e processamento;
5. responsividade, adaptação e métodos de entrada;
6. acessibilidade e localização;
7. telemetria ou detalhes visuais não inferíveis.

Não usar perguntas para escolher tecnologia que pertence ao plan nem para redefinir requisito funcional que pertence à spec.

## 5. Especificação

Preencher o template por completo. Para cada `INT-*`, declarar:

- superfície, tipo e mudança;
- propósito, atores, permissões e ponto de entrada;
- hierarquia do conteúdo e dados exibidos;
- ações, transições, validações e feedback;
- todos os estados canônicos, marcando `N/A — motivo` quando inaplicável;
- comportamento responsivo/adaptativo e métodos de entrada;
- acessibilidade e localização;
- componentes, tokens e design system reutilizados ou novos;
- integrações e contratos, sem duplicar o contrato externo;
- telemetria;
- necessidade e localização do wireframe;
- stories, requisitos, critérios de sucesso e contratos relacionados.

Consultar conforme a superfície:

- UI gráfica: `references/graphical-ui.md`;
- CLI/TUI: `references/cli-tui.md`;
- cobertura e rastreabilidade: `references/traceability.md`.

## 6. Wireframes

Exigir wireframe de baixa fidelidade quando houver:

- tela gráfica nova;
- alteração estrutural de layout;
- mudança de navegação ou hierarquia da informação;
- transformação responsiva que não fique inequívoca em texto.

Dispensar wireframe para mudança isolada de texto, validação, estilo simples ou CLI/TUI.

Registrar `REQUIRED`, `OPTIONAL` ou `N/A` em cada interação. Quando `REQUIRED`, incluir diagrama no documento ou path relativo em `wireframes/`.

## 7. Validação

Executar:

```bash
python scripts/validate-interface-spec.py docs/specs/{feature-short-name}/interface-spec.md
```

Se estiver fora da pasta da skill, usar o path absoluto do script.

Além do script, confirmar semanticamente:

- toda superfície `FULL` ou `PARTIAL` possui ao menos um `INT-*`;
- todo item do inventário possui detalhe e rastreabilidade;
- todo estado canônico foi definido ou justificado como não aplicável;
- wireframes obrigatórios existem;
- nenhuma decisão contradiz spec, plan, constitution ou contracts;
- não restam `TODO`, placeholders ou `[NEEDS CLARIFICATION]`.

Não prosseguir para checklist ou backlog com falha de validação.

## 8. Relatório

Reportar:

```markdown
## Interface Design Concluído

**Feature**: [nome]
**Arquivo**: docs/specs/[feature]/interface-spec.md
**Superfícies**: [N]
**Interações**: [N]
**Wireframes obrigatórios**: [N]
**Validação**: PASS

### Próximos Passos

1. `Dev Pipeline - 7. Planning - Checklist` — executar domínios `interface` e `ux` quando aplicável.
2. `Dev Pipeline - 8. Implementation - Create Tasks` — decompor cada `INT-*` em trabalho rastreável.
3. `Dev Pipeline - 9. Implementation - Analyze` — validar cobertura cross-artifact após criar o backlog.
```

## Regras Importantes

- Não implementar código nesta etapa.
- Não transformar wireframe em fonte de verdade.
- Não impor paridade entre canais sem requisito explícito.
- Não duplicar payloads completos já mantidos em `contracts/`.
- Não criar `interface-spec.md` com conteúdo N/A para feature headless.
- Não deixar decisões materiais para a execução.
