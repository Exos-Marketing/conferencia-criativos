"""clickup_api.py — REST do ClickUp com o token do Keychain (serviço clickup-exos-api). Nunca imprime o token.

GET repete em 429/5xx/rede. Escrita só repete em 429, que o ClickUp recusa sem executar: em 5xx ou queda de rede
quem chamou relê a task e confere antes de tentar de novo (repetir duplicaria comentário ou anexo).
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

BASE = "https://api.clickup.com"
WS = "9013012202"
_TOKEN = None


def token() -> str:
    global _TOKEN
    if not _TOKEN:
        t = os.environ.get("CLICKUP_TOKEN", "").strip() or subprocess.run(
            ["security", "find-generic-password", "-s", "clickup-exos-api", "-w"],
            capture_output=True, text=True).stdout.strip()
        if not t:
            sys.exit("ERRO: token do ClickUp ausente (CLICKUP_TOKEN ou Keychain clickup-exos-api)")
        _TOKEN = t
    return _TOKEN


def _pedir(method: str, path: str, data: bytes | None, ctype: str, tries: int) -> tuple[int, object]:
    for a in range(tries):
        req = urllib.request.Request(BASE + path, data=data, method=method)
        req.add_header("Authorization", token())
        req.add_header("Content-Type", ctype)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                t = r.read().decode()
                return r.status, (json.loads(t) if t.strip() else {})
        except urllib.error.HTTPError as e:
            if e.code == 429 and a < tries - 1:
                reset = e.headers.get("X-RateLimit-Reset") or ""
                time.sleep(max(2, min(65, int(reset) - int(time.time()) + 1)) if reset.isdigit() else 5 * (a + 1))
                continue
            if e.code in (500, 502, 503, 504) and method == "GET" and a < tries - 1:
                time.sleep(3 * (a + 1))
                continue
            txt = e.read().decode()
            try:
                return e.code, json.loads(txt)
            except ValueError:
                return e.code, txt
        except OSError:
            if method == "GET" and a < tries - 1:
                time.sleep(3)
                continue
            return 0, "sem resposta (rede)"
    return 0, "esgotou as tentativas"


def api(method: str, path: str, body: dict | None = None, tries: int = 6) -> tuple[int, object]:
    data = json.dumps(body).encode() if body is not None else None
    return _pedir(method, path, data, "application/json", tries)


def ok(c: int, b: object, o_que: str) -> dict:
    if c != 200 or not isinstance(b, dict):
        raise RuntimeError(f"ClickUp {o_que} -> {c}: {str(b)[:300]}")
    return b


def id_da_task(s: str) -> str:
    """Aceita o ID ou a URL (…/t/<ws>/<id> ou …/t/<id>)."""
    m = re.search(r"/t/(?:\d+/)?([0-9a-z]+)/?$", s.strip())
    return m.group(1) if m else s.strip()


def tarefa(tid: str) -> dict:
    return ok(*api("GET", f"/api/v2/task/{tid}?include_markdown_description=true"), "GET task")


def comentarios(tid: str) -> list:
    return ok(*api("GET", f"/api/v2/task/{tid}/comment"), "GET comentários").get("comments", [])


def lista(lid: str) -> dict:
    return ok(*api("GET", f"/api/v2/list/{lid}"), "GET lista")


def pagina(doc: str, page: str, ws: str = WS) -> dict:
    return ok(*api("GET", f"/api/v3/workspaces/{ws}/docs/{doc}/pages/{page}?content_format=text/md"), "GET página")


def paginas(doc: str, ws: str = WS) -> list:
    c, b = api("GET", f"/api/v3/workspaces/{ws}/docs/{doc}/pageListing")
    return b if c == 200 and isinstance(b, list) else []


def anexar(tid: str, caminho: str, nome: str | None = None) -> dict:
    """POST multipart de um arquivo na task. Só repete em 429."""
    nome = nome or os.path.basename(caminho)
    fronteira = uuid.uuid4().hex
    tipo = mimetypes.guess_type(nome)[0] or "application/octet-stream"
    with open(caminho, "rb") as f:
        dados = f.read()
    cab = (f'--{fronteira}\r\nContent-Disposition: form-data; name="attachment"; filename="{nome}"\r\n'
           f"Content-Type: {tipo}\r\n\r\n").encode("utf-8")
    corpo = cab + dados + f"\r\n--{fronteira}--\r\n".encode()
    return ok(*_pedir("POST", f"/api/v2/task/{tid}/attachment", corpo,
                      f"multipart/form-data; boundary={fronteira}", 6), f"POST anexo {nome}")
