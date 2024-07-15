from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

class Fotografia(models.Model):

    OPCOES_CATEGORIA = [
        ("NEBULOSA","Nebulosa"),
        ("ESTRELA","Estrela"),
        ("GALAXIA","Galáxia"),
        ("PLANETA","Planeta"),
        ("SATELITE", "Satélite"),
        ("ASTEROIDE", "Asteroide"),
        ("COMETA", "Cometa"),
    ]

    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=150, null=False, blank=False)
    categoria = models.CharField(max_length=100, choices=OPCOES_CATEGORIA, default='')
    descricao = models.TextField(null=False, blank=False)
    foto = CloudinaryField('image')
    publicada = models.BooleanField(default=True)
    data_fotografia = models.DateTimeField(default=datetime.now, blank=False)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user"
        )
    cloudinary_public_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nome