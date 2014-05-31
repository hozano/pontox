/**
 * Created by pedro on 5/30/14.
 */
$(document).ready(function(){
    $('#gerar').click(function(){
        var setorID = $('input[name=setor_id]').val();
        var $data = $('input[name=data]').val();
        if($data != null){
            $data = $data.split('-');
            $.ajax({
                data : {'ano':$data[0], 'mes':$data[1], 'setor_id':setorID},
                type : 'get',
                url : '/tabelaAjax/',
                success : function(dados){
                    var tabela='<table class="table table-striped table-bordered table-hover">'+
                      '<thead><tr><th>Nome</th><th>CH Mês</th><th>CH Semanal</th></tr>'+
                      '</thead><tbody id="tabelaPrincipal">';
                    for(var i=0; i < dados.length; i++){
                        tabela += '<tr>'+
                          '<td><a href="/detalhes_usuario/'+setorID+'/'+dados[i].chave+'">'+dados[i].nome+'</a></td>'+
                          '<td>'+dados[i].horas_mes+'</td>'+
                          '<td></td>'+
                        '</tr>'
                    }
                    tabela+='</tbody></table>';
                    $('#tabelaPrincipal').html(tabela);
                }
            });
        }
        else{
            alert("Antes de realizar a busca, insira uma data!");
        }
    });
});