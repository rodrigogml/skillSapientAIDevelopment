# CLI and TUI Reference

Consultar esta referência para comandos de terminal e interfaces textuais interativas.

## Contrato de Comando

- Definir nome, subcomandos, argumentos posicionais, flags e aliases.
- Especificar required/default, valores permitidos, repetição e precedência entre flag, variável de ambiente e arquivo de configuração.
- Referenciar o contrato técnico quando mantido em `contracts/`.

## Entrada e Interatividade

- Declarar stdin, prompts, confirmação e leitura de segredo sem echo.
- Fornecer modo não interativo para automação quando a operação o exigir.
- Definir comportamento quando não houver TTY, quando stdin estiver fechado e quando confirmação for recusada.

## Saída

- Separar stdout de stderr.
- Definir formatos humano e estruturado, como JSON, sem misturar logs ao payload estruturado.
- Especificar exit codes estáveis e o comportamento de `--help` e `--version`.
- Tratar cor, `NO_COLOR`, terminal estreito, wrapping e redirecionamento para arquivo.

## Estados e Falhas

- Mapear os estados canônicos para progresso, ausência de resultados, sucesso, validação, falha remota, offline e acesso negado.
- Definir cancelamento, timeout, retry, idempotência e interrupção por sinal quando aplicável.
- Preservar mensagens acionáveis sem expor segredos.

## TUI

- Definir atalhos, foco, navegação, resize, terminal mínimo e alternativa textual.
- Descrever atualização de regiões sem depender exclusivamente de cor.
- Dispensar wireframe formal somente quando a estrutura textual ficar inequívoca; um mapa ASCII pode ser usado quando necessário.
