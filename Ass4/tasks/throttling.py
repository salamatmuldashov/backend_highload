from rest_framework.throttling import UserRateThrottle

class RoleBasedThrottle(UserRateThrottle):
    def get_rate(self):
        # Use `self.request` to determine user roles
        if hasattr(self, 'request') and self.request.user.is_staff:
            return '1000/day'  # Higher limit for staff
        return '10000/day'  # Default limit for regular users

    def allow_request(self, request, view):
        # Attach the request object to self for use in get_rate
        self.request = request
        return super().allow_request(request, view)
