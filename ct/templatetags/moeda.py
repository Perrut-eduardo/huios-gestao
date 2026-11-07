from django import template

register = template.Library()


@register.filter
def reais(centavos):
    """Formata inteiros armazenados em centavos, sem cálculo com float."""
    if centavos is None:
        return "Não informado"
    negativo = centavos < 0
    valor = abs(int(centavos))
    inteiro, cent = divmod(valor, 100)
    parte_inteira = f"{inteiro:,}".replace(",", ".")
    return f"{'-' if negativo else ''}R$ {parte_inteira},{cent:02d}"
