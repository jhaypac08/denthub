from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme that doesn't enforce CSRF validation.
    Used for session-based auth with proper CORS setup.
    """
    def enforce_csrf(self, request):
        # Don't enforce CSRF - we handle it manually with the CSRF token in headers
        return
