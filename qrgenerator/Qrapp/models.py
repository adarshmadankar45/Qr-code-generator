from django.db import models
from django.utils.timezone import now
from django.contrib.gis.geoip2 import GeoIP2

class QRCode(models.Model):
    data = models.TextField()
    qr_code_image = models.TextField()  # Base64 encoded image
    scan_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def is_expired(self):
        return self.expires_at and now() > self.expires_at

class ScanRecord(models.Model):
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=50, blank=True)

    @staticmethod
    def get_location(ip):
        try:
            geo = GeoIP2()
            return geo.city(ip)
        except:
            return "Unknown"

