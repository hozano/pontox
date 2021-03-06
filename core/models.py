#coding: utf-8
from django.db import models
from datetime import timedelta, date, datetime
from templatetags.time_format import horas_acumuladas
from calendar import Calendar


class Departamento(models.Model):
    nome = models.CharField(max_length=80)

    def ranking_mensal(self, ano, mes):
        return sorted(self.usuario_set.all(), key=lambda usuario: usuario.horas_mes(ano, mes))[::-1][:5]

    def ranking_as_json(self, ANO, MES):
        ranking = self.ranking_mensal(ANO, MES)
        return dict(
            primeiro_nome=ranking[0].nome, primeiro_horas=horas_acumuladas(ranking[0].horas_mes(ANO, MES)),
            segundo_nome=ranking[1].nome, segundo_horas=horas_acumuladas(ranking[1].horas_mes(ANO, MES)),
            terceiro_nome=ranking[2].nome, terceiro_horas=horas_acumuladas(ranking[2].horas_mes(ANO, MES)),
            quarto_nome=ranking[3].nome, quarto_horas=horas_acumuladas(ranking[3].horas_mes(ANO, MES)),
            quinto_nome=ranking[4].nome, quinto_horas=horas_acumuladas(ranking[4].horas_mes(ANO, MES)),
        )

    def usuarios_ativos(self):
        return Usuario.objects.filter(departamento=self, ativo=True)

    def __unicode__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=120)
    departamento = models.ForeignKey(Departamento)
    carga_horaria_semanal = models.IntegerField(default=20,blank=True)
    ativo = models.BooleanField(default=True)

    def horas_mes(self, ano, mes):
        total = timedelta(hours=0, minutes=0)
        for dia in self.diatrabalho_set.all().filter(data__year=ano, data__month=mes):
            total += dia.horas_trabalhadas()

        return total

    def horas_semana(self, ano, mes, semana):

        total = timedelta(hours=0, minutes=0)

        calendario = Calendar()
        listasemana = calendario.monthdays2calendar(year=ano, month=mes)

        try:
            for dia in listasemana[semana]:
                if not dia[0] == 0:
                    diatrabalhado = self.diatrabalho_set.filter(data=datetime(year=ano, month=mes, day=dia[0]))
                    if diatrabalhado:
                        diatrabalhado = diatrabalhado[0]
                        total += diatrabalhado.horas_trabalhadas()

            return total
        except IndexError:
            return timedelta(hours=0, minutes=0)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

class DiaTrabalho(models.Model):
    data = models.DateField()
    usuario = models.ForeignKey(Usuario)


    class Meta:
        ordering = ['-data']

    def __unicode__(self):
        return "Data: " + unicode(self.data)

    def horas_trabalhadas(self):
        tempo = timedelta(hours=0, minutes=0)
        for regra in self.usuario.departamento.regra_set.all():
            tempo += regra.horas_trabalhadas(self)

        return tempo


class Registro(models.Model):
    registro = models.DateTimeField(format('%m/%d/%Y %H:%M'))
    dia_trabalho = models.ForeignKey(DiaTrabalho)

    class Meta:
        ordering = ['-registro']

    def __unicode__(self):
        return "Entradas: "+str(self.registro)


class Regra(models.Model):
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return self.horario_entrada.__str__() + '-' + self.horario_saida.__str__()

    def horas_trabalhadas(self, dia_trabalho):
        registros = dia_trabalho.registro_set.all()
        inicio = None
        tempo = timedelta(hours=0, minutes=0)
        for registro in registros:
            if (not inicio) and (self.horario_entrada <= registro.registro.time() <= self.horario_saida):
                inicio = registro.registro
            elif inicio and (self.horario_entrada <= registro.registro.time() <= self.horario_saida):
                fim = registro.registro
                tempo = inicio-fim
                inicio = None
        return tempo

class Upload(models.Model):
    titulo = models.CharField(max_length=120)
    arquivo = models.FileField(upload_to='media/%Y%m%d')