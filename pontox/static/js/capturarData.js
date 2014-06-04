/**
 * Created by pedro on 5/30/14.
 */
$(document).ready(function(){
    var setorID = $('input[name=setor_id]').val();
    $('#gerar').click(function(){
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
                          '<td><select>'+'<option>Horas por semana</option>'+
                            '<option>Semana 1: '+dados[i].semana1+' <option/>'+
                            '<option>Semana 2: '+dados[i].semana2+' <option/>'+
                            '<option>Semana 3: '+dados[i].semana3+' <option/>'+
                            '<option>Semana 4: '+dados[i].semana4+' <option/>'+
                            '<option>Semana 5: '+dados[i].semana5+' <option/>'+
                           '</select></td>'+
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
    $('#ranking').click(function(){
        var $data = $('input[name=ranking]').val();
        console.log($data.split('-'))
    })
});