# graceful.py
import signal
import threading

_stop = threading.Event()
_on_shutdown = None

def _handler(sig, frame):
    print("\nCtrl+C detected — shutting down...")
    _stop.set()
    if _on_shutdown:
        try:
            _on_shutdown()
        except Exception as e:
            print("shutdown error:", e)

def install(on_shutdown=None):
    """Gọi 1 lần ở main để đăng ký Ctrl+C handler."""
    global _on_shutdown
    _on_shutdown = on_shutdown
    signal.signal(signal.SIGINT, _handler)
    # Trên Windows SIGTERM có thể không có – bỏ qua nếu lỗi
    try:
        signal.signal(signal.SIGTERM, _handler)
    except Exception:
        pass

def running() -> bool:
    """Dùng trong vòng lặp."""
    return not _stop.is_set()
