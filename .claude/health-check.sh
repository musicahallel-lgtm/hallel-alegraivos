#!/usr/bin/env bash
# Hallel Music – CSS/performance health check
# Runs at SessionStart and injects findings into Claude's context.

FILE="/Users/leoecarla/hallel-music/index.html"
ISSUES=()

if [[ ! -f "$FILE" ]]; then
  echo '{}'; exit 0
fi

# ── 1. transition:all ─────────────────────────────────────────────────────────
TA=$(grep -c 'transition[[:space:]]*:[[:space:]]*all' "$FILE" 2>/dev/null); TA=${TA:-0}
if (( TA > 0 )); then
  LINES=$(grep -n 'transition[[:space:]]*:[[:space:]]*all' "$FILE" | head -5 | cut -d: -f1 | tr '\n' ',' | sed 's/,$//')
  ISSUES+=("⚠️  transition:all encontrado ${TA}x (linhas ${LINES}) — substituir por propriedades específicas")
fi

# ── 2. backdrop-filter blur alto (>8px) ───────────────────────────────────────
BIG_BLUR=0
while IFS= read -r val; do
  if (( val > 8 )); then (( BIG_BLUR++ )); fi
done < <(grep -oE 'backdrop-filter[^;]*blur\([0-9]+px\)' "$FILE" | grep -oE 'blur\([0-9]+' | grep -oE '[0-9]+')
if (( BIG_BLUR > 0 )); then
  VALS=$(grep -oE 'backdrop-filter[^;]*blur\([0-9]+px\)' "$FILE" | head -2 | tr '\n' '|')
  ISSUES+=("⚠️  backdrop-filter com blur>8px encontrado ${BIG_BLUR}x — considerar ≤8px: ${VALS}")
fi

# ── 3. will-change abusivo ─────────────────────────────────────────────────────
WC=$(grep -c 'will-change' "$FILE" 2>/dev/null); WC=${WC:-0}
if (( WC > 3 )); then
  ISSUES+=("⚠️  will-change usado ${WC}x — use apenas em elementos que realmente animam")
fi

# ── 4. console.log esquecido ──────────────────────────────────────────────────
CL=$(grep -c 'console\.log' "$FILE" 2>/dev/null); CL=${CL:-0}
if (( CL > 0 )); then
  ISSUES+=("ℹ️  ${CL} console.log() encontrado(s) no arquivo de produção")
fi

# ── Output ────────────────────────────────────────────────────────────────────
if (( ${#ISSUES[@]} == 0 )); then
  echo '{}'
else
  MSG="🔍 Health Check Automático – index.html\n\n"
  for i in "${ISSUES[@]}"; do
    MSG+="• $i\n"
  done
  MSG+="\nCorrija esses pontos quando relevante durante a sessão."
  JSON_MSG=$(printf '%s' "$MSG" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$JSON_MSG"
fi
