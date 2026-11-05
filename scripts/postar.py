"""postar.py — envia a conferência aprovada para a task: prints anexados, comentário atribuído, status e responsável.

uso: ~/.exos-whisper/bin/python -I postar.py <envio.json> [--apply] [--forcar]

Sem --apply só mostra a prévia exata (nada é escrito). Só rode --apply depois do "pode enviar" do Cleber.
envio.json (caminhos relativos à pasta do próprio envio.json):
  {"task_id": "...", "responsavel": {"id": 54941517, "nome": "Patrick Guilherme"},
   "tirar_responsaveis": [54927970], "status": "em alteração & ajuste",
   "comentario": "comentario.md", "prints": ["prints/Conferência - ... .png"]}
comentario.md:
  1ª linha "@<nome do responsável> ..." vira menção; "## Título" vira linha em negrito; "- item" vira "• item";
  [[nome do print sem .png]] vira link para o anexo; **trecho** vira negrito.
Idempotente: anexo com o mesmo nome não sobe de novo; comentário com o mesmo começo não é postado de novo (--forcar posta).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clickup_api as cu  # noqa: E402

LINK = re.compile(r"\[\[(.+?)\]\]")
NEGRITO = re.compile(r"\*\*(.+?)\*\*")


def _inline(txt: str, urls: dict, faltam: set) -> list:
    """Texto de uma linha -> blocos (texto, negrito, link)."""
    blocos, pos = [], 0
    for m in re.finditer(r"\[\[(.+?)\]\]|\*\*(.+?)\*\*", txt):
        if m.start() > pos:
            blocos.append({"text": txt[pos:m.start()]})
        if m.group(1) is not None:
            nome = m.group(1).strip()
            url = urls.get(nome)
            if url is None:
                faltam.add(nome)
                url = "(link do anexo)"
            blocos.append({"text": nome, "attributes": {"link": url}})
        else:
            blocos.append({"text": m.group(2), "attributes": {"bold": True}})
        pos = m.end()
    if pos < len(txt):
        blocos.append({"text": txt[pos:]})
    return blocos


def montar(md: str, resp: dict, urls: dict) -> tuple[list, set]:
    blocos, faltam = [], set()
    linhas = md.rstrip("\n").split("\n")
    for i, ln in enumerate(linhas):
        if i == 0:
            arroba = "@" + resp["nome"]
            if not ln.startswith(arroba):
                raise SystemExit(f"ERRO: a 1ª linha do comentário tem de começar com '{arroba}'")
            blocos.append({"type": "tag", "user": {"id": int(resp["id"])}})
            blocos += _inline(ln[len(arroba):], urls, faltam)
        elif ln.startswith("## "):
            blocos.append({"text": ln[3:].strip(), "attributes": {"bold": True}})
        elif ln.startswith("- "):
            blocos += _inline("• " + ln[2:], urls, faltam)
        else:
            blocos += _inline(ln, urls, faltam)
        blocos.append({"text": "\n"})
    return blocos, faltam


def em_texto(blocos: list, resp: dict) -> str:
    out = []
    for b in blocos:
        if b.get("type") == "tag":
            out.append("@" + resp["nome"])
        elif (b.get("attributes") or {}).get("link"):
            out.append(f"{b['text']} [link: {b['attributes']['link'][:60]}]")
        elif (b.get("attributes") or {}).get("bold"):
            out.append(f"**{b['text']}**")
        else:
            out.append(b["text"])
    return "".join(out)


def chave(md: str) -> list:
    """Trechos que identificam o comentário já postado (o 1º título e o 1º item)."""
    tit = next((ln[3:].strip() for ln in md.split("\n") if ln.startswith("## ")), "")
    item = next((LINK.sub(lambda m: m.group(1), ln[2:]).strip()[:80] for ln in md.split("\n") if ln.startswith("- ")), "")
    return [t for t in (tit, item) if t]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    aplicar, forcar = "--apply" in sys.argv, "--forcar" in sys.argv
    cfg_path = os.path.abspath(args[0])
    base = os.path.dirname(cfg_path)
    cfg = json.load(open(cfg_path))
    tid, resp = cu.id_da_task(cfg["task_id"]), cfg["responsavel"]
    md = open(os.path.join(base, cfg["comentario"]), encoding="utf-8").read()
    prints = [os.path.join(base, p) for p in cfg.get("prints", [])]
    for p in prints:
        if not os.path.exists(p):
            sys.exit(f"ERRO: print não encontrado: {p}")

    t = cu.tarefa(tid)
    estados = [s["status"] for s in cu.lista(t["list"]["id"]).get("statuses", [])]
    if cfg["status"] not in estados:
        sys.exit(f"ERRO: status '{cfg['status']}' não existe na lista {t['list']['name']}: {estados}")
    anexos = {a["title"]: a for a in t.get("attachments", [])}
    nomes = {os.path.splitext(os.path.basename(p))[0]: p for p in prints}
    urls = {n: anexos[os.path.basename(p)]["url"] for n, p in nomes.items() if os.path.basename(p) in anexos}
    blocos, faltam = montar(md, resp, urls)
    citados = set(LINK.findall(md))
    sem_arquivo = {c for c in citados if c.strip() not in nomes}
    if sem_arquivo:
        sys.exit(f"ERRO: o comentário cita print que não está em 'prints': {sorted(sem_arquivo)}")
    nao_citados = [n for n in nomes if n not in citados]
    k = chave(md)
    ja = [c for c in cu.comentarios(tid) if k and all(x in (c.get("comment_text") or "") for x in k)]

    atuais = [a["username"] for a in t["assignees"]]
    print(f"TASK  {t['name']}  ({tid})")
    print("ANEXOS")
    for n, p in nomes.items():
        print(f"   {'já anexado' if os.path.basename(p) in anexos else 'vai subir '}  {os.path.basename(p)}")
    if nao_citados:
        print(f"   aviso: print anexado sem citação no comentário: {nao_citados}")
    print(f"COMENTÁRIO  (atribuído a {resp['nome']})" + ("  — JÁ POSTADO, não repete (use --forcar)" if ja and not forcar else ""))
    print("-" * 100)
    print(em_texto(blocos, resp).rstrip())
    print("-" * 100)
    print(f"STATUS       {t['status']['status']} -> {cfg['status']}")
    print(f"RESPONSÁVEL  {', '.join(atuais) or '-'} -> {resp['nome']}")
    if not aplicar:
        print("\nPRÉVIA: nada foi escrito. Depois do 'pode enviar', rode de novo com --apply.")
        return

    log = {"quando": dt.datetime.now().isoformat(timespec="seconds"), "task": tid, "anexos": {}, "comentario": None}
    for n, p in nomes.items():
        nome = os.path.basename(p)
        if nome in anexos:
            urls[n] = anexos[nome]["url"]
            continue
        r = cu.anexar(tid, p, nome)
        urls[n] = r["url"]
        log["anexos"][nome] = r.get("id")
        print(f"anexado: {nome}")
    blocos, faltam = montar(md, resp, urls)
    if faltam:
        sys.exit(f"ERRO: sem URL para {sorted(faltam)}; nada foi comentado")
    if ja and not forcar:
        print(f"comentário já existe ({ja[0]['id']}): não repeti")
        cid = ja[0]["id"]
    else:
        c, b = cu.api("POST", f"/api/v2/task/{tid}/comment",
                      {"comment": blocos, "assignee": int(resp["id"]), "notify_all": False}, tries=6)
        cid = cu.ok(c, b, "POST comentário").get("id")
        print(f"comentário postado: {cid}")
    log["comentario"] = cid
    cu.ok(*cu.api("PUT", f"/api/v2/task/{tid}", {"status": cfg["status"]}), "PUT status")
    tirar = [int(x) for x in cfg.get("tirar_responsaveis", []) if int(x) != int(resp["id"])]
    c, b = cu.api("PUT", f"/api/v2/task/{tid}", {"assignees": {"add": [int(resp["id"])], "rem": tirar}})
    if c != 200:                                  # Space com um responsável só: tira antes, põe depois
        cu.ok(*cu.api("PUT", f"/api/v2/task/{tid}", {"assignees": {"add": [], "rem": tirar}}), "PUT responsável (tirar)")
        cu.ok(*cu.api("PUT", f"/api/v2/task/{tid}", {"assignees": {"add": [int(resp["id"])], "rem": []}}), "PUT responsável (pôr)")
    json.dump(log, open(os.path.join(base, "envio_log.json"), "w"), ensure_ascii=False, indent=1)

    # relê e confere
    t2 = cu.tarefa(tid)
    com = next((c for c in cu.comentarios(tid) if str(c["id"]) == str(cid)), None)
    titulos = {a["title"] for a in t2.get("attachments", [])}
    checks = {
        "prints anexados": all(os.path.basename(p) in titulos for p in prints),
        "comentário existe": com is not None,
        "comentário atribuído": bool(com and (com.get("assignee") or {}).get("id") == int(resp["id"])),
        "comentário em aberto": bool(com and com.get("resolved") is False),
        "links dos prints no comentário": bool(com) and all(
            any((b.get("attributes") or {}).get("link") == urls[n] for b in com.get("comment", [])) for n in citados),
        "status": t2["status"]["status"] == cfg["status"],
        "responsável": [a["id"] for a in t2["assignees"]] == [int(resp["id"])],
    }
    print("\nCONFERÊNCIA DO ENVIO")
    for k2, v in checks.items():
        print(f"   {'ok ' if v else 'FALHOU'}  {k2}")
    sys.exit(0 if all(checks.values()) else 1)


if __name__ == "__main__":
    main()
