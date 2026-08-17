# Interface Traceability Reference

## Cadeia Obrigatória

Manter a cadeia:

```text
SURF-* -> INT-* -> User Story/FR -> Contract -> Task -> Verification Evidence
```

Na etapa de Interface Design, preencher a cadeia até contracts. As etapas de Create Tasks, Analyze, Execute Task e Review Task completam tasks e evidências.

## Cobertura por Superfície

- `FULL`: exigir interação para todo comportamento funcional da feature aplicável à superfície.
- `PARTIAL`: listar explicitamente comportamentos incluídos e excluídos.
- `DEFERRED`: não gerar task na entrega atual; registrar motivo e horizonte quando conhecido.
- `N/A`: justificar por que a capacidade não faz sentido naquela superfície.

Não inferir que “web responsiva” cria automaticamente paridade com Android ou iOS.

## Cobertura por Interação

Cada `INT-*` deve:

- pertencer a exatamente uma `SURF-*`;
- existir no inventário e na seção de detalhes;
- mapear para pelo menos uma story ou requisito funcional;
- referenciar contrato quando consumir API, evento ou comando externo;
- receber task explícita quando a cobertura for `FULL` ou `PARTIAL`.

## Severidade Downstream

- Superfície `FULL` sem interação ou task: `CRITICAL` quando bloquear a feature baseline; caso contrário, `HIGH`.
- Interação sem detalhe, contrato ou rastreabilidade: `HIGH`.
- Estado, responsividade ou acessibilidade parcialmente definidos: `MEDIUM` ou `HIGH`, conforme impacto.
- Diferença intencional entre superfícies documentada: não reportar como drift.
