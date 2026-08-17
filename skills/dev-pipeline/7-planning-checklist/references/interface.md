# Domínio: Interface

Itens exemplo para validar a qualidade do contrato técnico de superfícies humanas. Adaptar à feature e nunca testar a implementação.

## Cobertura de Superfícies

- Todas as superfícies declaradas na spec possuem `FULL`, `PARTIAL`, `DEFERRED` ou `N/A` no interface spec? [Completude]
- Escopos `PARTIAL` e `DEFERRED` descrevem explicitamente capacidades incluídas e excluídas? [Clareza]
- Diferenças intencionais de paridade estão documentadas sem conflito com a spec? [Consistência]

## Inventário e Estado Atual

- Toda tela, comando, diálogo, painel, notificação ou fluxo novo/modificado possui `INT-*` estável? [Rastreabilidade]
- Alterações em interfaces existentes identificam rota/comando/componente e comportamento atual? [Completude]
- Itens removidos definem impacto em navegação, automações, deep links ou documentação? [Cobertura]

## Comportamento e Estados

- Cada `INT-*` define ações, transições, permissões, validações e feedback? [Completude]
- Estados initial, loading, empty, ready, processing, success, validation-error, remote-error, offline, access-denied e partial-stale estão definidos ou justificados como N/A? [Cobertura]
- Ações destrutivas, retry e preservação de dados têm requisitos inequívocos? [Clareza]

## Responsividade e Adaptação

- Regras cobrem todos os form factors declarados no catálogo? [Cobertura]
- Reflow, priorização, navegação, orientação e métodos de entrada estão especificados? [Completude]
- Web responsiva e aplicativos nativos têm diferenças intencionais documentadas? [Consistência]

## Acessibilidade e Localização

- Requisitos seguem o baseline da constitution e do catálogo? [Constitution Alignment]
- Foco, teclado, leitor de tela, contraste, reduced motion e touch estão definidos quando aplicáveis? [Cobertura]
- Mensagens, formatos regionais, expansão de texto e RTL estão especificados para os locales suportados? [Cobertura]

## Contratos e Componentes

- Cada interação referencia contratos e campos consumidos sem duplicar a fonte de verdade externa? [Consistência]
- Componentes e tokens reutilizados ou novos apontam para o design system correto? [Rastreabilidade]
- Cache, stale data, atualização otimista e falhas remotas têm comportamento de interface definido? [Cobertura]

## Wireframes e Rastreabilidade

- Toda interação que exige wireframe possui artefato coerente com o texto? [Completude]
- O texto permanece explicitamente como fonte de verdade em caso de divergência visual? [Clareza]
- Cada `INT-*` mapeia para story/FR, success criteria e contracts aplicáveis? [Rastreabilidade]
