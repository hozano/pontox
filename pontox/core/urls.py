from django.conf.urls import patterns, include, url
from views import TabelaSetorAJAX, RankingAJAX
from django.contrib.auth.views import login,logout, login_required

urlpatterns = patterns('core.views',
    url(r'^index/$', 'index', name='index'),
    url(r'^cad_departamento/$', 'cadDepartamento', name='cadDepartamento'),
    url(r'^$', login, kwargs={'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, kwargs={'next_page':'/'}, name='logout' ),
    url(r'^registros/(?P<setor_id>\d+)$', 'registros', name='registros'),
    url(r'^setor/(?P<setor_id>\d+)$', 'setor', name='setor'),
    url(r'^upload/(?P<setor_id>\d+)$','upload', name='upload'),
    url(r'^detalhes_usuario/(?P<setor_id>\d+)/(?P<usuario_id>\d+)$','detalhesUsuario', name='detalhesUsuario'),
    url(r'^regras/(?P<setor_id>\d+)', 'regras', name='regras'),
    url(r'^tabelaAjax/$', login_required(TabelaSetorAJAX.as_view()), name='tabAJAX'),
    url(r'^rankingAjax/$', login_required(RankingAJAX.as_view()), name='rankAJAX')
)