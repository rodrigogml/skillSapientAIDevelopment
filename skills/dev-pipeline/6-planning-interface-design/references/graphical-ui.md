# Graphical UI Reference

Consultar esta referência para web, mobile web, desktop, Android e iOS.

## Estrutura e Navegação

- Definir hierarquia visual, regiões, ordem de leitura e prioridade das ações.
- Registrar rota, deep link, origem da navegação, retorno e comportamento do botão voltar.
- Para modificação, separar estado atual e mudança desejada.
- Referenciar design system e tokens existentes; justificar componente novo.

## Estados

Resolver cada estado canônico ou marcar `N/A — motivo`:

- `initial`;
- `loading`;
- `empty`;
- `ready`;
- `processing`;
- `success`;
- `validation-error`;
- `remote-error`;
- `offline`;
- `access-denied`;
- `partial-stale`.

Definir apresentação, ações permitidas e transição de saída. Não usar apenas “mostrar erro”; especificar conteúdo seguro, retry e preservação de dados digitados.

## Responsividade e Adaptação

- Usar os form factors e breakpoints declarados no catálogo ou design system.
- Explicar reflow, empilhamento, ocultação, priorização e navegação em cada form factor.
- Tratar orientação, safe areas, teclado virtual, pointer, touch e teclado físico quando aplicável.
- Não tratar Android/iOS nativo como simples breakpoint de web.

## Acessibilidade

- Seguir o baseline da constitution.
- Definir ordem de foco, foco inicial e retorno de foco.
- Declarar nomes acessíveis, landmarks, headings e anúncios dinâmicos.
- Preservar operação por teclado e leitor de tela nos fluxos críticos.
- Definir contraste, reduced motion, zoom e tamanho de alvo conforme o padrão do projeto.

## Conteúdo e Localização

- Usar termos canônicos e chaves de mensagem quando o projeto possuir i18n.
- Definir formatação de datas, horas, números, moeda e timezone.
- Considerar expansão de texto, pluralização e RTL quando suportado.
- Não colocar segredos ou dados sensíveis em telemetria, notificações ou mensagens de erro.

## Wireframes

Exigir wireframe para tela nova, navegação, hierarquia estrutural ou transformação responsiva ambígua. Manter baixa fidelidade e anotar IDs de interação, regiões e estados relevantes.
