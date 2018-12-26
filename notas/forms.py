from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, SelectDateWidget

from .models import Product, Nota, NotaItens


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['maquina_pt',
                  'maquina_en',
                  'maquina_ch',
                  'tipo_pt',
                  'tipo_en',
                  'tipo_ch',
                  'modelo_pt',
                  'modelo_en',
                  'modelo_ch',
                  'area_trabalho_pt',
                  'area_trabalho_en',
                  'area_trabalho_ch',
                  'eixo_z_pt',
                  'eixo_z_en',
                  'eixo_z_ch',
                  'cor_pt',
                  'cor_en',
                  'cor_ch',
                  'faz_pt',
                  'faz_en',
                  'faz_ch',
                  'voltagem_pt',
                  'voltagem_en',
                  'voltagem_ch',
                  'ncm',
                  'nome_classificacao',
                  'caixa_lateral_base',
                  'opcionais',
                  'imagem',
                  ]
        widgets = {
            'maquina_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Máquina'}),
            'maquina_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Máquina'}),
            'maquina_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Máquina'}),
            'tipo_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
            'tipo_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
            'tipo_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo'}),
            'modelo_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'modelo_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'modelo_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'area_trabalho_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Área de trabalho'}),
            'area_trabalho_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Área de trabalho'}),
            'area_trabalho_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Área de trabalho'}),
            'eixo_z_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Eixo Z'}),
            'eixo_z_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Eixo Z'}),
            'eixo_z_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Eixo Z'}),
            'cor_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'Cor'}),
            'cor_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Cor'}),
            'cor_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'Cor'}),
            'faz_pt': Textarea(attrs={'class': 'form-control', 'placeholder': 'O que ela faz'}),
            'faz_en': Textarea(attrs={'class': 'form-control', 'placeholder': 'O que ela faz'}),
            'faz_ch': Textarea(attrs={'class': 'form-control', 'placeholder': 'O que ela faz'}),
            'voltagem_pt': TextInput(attrs={'class': 'form-control', 'placeholder': 'voltagem'}),
            'voltagem_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'voltagem'}),
            'voltagem_ch': TextInput(attrs={'class': 'form-control', 'placeholder': 'voltagem'}),
            'ncm': TextInput(attrs={'class': 'form-control', 'placeholder': 'NCM'}),
            'nome_classificacao': Textarea(attrs={'class': 'form-control', 'placeholder': 'Classificação'}),
            'caixa_lateral_base': TextInput(attrs={'class': 'form-control', 'placeholder': 'Caixa Lateral Base'}),
            'opcionais': Textarea(attrs={'class': 'form-control', 'placeholder': 'Opcionais'}),
        }


class NotaForm(ModelForm):
    class Meta:
        model = Nota
        fields = ['description', 'date', 'dolar_dia']

        widgets = {
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'date': SelectDateWidget(attrs={'class': 'form-control'}),
            'dolar_dia': NumberInput(attrs={'class': 'form-control'}),
        }


class NotaItensForm(ModelForm):
    class Meta:
        model = NotaItens
        fields = ['item', 'quantidade', 'valor_usd']

        widgets = {
            'item': Select(attrs={'class': 'form-control'}),
            'quantidade': NumberInput(attrs={'class': 'form-control'}),
            'valor_usd': NumberInput(attrs={'class': 'form-control'}),
        }
