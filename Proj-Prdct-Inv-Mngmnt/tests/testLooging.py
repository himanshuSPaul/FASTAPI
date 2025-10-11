import sys
import os
import importlib.util
import pkgutil
from pathlib import Path


print("os.path.dirname(__file__) :", os.path.dirname(__file__))
print("os.path.join(os.path.dirname(__file__), '..')", os.path.join(os.path.dirname(__file__), ".."))
# print("os.path.join(os.path.dirname(__file__), '..', 'app' :", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path)

# print("cwd:", os.getcwd())
# print("script path:", Path(__file__).resolve())
# print("sys.path[0]:", sys.path[0])
# print("sys.path (first 6):", sys.path[:6])

spec = importlib.util.find_spec("app")
print("importlib.util.find_spec('app') ->", spec)

# spec_loog = importlib.util.find_spec("app.utils.looging")
# print("importlib.util.find_spec('app.utils.looging') ->", spec_loog)

# # List top-level package names found in first sys.path entry (quick view)
# try:
#     first = sys.path[0] or "."
#     found = [m.name for m in pkgutil.iter_modules([first])]
#     print("top-level modules in sys.path[0]:", found[:40])
# except Exception as e:
#     print("could not list modules in sys.path[0]:", e)

# # Try importing and show error if it fails
# try:
#     import app
#     print("import app OK ->", getattr(app, "__file__", "<package>"))
# except Exception as exc:
#     print("import app FAILED:", type(exc).__name__, exc)