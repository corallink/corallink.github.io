#!/usr/bin/env python3
"""코랄웍스 로컬 미리보기 서버 — public/ 정적 서빙 + 깔끔한 URL(.html 자동 매핑).

사용법: python3 _preview_server.py  →  http://localhost:8081/
(quartz serve 대용. 빌드 결과물을 그대로 보여주기만 하고, 파일 감시·재빌드는 안 함)
"""
import http.server
import os
import urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
PORT = 8081


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        path = urllib.parse.unquote(self.path.split("?")[0].split("#")[0])
        fs_path = os.path.join(ROOT, path.lstrip("/"))
        # 깔끔한 URL → .html 매핑 (퀄츠 클린 URL 대응)
        if not os.path.exists(fs_path) and os.path.exists(fs_path.rstrip("/") + ".html"):
            self.path = urllib.parse.quote(path.rstrip("/") + ".html")
        return super().send_head()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("localhost", PORT), CleanURLHandler) as httpd:
        print(f"코랄웍스 미리보기: http://localhost:{PORT}/")
        httpd.serve_forever()
