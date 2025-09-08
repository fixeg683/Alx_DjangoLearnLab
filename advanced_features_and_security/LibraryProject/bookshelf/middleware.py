# bookshelf/middleware.py
from django.utils.deprecation import MiddlewareMixin

class CSPMiddleware(MiddlewareMixin):
    """
    Lightweight Content-Security-Policy without extra deps.
    Adjust directives carefully for your environment.
    """
    def process_response(self, request, response):
        # Basic sane defaults; adjust to include your domains/CDNs as needed.
        csp = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
            "font-src 'self' data:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "upgrade-insecure-requests"
        )
        response.headers.setdefault("Content-Security-Policy", csp)
        return response
