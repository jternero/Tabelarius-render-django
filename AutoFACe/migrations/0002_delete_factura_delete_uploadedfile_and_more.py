# Generated by Django 5.1.7 on 2025-03-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AutoFACe", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Factura",
        ),
        migrations.DeleteModel(
            name="UploadedFile",
        ),
        migrations.RemoveField(
            model_name="userupload",
            name="file",
        ),
        migrations.RemoveField(
            model_name="userupload",
            name="uploaded_at",
        ),
        migrations.AddField(
            model_name="userupload",
            name="pdf",
            field=models.FileField(blank=True, null=True, upload_to="pdf_remisiones/"),
        ),
        migrations.AddField(
            model_name="userupload",
            name="xml_firmado",
            field=models.FileField(blank=True, null=True, upload_to="xml_firmados/"),
        ),
    ]
