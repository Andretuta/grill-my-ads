<p align="center">
  <img src="assets/icon.png" alt="ícone grill-my-ads" width="160">
</p>

<h1 align="center">grill-my-ads</h1>

<p align="center">
  <b>Um gestor de tráfego implacável no seu terminal.</b><br>
  Uma skill do Claude que te entrevista sobre o produto (e, se você pedir, lê o seu repositório) e monta anúncios no Meta (Facebook · Instagram · WhatsApp · Messenger) pelo MCP oficial do Meta Ads, sempre como rascunho. Só publica com o seu "ok".
</p>

<p align="center">
  <a href="README.md">🇺🇸 Read in English</a>
  <br><br><a href="https://m8ven.ai/mcp/andretuta-grill-my-ads-1cefy2?s=readme"><img src="https://m8ven.ai/badge/mcp/andretuta-grill-my-ads-1cefy2?variant=verified&v=f45c281cd97490ed874dbea0b8e2ea3e" alt="M8ven Verified"></a>
</p>

---

## Por quê

A maior parte da verba de anúncio é perdida antes da primeira impressão: objetivo errado, nenhuma conta de margem, a página inicial como destino, cinco cópias do mesmo criativo. O `grill-my-ads` te entrevista como um gestor de tráfego sênior *antes* de gastar um centavo, faz a pesquisa sozinho e só depois monta a campanha.

## O que faz

| Comando | O que acontece |
|---|---|
| `/grill-my-ads` | Te entrevista em rodadas, com perguntas numeradas e uma resposta recomendada em cada uma. Pesquisa o objetivo e o destino mais viáveis e escreve de 3 a 5 conceitos realmente diferentes. Usa as suas fotos/vídeos ou escreve um roteiro de vídeo UGC. Monta campanha, conjunto, criativos e anúncios **em rascunho**, mostra as prévias e **só publica com um "ok" explícito** |
| `/grill-my-ads --repo` | O mesmo fluxo, mas antes lê o projeto atual (landing page, preços, rotas, fluxo real do usuário) para adiantar a entrevista e gerar o vídeo do produto a partir do código (via [brag](https://github.com/latent-spaces/brag)). **Só quando você pede**: o padrão nunca mexe nos seus arquivos |
| `/grill-my-ads audit` | Auditoria da conta, só leitura: cerca de 40 checagens (pixel/CAPI, diversidade e fadiga de criativo, estrutura, público, compliance). Devolve nota de 0 a 100, conceito de A a F e as correções rápidas |
| `/grill-my-ads roi` | Cruza o gasto no Meta com os **seus** dados (pedidos, leads qualificados, membros que ficaram). Calcula CPA real, ROAS comparado ao ROAS de equilíbrio e lucro, e diz por anúncio se é para ESCALAR, MANTER ou CORTAR |

### Destaques
- **Fatos ela busca, decisões são suas.** Conta, página, IG, pixel e histórico vêm do MCP. Orçamento, oferta e aprovação ela pergunta.
- **Funciona para qualquer produto.** Só a entrevista já basta: café, curso, serviço local, SaaS.
- **Do repositório ao anúncio, só se você pedir.** Com `--repo`, lê a landing page, os preços, as rotas e o fluxo real do usuário, e nunca `.env`, chaves ou segredos. Sem a flag, não lê nenhum arquivo seu.
- **Criativos em vídeo.** Usa a sua mídia, escreve um roteiro de UGC ou, com `--repo`, renderiza um vídeo do produto em 9:16 e 4:5 a partir do código.
- **Segurança em primeiro lugar:**
  - tudo nasce em rascunho/PAUSADO;
  - pausa, nunca apaga;
  - nunca deduz o orçamento nem inventa IDs de interesse;
  - aumenta o orçamento no máximo 20% por vez;
  - passa todo texto por um linter de política;
  - sempre pergunta sobre a divulgação de uso de IA.
- **Atualizada (2026):**
  - unificação do Advantage+;
  - diversidade de criativos (Andromeda);
  - fim das janelas de atribuição por visualização de 7 e 28 dias (jan/2026);
  - repasse de 12,15% de impostos no Brasil;
  - LGPD/GDPR.

## Requisitos

- [Claude Code](https://claude.com/claude-code) ou Claude.ai (Personalizar → Skills)
- **MCP oficial do Meta Ads** conectado: `https://mcp.facebook.com/ads`
- Python 3.9+ (para os scripts, só biblioteca padrão)
- Opcional, para vídeo: Node 18+, ffmpeg e a skill [brag](https://github.com/latent-spaces/brag)

## Instalação

**Claude Code**
```bash
git clone https://github.com/Andretuta/grill-my-ads ~/.claude/skills/grill-my-ads
```

**Claude.ai:** baixe o repositório como ZIP e envie em *Personalizar → Skills*.

Depois é só digitar `/grill-my-ads` (ou "me entrevista pra criar um anúncio"). Dentro de um projeto de código, use `/grill-my-ads --repo` para montar o anúncio a partir do código.

## Scripts auxiliares

Python só com biblioteca padrão, cada um com `--selftest`.

| Script | Exemplo |
|---|---|
| `scripts/budget.py` | `python scripts/budget.py min --cpa 40`: orçamento diário mínimo para sair do aprendizado (também em centavos) |
| `scripts/policy_lint.py` | `python scripts/policy_lint.py --file copy.txt`: aponta atributos pessoais, promessas garantidas, antes/depois etc. (PT + EN) |
| `scripts/audit_score.py` | `python scripts/audit_score.py checks.json`: nota ponderada, conceito e correções rápidas |
| `scripts/roi.py` | `python scripts/roi.py report --meta meta.csv --biz biz.csv --margin 0.45 --tax 0.1215` |
| `scripts/utm.py` | `python scripts/utm.py exemplo.com/oferta`: template de UTM padrão do Meta |

## Estrutura

```
SKILL.md              roteador + fluxo de criação + regras inegociáveis
references/           catálogo do MCP, árvore de entrevista, árvore de viabilidade, criativo,
                      políticas, tracking, estrutura e escala, auditoria, ROI, notas regionais, fontes
scripts/              budget · policy_lint · audit_score · roi · utm
assets/               templates de contexto do produto, brief e roteiro de vídeo
examples/             sessões completas de exemplo + entradas/saídas de exemplo
```

> Os arquivos da skill estão em inglês, mas ela responde no idioma de quem usa. Em português, a conversa toda acontece em português.

## Exemplos

Veja [`examples/`](examples/):
- uma sessão completa de entrevista, em que a skill contesta um orçamento baixo e monta a tabela de viabilidade;
- uma sessão com `--repo`, lendo o projeto e gerando o vídeo;
- entradas e saídas esperadas para ROI, auditoria e linter de política.

## Aviso

Este projeto não tem vínculo com a Meta. Os benchmarks são faixas, marcadas como oficiais [OF] ou de prática de mercado [PR], e não são garantia de resultado. A responsabilidade pelo gasto, pelo cumprimento das políticas e pela privacidade é sua. O linter de política é uma heurística, não uma aprovação.

## Créditos

Baseado em ideias de:
- [Digitizers/meta-ads-mcp](https://github.com/Digitizers/meta-ads-mcp) (MIT-0)
- [claude-ads](https://github.com/Hainrixz/claude-ads) (MIT)
- [latent-spaces/brag](https://github.com/latent-spaces/brag) (MIT)
- a técnica [grilling](https://github.com/mattpocock/skills) do Matt Pocock
- e outros projetos.

Veja [LICENSES.md](LICENSES.md).

## Licença

[MIT](LICENSE)
