from django import template
from core.models import DiaTrabalho, Usuario

register = template.Library()

@register.simple_tag()
def horas_mes(usuario_id, ano, mes):
    usuario = Usuario.objects.get(id=int(usuario_id))
    return usuario.horas_mes(ano, mes)

MONTHS = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
@register.simple_tag()
def month_tabs(depto, ano, mes):
    from datetime import date
    data = date(ano, mes, 1)
    ate = date.today()
    dias = DiaTrabalho.objects.filter(usuario__departamento__id=depto).order_by('-data')
    if dias:
        ultimo_dia = dias[0]
        if ultimo_dia.data > ate:
            ate = ultimo_dia.data

    result = ""

    desde = date.today()
    dias_desde = DiaTrabalho.objects.filter(usuario__departamento__id=depto).order_by('data')
    if dias_desde:
        desde = dias_desde[0]

    if desde.data.year < data.year:
        result += """
            <li>
                <a href="/setor/%s/%s/%s">
                    <i class="green fa fa-arrow-left bigger-110"></i>
                    %s
                </a>
            </li>
            """ % (depto,data.year-1,12,data.year-1)
    for i in range(1,13):
        iter_date = date(data.year, i, 1)
        tupla_criacao = (desde.data.year, desde.data.month)
        tupla_iter = (iter_date.year, iter_date.month)
        tupla_ate = (ate.year, ate.month)
        if (tupla_criacao <= tupla_iter <= tupla_ate):
            active = ""
            if (data.month == iter_date.month) and (data.year == iter_date.year):
                active = "class='active'"
            result += """
                <li %s>
                    <a  href="/setor/%s/%s/%s">
                        %s/%s
                    </a>
                </li>
                """ % (active, depto, iter_date.year,iter_date.month,MONTHS[iter_date.month-1], str(iter_date.year)[2:])
    if ate.year > data.year:
        result += """
            <li>
                <a href="/setor/%s/%s/%s">
                    %s
                    <i class="green fa fa-arrow-right bigger-110"></i>
                </a>
            </li>
            """ % (depto, data.year+1,1,data.year+1)
    return result