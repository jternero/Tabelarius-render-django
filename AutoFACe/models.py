# models.py
from django.db import models

# models.py
class UserUpload(models.Model):
    email = models.EmailField()
    xml_firmado = models.FileField(upload_to='xml_firmados/', null=True, blank=True)  # <-- permite valores nulos temporalmente
    pdf = models.FileField(upload_to='pdf_remisiones/', null=True, blank=True)

    def __str__(self):
        return self.email
