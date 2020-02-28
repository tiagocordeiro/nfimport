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
    voltagem_pt = models.CharField(max_length=255)
    voltagem_en = models.CharField(max_length=255, blank=True, null=True)
    voltagem_ch = models.CharField(max_length=255, blank=True, null=True)
    ncm = models.CharField(max_length=255)
    nome_classificacao = models.TextField(blank=True, null=True)
    caixa_lateral_base = models.CharField(max_length=255, blank=True, null=True)
    opcionais = models.TextField(blank=True, null=True)
    imagem = models.URLField(blank=True, null=True, default='https://via.placeholder.com/150')
    codigo_sku = models.CharField('Código do produto no Bling',
                                  max_length=60,
                                  unique=True,
                                  blank=True,
                                  null=True)
    preco_custo = models.DecimalField('Preço de custo em ¥',
                                      max_digits=16,
                                      decimal_places=10,
                                      default=0.0,
                                      blank=True,
                                      null=True)
    preco_federal = models.DecimalField('Preço federal',
                                        max_digits=16,
                                        decimal_places=10,
                                        default=0.0,
                                        blank=True,
                                        null=True)
    peso_liquido = models.DecimalField('Peso Líquido em Kg',
                                       max_digits=10,
                                       decimal_places=3,
                                       default=0,
                                       blank=True,
                                       null=True)
    peso_bruto = models.DecimalField('Peso Bruto em Kg',
                                     max_digits=10,
                                     decimal_places=3,
                                     default=0,
                                     blank=True,
                                     null=True)
    largura = models.DecimalField('Largura em cm',
                                  max_digits=10,
                                  decimal_places=2,
                                  default=0,
                                  blank=True,
                                  null=True)
    altura = models.DecimalField('Altura em cm',
                                 max_digits=10,
                                 decimal_places=2,
                                 default=0,
                                 blank=True,
                                 null=True)
    profundidade = models.DecimalField('Profundidade em cm',
                                       max_digits=10,
                                       decimal_places=2,
                                       default=0,
                                       blank=True,
                                       null=True)

    class Meta:
        ordering = ('maquina_pt', 'tipo_pt', 'modelo_pt')
        verbose_name = 'máquina'
        verbose_name_plural = 'máquinas'

    def cubagem(self):
        return float(self.largura) / 100 * float(self.altura) / 100 * float(self.profundidade) / 100

    def build_product_name_str(self):
        fields_to_return = [self.codigo_sku, self.maquina_pt,
                            self.tipo_pt, self.modelo_pt]

        str_to_return = ''
        fields_total_len = len(fields_to_return)
        field_item_position = 1

        for field in fields_to_return:
            if field:
                if field_item_position == fields_total_len:
                    str_to_return += field
                else:
                    str_to_return += field + ' - '
            field_item_position += 1

        return str_to_return

    def __str__(self):
        return self.build_product_name_str()


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
