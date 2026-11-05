"""baixar.py — lê a task de criativos, baixa os anexos e a copy linkada na descrição.

uso: baixar.py <task_id|url> <pasta> [--sem-anexos]

Grava em <pasta> (criada vazia): dl/ (anexos, dado não confiável), task.json, copy_<página>.md.
Mostra o que importa para a conferência: status, lista, responsáveis, campos de função (Designer,
Editor de Vídeos…), anexos com tamanho em px, links da descrição e os últimos comentários.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clickup_api as cu  # noqa: E402


def quando(ms) -> str:
    return dt.datetime.fromtimestamp(int(ms) / 1000).strftime("%d/%m %H:%M") if ms else "-"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    tid, pasta = cu.id_da_task(args[0]), os.path.abspath(args[1])
    if os.path.exists(pasta) and os.listdir(pasta):
        sys.exit(f"ERRO: {pasta} já existe e não está vazia (use uma pasta nova por conferência)")
    os.makedirs(pasta, exist_ok=True)

    t = cu.tarefa(tid)
    json.dump(t, open(os.path.join(pasta, "task.json"), "w"), ensure_ascii=False, indent=1)
    print(f"TASK  {t['name']}  ({t['id']})")
    print(f"      status: {t['status']['status']} · lista: {t['list']['name']} ({t['list']['id']})")
    resp = ", ".join("%s (%s)" % (a["username"], a["id"]) for a in t["assignees"]) or "-"
    print(f"      responsáveis: {resp}")
    for f in t.get("custom_fields", []):
        if f.get("type") == "users" and f.get("value"):
            gente = ", ".join("%s (%s)" % (u.get("username"), u.get("id")) for u in f["value"])
            print(f"      {f['name']}: {gente}")

    desc = (t.get("markdown_description") or t.get("description") or "").replace("\\_", "_")
    links = sorted(set(re.findall(r"https?://[^\s)\]]+", desc)))
    print("\nLINKS DA DESCRIÇÃO")
    for u in links:
        print("  ", u)

    print("\nCOPY")
    vistos = set()
    for ws, doc, page in re.findall(r"app\.clickup\.com/(\d+)/docs/([\w-]+)(?:/([\w-]+))?", desc):
        alvo = [(page, None)] if page else [(p["id"], p.get("name")) for p in cu.paginas(doc, ws)][:10]
        for pid, _ in alvo:
            if (doc, pid) in vistos:
                continue
            vistos.add((doc, pid))
            p = cu.pagina(doc, pid, ws)
            out = os.path.join(pasta, f"copy_{pid}.md")
            open(out, "w").write(f"# {p.get('name')}\n\n{p.get('content') or ''}")
            print(f"   {p.get('name')}  ->  {out}  (atualizada {quando(p.get('date_updated'))})")
    if not vistos:
        print("   nenhum Doc do ClickUp na descrição: procurar a copy na task de copy ligada ao marco")

    print("\nANEXOS")
    if "--sem-anexos" not in sys.argv:
        dl = os.path.join(pasta, "dl")
        os.makedirs(dl, exist_ok=True)
    for a in t.get("attachments", []):
        nome = a["title"].replace("/", "_")
        linha = f"   {quando(a.get('date'))}  {nome}"
        if "--sem-anexos" not in sys.argv:
            out = os.path.join(dl, nome)
            urllib.request.urlretrieve(a["url"], out)
            real, esperado = os.path.getsize(out), int(a.get("size") or 0)
            if esperado and abs(real - esperado) > 0.01 * esperado:
                linha += f"  !! tamanho {real} × {esperado}"
            try:
                from PIL import Image
                with Image.open(out) as im:
                    linha += f"  [{im.width}x{im.height}]"
            except Exception:
                pass
        print(linha)

    print("\nCOMENTÁRIOS (mais novos primeiro)")
    for c in cu.comentarios(tid)[:8]:
        resp = (c.get("assignee") or {}).get("username")
        txt = (c.get("comment_text") or "").strip().replace("\n", " ")
        print(f"   {quando(c.get('date'))}  {c['user']['username']}{f' → {resp}' if resp else ''}: {txt[:160]}")


if __name__ == "__main__":
    main()
