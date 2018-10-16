from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True


class Active(models.Model):
    active = models.BooleanField('ativo', default=True)

    class Meta:
        abstract = True


class Product(TimeStampedModel, Active):
    maquina_pt = models.CharField(max_length=255)
    maquina_en = models.CharField(max_length=255)
    maquina_ch = models.CharField(max_length=255)
    tipo_pt = models.CharField(max_length=255)
    tipo_en = models.CharField(max_length=255)
    tipo_ch = models.CharField(max_length=255)
    modelo_pt = models.CharField(max_length=255)
    modelo_en = models.CharField(max_length=255)
    modelo_ch = models.CharField(max_length=255)
    area_trabalho_pt = models.CharField(max_length=255)
    area_trabalho_en = models.CharField(max_length=255)
    area_trabalho_ch = models.CharField(max_length=255)
    eixo_z_pt = models.CharField(max_length=255)
    eixo_z_en = models.CharField(max_length=255)
    eixo_z_ch = models.CharField(max_length=255)
    cor_pt = models.CharField(max_length=255)
    cor_en = models.CharField(max_length=255)
    cor_ch = models.CharField(max_length=255)
    faz_pt = models.TextField()
    faz_en = models.TextField()
    faz_ch = models.TextField()
    voltagem_pt = models.CharField(max_length=10)
    voltagem_en = models.CharField(max_length=10)
    voltagem_ch = models.CharField(max_length=10)
    ncm = models.CharField(max_length=20)
    nome_classificacao = models.TextField()
    caixa_lateral_base = models.CharField(max_length=255)
    opcionais = models.TextField()
    imagem = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name = 'máquina'
        verbose_name_plural = 'máquinas'
