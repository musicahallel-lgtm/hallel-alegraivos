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
story.append(Paragraph("“Cantai ao Senhor um cântico novo!” — Sl 96",
             S('vers', fontName='Helvetica-Oblique', fontSize=11, textColor=VERDE_ESC, alignment=TA_CENTER)))
story.append(PageBreak())

# ───────────────────────── BEM-VINDO ─────────────────────────
story.append(Paragraph("Seja bem-vindo(a)! \U0001F64F", st_h1))
story.append(Paragraph(
    "Este é o aplicativo do nosso Ministério de Música. Por ele você acompanha as suas "
    "<b>escalas (missões)</b>, estuda as <b>músicas</b>, vê os <b>set lists</b>, a <b>agenda</b> "
    "de eventos e muito mais — tudo na palma da mão. Este manual mostra, passo a passo, como usar.",
    st_body))
story.append(Spacer(1, 3))
story.append(caixa(None,
    "Os seus dados ficam guardados <b>no seu próprio celular</b>. O app é leve, rápido e "
    "funciona até sem internet (para tocar vídeos e áudios você precisa estar conectado)."))

# ───────────────────────── 1. INSTALAR ─────────────────────────
story.append(Paragraph("1. Como instalar no celular", st_h1))
story.append(Paragraph(
    "O Hallel funciona como um aplicativo, mas você instala direto pelo navegador — "
    "rápido e sem ocupar espaço. Acesse o link enviado pelo coordenador e siga abaixo:", st_body))

story.append(Paragraph("\U0001F4F1 iPhone (Safari)", st_h2))
story.extend(steps([
    "Abra o link no <b>Safari</b>.",
    "Toque no botão <b>Compartilhar</b> (o quadradinho com uma seta para cima).",
    "Escolha <b>“Adicionar à Tela de Início”</b>.",
    "Pronto! O ícone do Hallel aparece na tela, igual a qualquer app.",
]))
story.append(Paragraph("\U0001F916 Android (Chrome)", st_h2))
story.extend(steps([
    "Abra o link no <b>Chrome</b>.",
    "Toque no menu <b>(três pontinhos)</b> ou no aviso <b>“Instalar aplicativo”</b>.",
    "Escolha <b>“Instalar”</b>.",
    "O ícone do Hallel aparece na tela do celular.",
]))
story.append(dica("Sempre abra o app pelo <b>ícone na tela</b> (não pelo navegador). "
                  "Assim ele abre em tela cheia e fica mais rápido."))

# ───────────────────────── 2. ENTRAR ─────────────────────────
story.append(Paragraph("2. Como entrar (login)", st_h1))
story.extend(steps([
    "O coordenador vai te entregar um <b>usuário</b> e uma <b>senha</b>.",
    "Na tela inicial, digite o usuário e a senha.",
    "Toque no \U0001F441 (olhinho) se quiser ver a senha que está digitando.",
    "Toque em <b>Entrar</b>.",
]))
story.append(Paragraph("Primeiro acesso", st_h2))
story.append(Paragraph(
    "Na primeira vez, o app vai pedir para você confirmar seu <b>WhatsApp</b> e <b>e-mail</b>. "
    "Isso ajuda o coordenador a falar com você e a recuperar seu acesso caso esqueça a senha.", st_body))
story.append(caixa("Esqueceu a senha?",
    "Na tela de login, toque em <b>“Recuperar acesso”</b> e siga as instruções, "
    "ou peça ao coordenador para redefinir a sua senha."))
story.append(caixa("Ainda não tem acesso?",
    "Toque em <b>“Solicitar entrada”</b> na tela de login, preencha seus dados "
    "(nome, instrumento, WhatsApp, data de nascimento e tamanho da camisa) e aguarde o "
    "coordenador liberar."))

story.append(PageBreak())

# ───────────────────────── 3. TELA INICIAL ─────────────────────────
story.append(Paragraph("3. A tela inicial", st_h1))
story.append(Paragraph(
    "Ao entrar, você vê a <b>tela inicial</b> com os ícones de cada área — parecido com a tela "
    "de apps do celular. É só tocar no ícone para abrir. Para voltar, use o botão "
    "<b>‹ Voltar</b> no topo ou toque na <b>logo</b>.", st_body))
story.append(Spacer(1, 2))
story.append(Paragraph("As áreas que você verá:", st_h2))
area_data = [
    ["\U0001F3AF  Minha Escala", "Suas missões: onde e quando você está escalado."],
    ["\U0001F3B8  Músicas",      "A biblioteca com cifras, letras, áudios e partituras."],
    ["\U0001F4CB  Set Lists",    "A ordem das músicas de cada celebração."],
    ["▶️  Playlist",    "Ouça as músicas em sequência (YouTube/Spotify)."],
    ["\U0001F4C5  Agenda",       "Calendário com todos os eventos e cultos."],
    ["\U0001F4B0  Financeiro",   "Prestação de contas (somente para acompanhar)."],
    ["\U0001F4E6  Inventário",   "Patrimônio do ministério (somente para acompanhar)."],
]
t = Table([[Paragraph(f"<b>{a}</b>", st_box), Paragraph(b, st_box)] for a,b in area_data],
          colWidths=[42*mm, 118*mm])
t.setStyle(TableStyle([
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('LINEBELOW',(0,0),(-1,-2),0.4,colors.HexColor("#e0e0e0")),
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),4),
]))
story.append(t)

# ───────────────────────── 4. MINHA ESCALA ─────────────────────────
story.append(Paragraph("4. Minha Escala (suas missões) \U0001F3AF", st_h1))
story.append(Paragraph(
    "É a área mais importante para você. Aqui aparecem os eventos em que você foi "
    "<b>escalado</b> para tocar ou cantar, com a data, o horário, a sua função e o "
    "<b>local</b>.", st_body))
story.append(Paragraph("Confirmar presença", st_h2))
story.append(Paragraph("Em cada missão você responde se pode ir:", st_body))
story.extend(bullets([
    "<b>✅ Posso</b> — confirma que você estará presente.",
    "<b>❌ Não posso</b> — avisa que não poderá ir naquela data.",
]))
story.append(Paragraph(
    "Se marcar <b>Não posso</b>, você pode <b>indicar um substituto</b>: o app envia um "
    "convite para o outro membro, que aceita ou recusa. Assim o coordenador fica sabendo "
    "na hora.", st_body))
story.append(dica("Confirme sua presença o quanto antes. Isso ajuda demais o coordenador "
                  "a organizar a equipe de cada celebração. \U0001F64F"))

story.append(PageBreak())

# ───────────────────────── 5. MÚSICAS ─────────────────────────
story.append(Paragraph("5. Biblioteca de Músicas \U0001F3B8", st_h1))
story.append(Paragraph(
    "Toque em <b>Músicas</b> para ver todo o repertório. Use a <b>busca</b> no topo para "
    "achar pelo nome ou pelo artista, ou filtre pelo <b>tom</b>.", st_body))
story.append(Paragraph("Ao abrir uma música você encontra:", st_h2))
story.extend(bullets([
    "<b>Player</b> — ouça no YouTube, Spotify ou Deezer (precisa de internet).",
    "<b>Cifra e letra</b> — para acompanhar e estudar.",
    "<b>Transpor o tom</b> — suba ou desça o tom da cifra conforme a sua voz/instrumento.",
    "<b>Partitura em PDF</b> — quando disponível, dá para abrir e baixar.",
    "<b>Mixer</b> — em algumas músicas, separe os instrumentos (voz, violão, bateria…) "
    "para estudar cada parte.",
]))
story.append(dica("No <b>Mixer</b>, toque em <b>M</b> para silenciar um instrumento e "
                  "<b>S</b> para ouvir só ele (solo). Ótimo para treinar a sua parte!"))

# ───────────────────────── 6. SET LISTS ─────────────────────────
story.append(Paragraph("6. Set Lists \U0001F4CB", st_h1))
story.append(Paragraph(
    "O <b>Set List</b> é a sequência de músicas de cada celebração, na ordem em que serão "
    "tocadas — muitas vezes separadas por momentos (entrada, ofertório, comunhão…). "
    "Toque em uma música do set list para abrir a cifra e o player na hora.", st_body))

# ───────────────────────── 7. PLAYLIST ─────────────────────────
story.append(Paragraph("7. Playlist ▶️", st_h1))
story.append(Paragraph(
    "Na <b>Playlist</b> você ouve as músicas em sequência, direto pelo YouTube ou Spotify. "
    "Dá para tocar todo o repertório ou só as músicas de um set list — perfeito para se "
    "preparar no caminho para o ensaio.", st_body))

# ───────────────────────── 8. AGENDA ─────────────────────────
story.append(Paragraph("8. Agenda \U0001F4C5", st_h1))
story.append(Paragraph(
    "A <b>Agenda</b> mostra o calendário do ano com todos os eventos e os cultos semanais. "
    "Os dias com evento ficam destacados — e os dias em que <b>você</b> está escalado também.", st_body))
story.extend(bullets([
    "Toque em um <b>dia</b> para ver o(s) evento(s) daquela data.",
    "Se houver mais de um evento no mesmo dia, o app mostra a lista para você escolher.",
    "Dentro do evento você vê a <b>escala</b>, o <b>horário</b> e o <b>endereço</b>.",
]))
story.append(caixa("\U0001F4CD  Como chegar",
    "Quando o evento tem endereço, aparecem os botões <b>Google Maps</b> e <b>Waze</b>. "
    "Toque e o app de navegação abre a rota direto para o local. \U0001F697"))

story.append(PageBreak())

# ───────────────────────── 9. OUTROS ─────────────────────────
story.append(Paragraph("9. Financeiro e Inventário", st_h1))
story.append(Paragraph(
    "Você pode <b>acompanhar</b> (apenas visualizar) a prestação de contas no "
    "<b>Financeiro</b> — entradas, saídas e saldo — e o <b>Inventário</b> com os "
    "equipamentos e instrumentos do ministério. Só o coordenador faz lançamentos.", st_body))

story.append(Paragraph("10. Aniversários \U0001F389", st_h1))
story.append(Paragraph(
    "No dia do aniversário de um membro, o app mostra um aviso para todos celebrarem juntos. "
    "Não esqueça de parabenizar seu irmão(ã)! \U0001F382", st_body))

# ───────────────────────── DÚVIDAS ─────────────────────────
story.append(Paragraph("Dúvidas frequentes", st_h1))
faq = [
    ("O app está sem novidades / desatualizado?",
     "Abra o app com internet — ele se atualiza sozinho. No iPhone, se algo não mudar, "
     "remova o ícone e instale de novo pelo Safari."),
    ("Preciso de internet para tudo?",
     "Não. Ver escalas, cifras e a agenda funciona offline. Só <b>tocar</b> vídeos e "
     "áudios (YouTube, Spotify, mixer) precisa de conexão."),
    ("Troquei de celular. E meus dados?",
     "É só instalar o app no novo aparelho e entrar com seu usuário e senha."),
    ("Vou faltar em uma escala. O que faço?",
     "Em Minha Escala, marque <b>Não posso</b> e, se possível, <b>indique um substituto</b>."),
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
