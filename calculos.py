class ValidacaoErro(Exception):
    """Exceção customizada para erros de validação de entrada."""
    pass


def calcular_inss(salario: float) -> float:
    """
    Calcula o desconto do INSS de forma progressiva, conforme faixas e alíquotas de 2025.

    Faixas baseadas nos valores mensais:
    - Até 1512,00: 7.5%
    - De 1512,01 até 2547,00: 9%
    - De 2547,01 até 3856,00: 12%
    - De 3856,01 até 7507,49: 14%
    - Acima de 7507,49: teto fixo de 877,24

    Args:
        salario (float): Salário bruto mensal.

    Returns:
        float: Valor do desconto do INSS.
    """
    teto = 877.24

    if salario > 7507.49:
        return teto

    faixas = [
        (1512.00, 0.075),
        (2547.00, 0.09),
        (3856.00, 0.12),
        (7507.49, 0.14),
    ]

    desconto = 0
    faixa_anterior = 0

    for limite, aliquota in faixas:
        if salario > limite:
            desconto += (limite - faixa_anterior) * aliquota
            faixa_anterior = limite
        else:
            desconto += (salario - faixa_anterior) * aliquota
            break

    return round(desconto, 2)


def calcular_irrf(base: float) -> float:
    """
    Calcula o desconto do IRRF com base na base de cálculo (salário menos INSS).

    Args:
        base (float): Base de cálculo para IRRF.

    Returns:
        float: Valor do desconto do IRRF.
    """
    if base <= 2112.00:
        return 0
    elif base <= 2826.65:
        return max(0, base * 0.075 - 158.40)
    elif base <= 3751.05:
        return max(0, base * 0.15 - 370.40)
    elif base <= 4664.68:
        return max(0, base * 0.225 - 651.73)
    else:
        return max(0, base * 0.275 - 884.96)


def calcular_valor_hora(
    salario_mensal: float,
    dias_no_mes: int = 30,
    horas_por_dia: int = 8
) -> float:
    """
    Calcula o valor da hora considerando o salário mensal e jornada padrão.

    Args:
        salario_mensal (float): Salário bruto mensal.
        dias_no_mes (int): Número de dias no mês (default 30).
        horas_por_dia (int): Número de horas por dia (default 8).

    Returns:
        float: Valor da hora trabalhada.
    """
    if salario_mensal <= 0 or dias_no_mes <= 0 or horas_por_dia <= 0:
        return 0.0

    diaria = salario_mensal / dias_no_mes
    return diaria / horas_por_dia


def calcular_extras(
    valor_hora: float,
    horas_extras: int,
    minutos_extras: int
) -> float:
    """
    Calcula o valor das horas e minutos extras.

    Args:
        valor_hora (float): Valor da hora normal.
        horas_extras (int): Quantidade de horas extras.
        minutos_extras (int): Quantidade de minutos extras.

    Returns:
        float: Valor total das horas e minutos extras.
    """
    if valor_hora <= 0:
        return 0.0

    valor_minuto = valor_hora / 60
    return horas_extras * valor_hora + minutos_extras * valor_minuto


def validar_int(valor, nome_campo, max_val=None) -> int:
    """
    Valida se o valor pode ser convertido para int >= 0 e opcionalmente <= max_val.

    Args:
        valor: Valor a validar.
        nome_campo: Nome do campo para mensagem de erro.
        max_val: Valor máximo permitido (opcional).

    Returns:
        int: Valor convertido.

    Raises:
        ValidacaoErro: Se valor inválido ou fora do intervalo.
    """
    try:
        v = int(valor)
        if v < 0:
            raise ValidacaoErro(f"{nome_campo} não pode ser negativo.")
        if max_val is not None and v > max_val:
            raise ValidacaoErro(f"{nome_campo} não pode ser maior que {max_val}.")
        return v
    except Exception:
        raise ValidacaoErro(f"{nome_campo} inválido.")


def validar_float(valor, nome_campo) -> float:
    """
    Valida se o valor pode ser convertido para float >= 0.

    Args:
        valor: Valor a validar.
        nome_campo: Nome do campo para mensagem de erro.

    Returns:
        float: Valor convertido.

    Raises:
        ValidacaoErro: Se valor inválido ou negativo.
    """
    try:
        v = float(valor)
        if v < 0:
            raise ValidacaoErro(f"{nome_campo} não pode ser negativo.")
        return v
    except Exception:
        raise ValidacaoErro(f"{nome_campo} inválido.")


def calcular_salario_bruto(dados: dict, tipo: str, dias_no_mes: int = 30) -> tuple:
    """
    Calcula o salário bruto + benefícios + extras conforme o tipo de trabalhador.

    Args:
        dados (dict): Dados de entrada.
        tipo (str): Tipo de trabalhador: 'Mensalista', 'Horista' ou 'Diarista'.
        dias_no_mes (int): Número de dias no mês para cálculo da hora (default 30).

    Returns:
        tuple: (salario_base, beneficios, extras, bruto, valor_hora)

    Raises:
        ValidacaoErro: Se algum dado inválido ou tipo inválido.
    """
    beneficios = validar_float(dados.get('beneficios', 0), "Benefícios")
    horas_extras = validar_int(dados.get('horas_extras', 0), "Horas extras")
    minutos_extras = validar_int(dados.get('minutos_extras', 0), "Minutos extras", max_val=59)

    if tipo == 'Mensalista':
        salario_base = validar_float(dados.get('salario_base', 0), "Salário base")
        valor_hora = calcular_valor_hora(salario_base, dias_no_mes=dias_no_mes)
    elif tipo == 'Horista':
        valor_hora = validar_float(dados.get('valor_hora', 0), "Valor da hora")
        horas_trabalhadas = validar_int(dados.get('horas_trabalhadas', 0), "Horas trabalhadas")
        salario_base = valor_hora * horas_trabalhadas
    elif tipo == 'Diarista':
        valor_diaria = validar_float(dados.get('valor_diaria', 0), "Valor da diária")
        dias_trabalhados = validar_int(dados.get('dias_trabalhados', 0), "Dias trabalhados")
        salario_base = valor_diaria * dias_trabalhados
        valor_hora = valor_diaria / 8 if valor_diaria > 0 else 0
    else:
        raise ValidacaoErro("Tipo de trabalhador inválido.")

    extras = calcular_extras(valor_hora, horas_extras, minutos_extras)
    bruto = salario_base + beneficios + extras

    return salario_base, beneficios, extras, bruto, valor_hora


def calcular_descontos(bruto: float) -> tuple:
    """
    Calcula descontos do INSS e IRRF com base no salário bruto.

    Args:
        bruto (float): Salário bruto.

    Returns:
        tuple: (inss, irrf)
    """
    inss = calcular_inss(bruto)
    irrf = calcular_irrf(bruto - inss)
    return inss, irrf


def calcular_fgts(bruto: float) -> float:
    """
    Calcula o valor do FGTS como 8% do salário bruto.

    Args:
        bruto (float): Salário bruto.

    Returns:
        float: Valor do FGTS.
    """
    return round(bruto * 0.08, 2)


def calcular_salario_liquido(bruto: float, inss: float, irrf: float) -> float:
    """
    Calcula salário líquido após descontos.

    Args:
        bruto (float): Salário bruto.
        inss (float): Desconto INSS.
        irrf (float): Desconto IRRF.

    Returns:
        float: Salário líquido.
    """
    return bruto - inss - irrf


def gerar_relatorio(dados: dict, tipo: str, dias_no_mes: int = 30) -> str:
    """
    Gera texto formatado com detalhamento do cálculo do salário.

    Args:
        dados (dict): Dados de entrada.
        tipo (str): Tipo de trabalhador.
        dias_no_mes (int): Número de dias no mês para cálculo da hora (default 30).

    Returns:
        str: Relatório detalhado ou mensagem de erro.
    """
    try:
        salario_base, beneficios, extras, bruto, valor_hora = calcular_salario_bruto(dados, tipo, dias_no_mes)
        inss, irrf = calcular_descontos(bruto)
        fgts = calcular_fgts(bruto)
        liquido = calcular_salario_liquido(bruto, inss, irrf)
        valor_minuto = valor_hora / 60 if valor_hora > 0 else 0

        return f"""
👷 Tipo: {tipo}
💰 Salário Base: R$ {salario_base:.2f}
➕ Benefícios: R$ {beneficios:.2f}
➕ Extras: R$ {extras:.2f}
📊 Salário Bruto: R$ {bruto:.2f}
📉 INSS: R$ {inss:.2f}
📉 IRRF: R$ {irrf:.2f}
📂 FGTS (8%): R$ {fgts:.2f}
✅ Salário Líquido: R$ {liquido:.2f}
⏰ Valor da Hora: R$ {valor_hora:.2f}
⏱️ Valor do Minuto: R$ {valor_minuto:.4f}
""".strip()

    except ValidacaoErro as e:
        return f"❌ Erro: {str(e)}"
