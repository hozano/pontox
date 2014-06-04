#coding: utf-8
from django.db import models
from datetime import timedelta, date, datetime
from templatetags.time_format import horas_acumuladas


class Departamento(models.Model):
    nome = models.CharField(max_length=80)

    def ranking_mensal(self):
        return sorted(self.usuario_set.all(), key=lambda usuario: usuario.horas_mes_passado())[::-1][:5]
    def __unicode__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=120)
    departamento = models.ForeignKey(Departamento)
    carga_horaria_semanal = models.IntegerField(default=20,blank=True)

    def horas_mes(self, ano, mes):
        total = timedelta(hours=0, minutes=0)
        for dia in self.diatrabalho_set.all().filter(data__year=ano, data__month=mes):
            total += dia.horas_trabalhadas()
        return total

    def horas_semana(self, ano, mes, semana):
        total = timedelta(hours=0, minutes=0)
        mes = date(year=ano, month=mes, day=1)
        if(semana == 1):
            semana = mes + timedelta(days=6)
        else:
            mes = mes + timedelta(days=(semana-1)*7)
            semana = mes + timedelta(weeks=semana*7)
        for dia in self.diatrabalho_set.filter(data__range=[mes, semana]):
            total += dia.horas_trabalhadas()
        return total

    def horas_as_json(self, ANO, MES):
        ANO = int(ANO); MES = int(MES)
        return dict(
            chave=self.id, nome=self.nome, carga_horaria=self.carga_horaria_semanal,
            horas_mes=horas_acumuladas(self.horas_mes(ANO, MES)),
            semana1=horas_acumuladas(self.horas_semana(ANO, MES, 1)),
            semana2=horas_acumuladas(self.horas_semana(ANO, MES, 2)),
            semana3=horas_acumuladas(self.horas_semana(ANO, MES, 3)),
            semana4=horas_acumuladas(self.horas_semana(ANO, MES, 4)),
            semana5=horas_acumuladas(self.horas_semana(ANO, MES, 5))
        )

    def __unicode__(self):
        return self.nome


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