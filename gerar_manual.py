# -*- coding: utf-8 -*-
"""Gera o Manual do Membro — Ministério de Música Hallel (PDF)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.pdfgen import canvas
import re

# A fonte padrão do PDF não tem emoji — removemos para não virar quadradinho.
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF"
    "\U0001F1E6-\U0001F1FF←-⇿⌀-⏿⬀-⯿▀-◿️⃣]"
)
def _clean(t):
    return re.sub(r"\s{2,}", " ", _EMOJI.sub("", t)).strip()

_RealParagraph = Paragraph
def Paragraph(text, *a, **k):   # noqa: N802 — patch para limpar emoji
    return _RealParagraph(_clean(text), *a, **k)

# ── Paleta Hallel ──
VERDE      = colors.HexColor("#00963F")
VERDE_ESC  = colors.HexColor("#006b2d")
LARANJA    = colors.HexColor("#F15A24")
CINZA      = colors.HexColor("#555555")
CINZA_CL   = colors.HexColor("#888888")
BG_BOX     = colors.HexColor("#f0faf4")
BG_DICA    = colors.HexColor("#FFF7E8")

LOGO = "icon-512.png"

styles = getSampleStyleSheet()

def S(name, **kw):
    kw.setdefault('parent', styles['Normal'])
    return ParagraphStyle(name, **kw)

st_h1 = S('h1', fontName='Helvetica-Bold', fontSize=17, textColor=VERDE,
          spaceBefore=18, spaceAfter=6, leading=21)
st_h2 = S('h2', fontName='Helvetica-Bold', fontSize=13, textColor=VERDE_ESC,
          spaceBefore=10, spaceAfter=3, leading=16)
st_body = S('body', fontName='Helvetica', fontSize=10.5, textColor=colors.HexColor("#222222"),
            leading=16, spaceAfter=5, alignment=TA_LEFT)
st_bul = S('bul', parent=st_body, leftIndent=14, bulletIndent=2, spaceAfter=3)
st_step = S('step', parent=st_body, leftIndent=20, spaceAfter=4)
st_small = S('small', fontName='Helvetica', fontSize=9, textColor=CINZA_CL, leading=12)
st_box = S('box', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#333333"), leading=15)
st_boxt = S('boxt', fontName='Helvetica-Bold', fontSize=10.5, textColor=VERDE_ESC, leading=15)

def bullets(items, style=st_bul):
    return [Paragraph(f"•&nbsp;&nbsp;{t}", style) for t in items]

def steps(items):
    out = []
    for i, t in enumerate(items, 1):
        out.append(Paragraph(f"<b><font color='#00963F'>{i}.</font></b>&nbsp;&nbsp;{t}", st_step))
    return out

def caixa(titulo, texto, bg=BG_BOX, borda=VERDE):
    inner = []
    if titulo:
        inner.append(Paragraph(titulo, st_boxt))
        inner.append(Spacer(1, 2))
    inner.append(Paragraph(texto, st_box))
    t = Table([[inner]], colWidths=[160*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.8, borda),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LINEBEFORE', (0,0), (0,-1), 3, borda),
    ]))
    return t

def dica(texto):
    return caixa("\U0001F4A1 Dica", texto, bg=BG_DICA, borda=LARANJA)

# ── Rodapé/cabeçalho com numeração ──
def on_page(canv, doc):
    canv.saveState()
    # rodapé
    canv.setStrokeColor(colors.HexColor("#e0e0e0"))
    canv.setLineWidth(0.5)
    canv.line(20*mm, 14*mm, 190*mm, 14*mm)
    canv.setFont('Helvetica', 8)
    canv.setFillColor(CINZA_CL)
    canv.drawString(20*mm, 9*mm, "Ministério de Música Hallel — Alegraivos")
    canv.drawRightString(190*mm, 9*mm, f"Página {doc.page}")
    canv.restoreState()

story = []

# ───────────────────────── CAPA ─────────────────────────
story.append(Spacer(1, 40*mm))
try:
    story.append(Image(LOGO, width=42*mm, height=42*mm, hAlign='CENTER'))
except Exception:
    pass
story.append(Spacer(1, 10*mm))
story.append(Paragraph("Manual do Membro", S('cap', fontName='Helvetica-Bold',
             fontSize=30, textColor=VERDE, alignment=TA_CENTER, leading=34)))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Aplicativo do Ministério de Música Hallel",
             S('cap2', fontName='Helvetica', fontSize=14, textColor=CINZA, alignment=TA_CENTER)))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("Comunidade Católica Hallel",
             S('cap3', fontName='Helvetica-Oblique', fontSize=11, textColor=CINZA_CL, alignment=TA_CENTER)))
story.append(Spacer(1, 14*mm))
story.append(HRFlowable(width="40%", thickness=2, color=LARANJA, hAlign='CENTER'))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("“Cantai ao Senhor um canto novo!” — Sl 96,1",
             S('vers', fontName='Helvetica-Oblique', fontSize=11, textColor=VERDE_ESC, alignment=TA_CENTER)))
story.append(PageBreak())

# ───────────────────────── BEM-VINDO ─────────────────────────
story.append(Paragraph("Seja bem-vindo(a)! \U0001F64F", st_h1))
story.append(Paragraph(
    "Este é o aplicativo do nosso Ministério de Música. Por ele você acompanha as suas "
    "<b>escalas</b>, confirma <b>presença</b> em missões e ensaios, estuda as <b>músicas</b>, "
    "vê os <b>set lists</b>, a <b>agenda</b> e conversa com a equipe — tudo na palma da mão. "
    "Este manual mostra, passo a passo, como usar.",
    st_body))
story.append(Spacer(1, 3))
story.append(caixa(None,
    "O app é leve, rápido e funciona como um aplicativo de verdade no seu celular. Tudo o que "
    "você vê fica <b>sincronizado</b> com o ministério. Para tocar vídeos e áudios é preciso "
    "estar conectado à internet."))

# ───────────────────────── 1. INSTALAR ─────────────────────────
story.append(Paragraph("1. Como instalar no celular", st_h1))
story.append(Paragraph(
    "O coordenador vai te enviar um <b>link</b>. Abra esse link no navegador e instale o app "
    "na tela inicial — assim ele vira um ícone, igual a qualquer aplicativo.", st_body))
story.append(Paragraph("\U0001F4F1 iPhone (Safari)", st_h2))
for p in steps([
    "Abra o link no <b>Safari</b> (precisa ser o Safari).",
    "Toque no botão <b>Compartilhar</b> (o quadradinho com a seta para cima).",
    "Escolha <b>Adicionar à Tela de Início</b>.",
    "Toque em <b>Adicionar</b>. Pronto — o ícone Hallel aparece na tela.",
]): story.append(p)
story.append(Paragraph("\U0001F916 Android (Chrome)", st_h2))
for p in steps([
    "Abra o link no <b>Chrome</b>.",
    "Toque nos <b>três pontinhos</b> (canto superior direito).",
    "Escolha <b>Instalar aplicativo</b> (ou <b>Adicionar à tela inicial</b>).",
    "Confirme. O ícone Hallel aparece na tela.",
]): story.append(p)
story.append(dica("Sempre abra o app pelo <b>ícone na tela</b> (não pelo navegador). "
                  "Assim ele abre em tela cheia e fica mais rápido."))

# ───────────────────────── 2. ENTRAR ─────────────────────────
story.append(Paragraph("2. Como entrar (login)", st_h1))
story.append(Paragraph(
    "Na primeira tela, digite o <b>usuário</b> e a <b>senha</b> que o coordenador criou para você "
    "e toque em <b>Entrar</b>.", st_body))
story.append(Paragraph("Primeiro acesso", st_h2))
story.append(Paragraph(
    "No primeiro acesso, o app vai pedir para você <b>criar a sua própria senha</b> — escolha "
    "uma que seja fácil de lembrar. Depois disso, o app te recebe com uma mensagem de boas-vindas.",
    st_body))
story.append(caixa("Esqueceu a senha?",
    "Na tela de entrada, toque em <b>Esqueci minha senha</b>. Você pode informar o <b>e-mail "
    "cadastrado</b> ou o seu <b>primeiro nome</b> para recuperar o acesso. Se precisar, o app "
    "abre uma mensagem para o coordenador no WhatsApp."))
story.append(caixa("Ainda não tem acesso?",
    "Na tela inicial existe a opção <b>Solicitar acesso</b>. Preencha seu nome, instrumento(s), "
    "tamanho da camisa, aniversário e WhatsApp. O coordenador recebe o pedido e aprova.",
    bg=BG_DICA, borda=LARANJA))
story.append(PageBreak())

# ───────────────────────── 3. TELA INICIAL ─────────────────────────
story.append(Paragraph("3. A tela inicial", st_h1))
story.append(Paragraph(
    "Ao entrar, você vê a tela inicial com os <b>atalhos</b> para cada área e alguns avisos "
    "importantes no topo:", st_body))
for p in bullets([
    "<b>Avisos urgentes</b> publicados pelo coordenador aparecem em destaque.",
    "<b>Lembrete de escala:</b> se você tem missão chegando, ela aparece já na abertura.",
    "<b>Mural de Ensaios:</b> os próximos ensaios, com botão para confirmar presença.",
    "<b>Ativar notificações:</b> toque uma vez para receber avisos e ensaios no celular.",
]): story.append(p)
story.append(Paragraph("As áreas que você verá:", st_h2))
areas = [
    ("\U0001F3AF Minha Escala", "Suas missões — onde e quando você vai tocar/cantar."),
    ("\U0001F3B8 Biblioteca", "Todas as músicas, com links, cifra, tom e mixer."),
    ("\U0001F4CB Set Lists", "A ordem das músicas de cada celebração."),
    ("▶️ Playlist", "Ouvir as músicas em sequência para estudar."),
    ("\U0001F4C5 Agenda", "O calendário com todos os eventos do ministério."),
    ("\U0001F4B0 Financeiro / \U0001F4E6 Inventário", "Prestação de contas e os materiais do grupo."),
]
data = [[Paragraph(f"<b>{n}</b>", st_box), Paragraph(d, st_box)] for n, d in areas]
t = Table(data, colWidths=[55*mm, 105*mm])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), colors.HexColor('#f7f7f7')),
    ('BOX',(0,0),(-1,-1),0.6, colors.HexColor('#e0e0e0')),
    ('INNERGRID',(0,0),(-1,-1),0.5, colors.HexColor('#e8e8e8')),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
]))
story.append(t)
story.append(dica("Para voltar à tela inicial a qualquer momento, toque na <b>logo</b> no topo "
                  "ou no botão <b>Voltar</b>."))

# ───────────────────────── 4. MINHA ESCALA ─────────────────────────
story.append(Paragraph("4. Minha Escala (suas missões) \U0001F3AF", st_h1))
story.append(Paragraph(
    "Aqui ficam todas as celebrações em que você foi escalado, da mais próxima para a mais "
    "distante. Em cada uma você vê a <b>data</b>, o <b>horário</b>, o <b>local</b> e a sua "
    "<b>função</b> (violão, vocal, teclado…).", st_body))
story.append(Paragraph("Confirmar presença", st_h2))
story.append(Paragraph(
    "Ao abrir uma missão, você responde se vai poder ir:", st_body))
for p in bullets([
    "Toque em <b>✅ Confirmar</b> se você vai.",
    "Toque em <b>❌ Não poderei</b> se não conseguir ir.",
]): story.append(p)
story.append(Paragraph(
    "O coordenador vê na hora quem confirmou e quem ainda não respondeu. Você pode trocar "
    "a sua resposta a qualquer momento.", st_body))
story.append(dica("Confirme o quanto antes! Isso ajuda demais o coordenador a organizar a equipe."))
story.append(PageBreak())

# ───────────────────────── 5. MURAL DE ENSAIOS ─────────────────────────
story.append(Paragraph("5. Mural de Ensaios \U0001F3BC", st_h1))
story.append(Paragraph(
    "Na tela inicial fica o <b>Mural de Ensaios</b> com os próximos ensaios marcados pelo "
    "coordenador. Em cada ensaio você vê data, horário e local (com botões de "
    "<b>Google Maps</b> e <b>Waze</b> para chegar).", st_body))
for p in bullets([
    "Toque em <b>✅ Vou</b> para confirmar que estará no ensaio.",
    "Toque em <b>❌ Não vou</b> caso não consiga.",
]): story.append(p)
story.append(caixa("Lembrete automático",
    "Se você confirmar presença, o app te <b>lembra na véspera e no dia</b> do ensaio — "
    "para você não esquecer. \U0001F514"))

# ───────────────────────── 6. BIBLIOTECA ─────────────────────────
story.append(Paragraph("6. Biblioteca de Músicas \U0001F3B8", st_h1))
story.append(Paragraph(
    "Toque em qualquer música para abrir e ver tudo sobre ela. Para encontrar rápido, use:", st_body))
for p in bullets([
    "A <b>busca</b> por nome da música ou do artista.",
    "O filtro por <b>tom</b> e por <b>momento</b> (Entrada, Comunhão, Adoração…).",
    "A <b>estrela ★</b> para marcar suas <b>favoritas</b> e filtrar só elas.",
]): story.append(p)
story.append(Paragraph("Dentro de cada música você encontra", st_h2))
for p in bullets([
    "<b>Player</b> do YouTube, Spotify e Deezer para ouvir.",
    "<b>Cifra</b> com botões de <b>tom</b> (+ / −) para subir ou descer e cantar no seu tom.",
    "<b>Tom por vocalista:</b> o tom em que cada cantor canta melhor aquela música.",
    "<b>Mixer</b> (quando disponível): separe os instrumentos e estude a sua parte.",
    "<b>PDF</b> da cifra, quando anexado.",
    "<b>\U0001F4AC Conversa:</b> deixe um recado ou tire dúvidas sobre a música com a equipe.",
]): story.append(p)
story.append(dica("Marque suas músicas favoritas ★ — assim você monta sua lista de estudo "
                  "e encontra tudo num toque."))
story.append(PageBreak())

# ───────────────────────── 7. SET LISTS ─────────────────────────
story.append(Paragraph("7. Set Lists (repertório) \U0001F4CB", st_h1))
story.append(Paragraph(
    "O <b>set list</b> é a ordem das músicas de uma celebração. Toque para abrir e ver a "
    "sequência completa, com o tom de cada uma. Ao tocar numa música da lista, ela abre "
    "direto na Biblioteca para você estudar.", st_body))
story.append(caixa("Repertório no evento",
    "Ao abrir um evento na Agenda, além da escala você vê o <b>repertório na ordem</b> "
    "(com tom e momento de cada música) — basta tocar para abrir a música."))

# ───────────────────────── 8. PLAYLIST ─────────────────────────
story.append(Paragraph("8. Playlist ▶️", st_h1))
story.append(Paragraph(
    "A Playlist toca as músicas em sequência, ótima para estudar no carro ou em casa. "
    "Você escolhe a plataforma (YouTube, Spotify…) e vai passando de uma para a outra.", st_body))

# ───────────────────────── 9. AGENDA ─────────────────────────
story.append(Paragraph("9. Agenda \U0001F4C5", st_h1))
story.append(Paragraph(
    "O calendário mostra todos os eventos do ministério. Toque num dia para ver o evento "
    "(se houver mais de um no mesmo dia, o app mostra as opções).", st_body))
for p in bullets([
    "Veja <b>data, horário e local</b> de cada evento.",
    "Use os botões <b>Google Maps</b> e <b>Waze</b> para chegar no local.",
    "Veja a <b>escala</b>, o <b>repertório</b> e <b>confirme sua presença</b>.",
    "Deixe um recado na <b>\U0001F4AC Conversa</b> do evento.",
]): story.append(p)

# ───────────────────────── 10. NOTIFICACOES E CONVERSA ─────────────────────────
story.append(Paragraph("10. Notificações e Conversa", st_h1))
story.append(Paragraph("\U0001F514 Notificações", st_h2))
story.append(Paragraph(
    "Na tela inicial, toque em <b>Ativar notificações</b> e permita quando o celular perguntar. "
    "Assim você é avisado quando o coordenador <b>publica um aviso</b> ou <b>marca um ensaio</b> "
    "(com o app aberto ou em segundo plano).", st_body))
story.append(Paragraph("\U0001F4AC Conversa", st_h2))
story.append(Paragraph(
    "Cada música e cada evento têm um espaço de <b>conversa</b>. Escreva sua mensagem e toque "
    "em <b>Enviar</b>. Todos da equipe veem. Você pode <b>excluir</b> as suas próprias mensagens.",
    st_body))
story.append(dica("Use a Conversa para combinar detalhes do ensaio, tirar dúvidas de uma música "
                  "ou só incentivar a equipe. \U0001F64C"))

# ───────────────────────── 11. ANIVERSARIOS ─────────────────────────
story.append(Paragraph("11. Aniversários \U0001F389", st_h1))
story.append(Paragraph(
    "O app guarda o seu aniversário (informado no cadastro) e mostra os aniversariantes do mês. "
    "Assim ninguém esquece de celebrar os irmãos do ministério!", st_body))
story.append(PageBreak())

# ───────────────────────── FAQ ─────────────────────────
story.append(Paragraph("Dúvidas frequentes", st_h1))
faq = [
    ("O app está sem novidades / desatualizado?",
     "Abra o app com internet e toque no ☁ no topo para atualizar. No iPhone, se algo não "
     "mudar, remova o ícone e instale de novo pelo Safari."),
    ("Preciso de internet para tudo?",
     "Para ver as informações, o básico funciona offline. Para <b>tocar</b> vídeos e áudios "
     "(YouTube, Spotify, mixer) e para <b>sincronizar</b> dados novos, você precisa de conexão."),
    ("As coisas que envio aparecem nos outros celulares?",
     "Sim. Confirmações, conversas e tudo o mais ficam guardados na nuvem. Em outro aparelho, "
     "toque no ☁ no topo para puxar as novidades."),
    ("Troquei de celular. E meus dados?",
     "É só instalar o app no novo aparelho e entrar com seu usuário e senha."),
    ("Vou faltar em uma escala ou ensaio. O que faço?",
     "Abra a missão (ou o ensaio) e marque <b>Não poderei / Não vou</b>. O coordenador é avisado."),
]
for q, a in faq:
    story.append(Paragraph(f"<b>{q}</b>", st_h2))
    story.append(Paragraph(a, st_body))

story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0e0e0")))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Qualquer dúvida, fale com o coordenador do ministério. Que Deus abençoe o seu serviço "
    "e a sua entrega! \U0001F3B6\U0001F64F",
    S('end', fontName='Helvetica-Oblique', fontSize=10.5, textColor=VERDE_ESC, leading=15)))


# ── build ──
doc = SimpleDocTemplate("Manual-do-Membro-Hallel.pdf", pagesize=A4,
                        leftMargin=20*mm, rightMargin=20*mm,
                        topMargin=18*mm, bottomMargin=20*mm,
                        title="Manual do Membro — Ministério de Música Hallel",
                        author="Ministério de Música Hallel")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("PDF gerado: Manual-do-Membro-Hallel.pdf")
