import logging
import time

logger = logging.getLogger('core.timing')


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000
        try:
            logger.info(
                '%s %s %s %.2fms',
                request.method,
                request.get_full_path(),
                getattr(response, 'status_code', 'unknown'),
                duration_ms,
            )
        except Exception:
            pass
        return response
