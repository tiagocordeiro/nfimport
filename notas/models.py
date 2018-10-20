from django.db import models

from core.models import Active, TimeStampedModel


class Product(TimeStampedModel, Active):
    maquina_pt = models.CharField(max_length=255)
    maquina_en = models.CharField(max_length=255, blank=True, null=True)
    maquina_ch = models.CharField(max_length=255, blank=True, null=True)
    tipo_pt = models.CharField(max_length=255)
    tipo_en = models.CharField(max_length=255, blank=True, null=True)
    tipo_ch = models.CharField(max_length=255, blank=True, null=True)
    modelo_pt = models.CharField(max_length=255)
    modelo_en = models.CharField(max_length=255, blank=True, null=True)
    modelo_ch = models.CharField(max_length=255, blank=True, null=True)
    area_trabalho_pt = models.CharField(max_length=255)
    area_trabalho_en = models.CharField(max_length=255, blank=True, null=True)
    area_trabalho_ch = models.CharField(max_length=255, blank=True, null=True)
    eixo_z_pt = models.CharField(max_length=255)
    eixo_z_en = models.CharField(max_length=255, blank=True, null=True)
    eixo_z_ch = models.CharField(max_length=255, blank=True, null=True)
    cor_pt = models.CharField(max_length=255)
    cor_en = models.CharField(max_length=255, blank=True, null=True)
    cor_ch = models.CharField(max_length=255, blank=True, null=True)
    faz_pt = models.TextField()
    faz_en = models.TextField(blank=True, null=True)
    faz_ch = models.TextField(blank=True, null=True)
    voltagem_pt = models.CharField(max_length=10)
    voltagem_en = models.CharField(max_length=10, blank=True, null=True)
    voltagem_ch = models.CharField(max_length=10, blank=True, null=True)
    ncm = models.CharField(max_length=20)
    nome_classificacao = models.TextField(blank=True, null=True)
    caixa_lateral_base = models.CharField(max_length=255, blank=True, null=True)
    opcionais = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        ordering = ('maquina_pt',)
        verbose_name = 'máquina'
        verbose_name_plural = 'máquinas'

    def __str__(self):
        return self.maquina_pt


class Nota(TimeStampedModel, Active):
    description = models.CharField(max_length=255)
    date = models.DateField()
    dolar_dia = models.DecimalField(
        decimal_places=2,
        max_digits=13,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('date', 'description')
        verbose_name = 'nota'
        verbose_name_plural = 'notas'

    def __str__(self):
        return self.description


class NotaItens(models.Model):
    item = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    nota = models.ForeignKey(Nota, null=True, on_delete=models.SET_NULL)
    quantidade = models.PositiveIntegerField()
    valor_usd = models.DecimalField(
        decimal_places=2,
        max_digits=13,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
