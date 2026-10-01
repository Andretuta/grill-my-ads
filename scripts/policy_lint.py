#!/usr/bin/env python3
"""Heuristic Meta ad-policy linter for ad copy (English + Portuguese). Stdlib only.

  policy_lint.py --text "Are you overweight? Guaranteed results!"
  policy_lint.py --file copy.txt          (one ad per blank-line-separated block)
  cat copy.txt | policy_lint.py
  policy_lint.py --selftest

Exit code 1 if any HIGH finding. Heuristic: a clean run is not policy approval.
"""
import argparse
import re
import sys

# (severity, rule, regex, fix hint)
RULES = [
    ("HIGH", "personal-attribute",
     r"\b(are|r) you\b[^.?!\n]{0,40}\b(fat|overweight|obese|depress\w*|anxious|anxiety|diabet\w*|in debt|broke|poor|"
     r"single|divorced|gay|lesbian|christian|muslim|jewish|old|bald|sick|pregnant|unemployed|addict\w*)\b",
     "Don't assert/imply the viewer's personal attributes; talk about the product or situation."),
    ("HIGH", "personal-attribute",
     r"\bvoc[eê]\s+(est[aá]|[eé]|anda|sofre|tem|vive|se sente)\b[^.?!\n]{0,40}\b(gord\w*|acima do peso|obes\w*|"
     r"deprimid\w*|ansios\w*|ansiedade|diab[eé]t\w*|endividad\w*|d[ií]vidas?|quebrad\w*|pobre|solteir\w*|divorciad\w*|"
     r"careca|doente|gr[aá]vida|desempregad\w*|viciad\w*|calv\w*)",
     "Don't assert/imply the viewer's personal attributes; talk about the product or situation."),
    ("HIGH", "personal-attribute",
     r"\b(tired of your|cansad[oa] d[aoe] sua?)\s+(belly|weight|fat|wrinkles|barriga|peso|gordura|rugas|celulite|dívida)",
     "Rephrase without targeting the viewer's body/finances."),
    ("HIGH", "guaranteed-results",
     r"\b(guarantee[ds]?|garantid[oa]s?|100% (effective|eficaz|garantido)|cures?|cura (definitiva|garantida)|"
     r"risk[- ]free returns?|lucro garantido|renda garantida)\b",
     "Remove guaranteed/absolute outcome claims (a money-back guarantee on the product is fine; say it precisely)."),
    ("HIGH", "weight-loss-claim",
     r"\b(lose|perca|perder|emagre\w*|elimin\w*)\b[^.\n]{0,20}\b\d+\s?(kg|lbs?|quilos|pounds)\b",
     "Specific weight-loss claims are restricted; remove numbers/timeframes."),
    ("HIGH", "before-after",
     r"\b(before\s*(and|&|/)\s*after|antes\s*(e|&|/)\s*depois)\b",
     "Before/after imagery/claims are banned for weight loss & anti-aging; avoid generally."),
    ("HIGH", "get-rich",
     r"\b(get rich|fique rico|dinheiro f[aá]cil|easy money|passive income guaranteed|turn \$?\d+ into|"
     r"transforme r?\$?\s?\d+ em)\b",
     "Unrealistic income/investment promises are prohibited."),
    ("MEDIUM", "fake-urgency",
     r"\b(only \d+ left|últimas? \d+ unidades|s[oó] hoje|today only|last chance|última chance|expires in \d+ ?(min|minutes|minutos))\b",
     "Only use urgency/scarcity if literally true; keep proof."),
    ("MEDIUM", "fake-ui",
     r"(\bclick (the )?play\b|\bclique no play\b|▶️|\byou have \d+ new (messages?|notifications?)\b|"
     r"\bvoc[eê] tem \d+ (novas? )?mensage)",
     "Fake buttons/notifications are deceptive."),
    ("MEDIUM", "platform-brand",
     r"\b(facebook|instagram|meta|whatsapp)\s+(approved|official|recommends|aprovad\w*|oficial|recomenda)\b",
     "Don't imply Meta endorsement."),
    ("MEDIUM", "restricted-category",
     r"\b(loan|empr[eé]stimo|cr[eé]dito|credit card|cart[aã]o de cr[eé]dito|crypto\w*|cripto\w*|bitcoin|casino|cassino|"
     r"aposta\w*|betting|bet\b|supplement\w*|suplement\w*|vaga de emprego|job opening|hiring|aluguel|im[oó]vel|mortgage)\b",
     "Possible restricted/special category: check policy + special_ad_categories."),
    ("LOW", "sensational",
     r"(!{2,}|\b[A-ZÀ-Ú]{6,}\b(?:\s+\b[A-ZÀ-Ú]{4,}\b){2,})",
     "Tone down caps/exclamations."),
    ("LOW", "generic-language",
     r"\b(streamline your workflow|game[- ]changer|revolutionary|revolucion[aá]ri\w*|next[- ]level|best in class|"
     r"o melhor do mercado|solução completa)\b",
     "Generic marketing language; be specific (number, result, demo)."),
]
COMPILED = [(s, n, re.compile(r, re.IGNORECASE if n != "sensational" else 0), h) for s, n, r, h in RULES]


def lint(text):
    found = []
    for sev, name, rx, hint in COMPILED:
        for m in rx.finditer(text):
            found.append({"severity": sev, "rule": name, "match": m.group(0).strip(), "hint": hint})
    return found


def selftest():
    bad = [
        ("Are you overweight? Try this.", "personal-attribute"),
        ("Você está endividado? Fale com a gente", "personal-attribute"),
        ("Cansado da sua barriga?", "personal-attribute"),
        ("Resultado garantido em 7 dias", "guaranteed-results"),
        ("Perca 10kg em um mês", "weight-loss-claim"),
        ("Veja o antes e depois", "before-after"),
        ("Últimas 3 unidades!", "fake-urgency"),
        ("Empréstimo rápido", "restricted-category"),
        ("This is a game-changer", "generic-language"),
    ]
    for text, rule in bad:
        rules = {f["rule"] for f in lint(text)}
        assert rule in rules, (text, rules)
    clean = "Cupom de 20% no app hoje. Veja como funciona em 15 segundos."
    assert not [f for f in lint(clean) if f["severity"] == "HIGH"], lint(clean)
    print("policy_lint.py selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text"); p.add_argument("--file")
    a = p.parse_args()
    raw = a.text if a.text is not None else (open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read())
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    worst = False
    for i, block in enumerate(blocks, 1):
        found = lint(block)
        print(f"## Ad {i}: {'OK' if not found else str(len(found)) + ' finding(s)'}")
        for f in found:
            print(f"- [{f['severity']}] {f['rule']}: \"{f['match']}\" -> {f['hint']}")
            worst |= f["severity"] == "HIGH"
    print("\nHeuristic only; final check is Meta review / Advertising Standards.")
    sys.exit(1 if worst else 0)


if __name__ == "__main__":
    main()
