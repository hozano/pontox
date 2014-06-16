from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from core.models import Upload, Usuario, Registro, Departamento, DiaTrabalho
from core.forms import UploadForm, DepartamentoForm, RegraForm
from django.views.generic import TemplateView
import json
from datetime import datetime

@login_required
def index(request):
    departametos = Departamento.objects.all()
    count=range(1,100)[::-1]
    if request.method == 'POST':
        chaveDep = request.POST.get("chaveDep","")
        dep = Departamento.objects.get(pk=chaveDep)
        dep.delete()
        return HttpResponseRedirect(reverse('index'))
    return render(request,'index.html', {'departamentos':departametos, 'count':count})

@login_required
def cadDepartamento(request):
    formDep = DepartamentoForm()
    if request.method == 'POST':
        formDep = DepartamentoForm(request.POST)
        if formDep.is_valid():
            messages.success(request, 'Cadastrado com sucesso!')
            formDep.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'cadDepartamento.html', {'formDep':formDep})

@login_required
def upload(request, setor_id):
    form = UploadForm()
    departamento = Departamento.objects.get(pk=setor_id)
    if departamento.regra_set.all() == None:
        departamento = True
    else:
        departamento = False

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid:
            messages.success(request, 'Carregado com sucesso!')
            arquivo = Upload(arquivo=request.FILES['arquivo'], titulo=request.POST['titulo'])
            arquivo.save()

            #Inicio do tratamento do arquivo
            linhas = arquivo.arquivo.readlines()
            linhas.pop(0)
            #Objeto modelo para tratar as datas
            d = datetime.now()
            for i in linhas:
                info = i.split("	"); nome = info[3]; dataHora = info[4]
                name = nome.replace(" ", "");dateTime = dataHora.replace("\r\n", "")
                dateTime = dateTime.replace("  "," ")
                dateTime = d.strptime(dateTime,"%Y/%m/%d %H:%M")

                data = dateTime.date()

                usuario, created = Usuario.objects.get_or_create(
                    nome=name,departamento=Departamento.objects.get(id=setor_id),
                    carga_horaria_semanal=20)
                dia_trabalho, created = DiaTrabalho.objects.get_or_create(usuario=usuario, data=data)

                Registro.objects.get_or_create(dia_trabalho=dia_trabalho, registro=dateTime)
            return HttpResponseRedirect(reverse('upload',args=(setor_id)))
    arquivos = Upload.objects.all()
    return render(request, 'upload.html', {'form':form, 'arquivos':arquivos,
                'setor_id':setor_id, 'departamento':departamento})

@login_required
def registros(request, setor_id):
    setor = Departamento.objects.get(pk=setor_id)
    return render(request, 'registros.html', {'setor':setor, 'setor_id':setor_id})

@login_required
def setor(request, setor_id):
    departamento = Departamento.objects.get(pk=setor_id)
    return render(request, 'setor.html',{'setor_id':setor_id, 'departamento':departamento})

@login_required
def detalhesUsuario(request,setor_id, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)
    return render(request, 'detalhesUsuario.html', {'setor_id':setor_id, 'usuario':usuario})

@login_required()
def regras(request, setor_id):
    form = RegraForm()
    if request.method == 'POST':
        form = RegraForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Regra adicionanda com sucesso!')
            form = form.save(commit=False)
            form.departamento = Departamento.objects.get(pk=setor_id)
            form.save()
            return HttpResponseRedirect(reverse('setor',args=setor_id))
    return render(request, 'regras.html', {'setor_id':setor_id, 'form':form,})

class TabelaSetorAJAX(TemplateView):
    def get(self, request, *args, **kwargs):
        ano = request.GET['ano']
        mes = request.GET['mes']
        departamento = Departamento.objects.get(pk=request.GET['setor_id'])
        usuarios = departamento.usuario_set.all()

        dados = [usuario.horas_as_json(ANO=ano, MES=mes) for usuario in usuarios]

        return HttpResponse(json.dumps(dados), content_type='application/json')

class RankingAJAX(TemplateView):
    def get(self, request, *args, **kwargs):
        ano = request.GET['ano']
        mes = request.GET['mes']
        departamento = Departamento.objects.get(pk=request.GET['setor_id'])

        dados = [departamento.ranking_as_json(ano, mes)]

        return HttpResponse(json.dumps(dados), content_type='application/json')