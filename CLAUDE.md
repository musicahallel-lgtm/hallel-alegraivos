# Hallel Music – Instruções para Claude

## Projeto
App web de gerenciamento musical do Ministério de Música Hallel.
Arquivo principal: `/Users/leoecarla/hallel-music/index.html` (único arquivo, ~4700 linhas)
Deploy: GitHub Pages em `https://musicahallel-lgtm.github.io/hallel-alegraivos`

## Health Check Automático
No início de cada sessão, um script (`health-check.sh`) escaneia o `index.html` em busca
de problemas de performance e CSS. Se houver achados, eles aparecem como contexto adicional.

**Quando encontrar problemas no health check:**
- Corrija-os proativamente durante a sessão, especialmente se forem `transition:all`
  ou `backdrop-filter` com blur alto
- Avise o usuário resumidamente o que foi corrigido
- Não pergunte confirmação para correções de performance menores (ex: transition:all)

## Paleta de cores atual
- Verde principal: `#00963F` (`--purple`)
- Laranja: `#F15A24` (`--gold`)
- Background: `#080810` (`--bg`)
- Header: `linear-gradient(118deg, #002912 0%, #00963F 58%, #a83800 100%)`

## Padrões de código
- State global: objeto `S` + `persist()` debounced + `render()` batched via rAF
- Sem frameworks — vanilla JS puro
- `contain: layout style` nos cards para performance
- Bottom nav fixo em mobile (<640px) via `bottomNav()` function
- Login card: fundo branco (`#ffffff`) com letras escuras

## Boas práticas para edições
- Prefira `transition: background-color .15s, box-shadow .15s, transform .15s` em vez de `transition: all`
- `backdrop-filter: blur(Xpx)` — manter ≤ 8px
- Testar no preview antes de commitar
