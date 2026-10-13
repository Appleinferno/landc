import http.server, functools, mimetypes
mimetypes.add_type("image/webp", ".webp")
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"h:\Websites\landc\charlotte-land-clearing")
H.func.extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".webp": "image/webp", ".svg": "image/svg+xml", ".js": "text/javascript"}
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
