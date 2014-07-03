/**
 * Created by pedro on 5/30/14.
 */
$(document).ready(function(){
    var setorID = $('input[name=setor_id]').val();
    var d = new Date(), mes = d.getMonth()+1, ano = d.getFullYear();
    updateTable(ano+'-'+mes);
    updateRanking(ano+'-'+mes);
    $('#gerar').click(function(){
        var $data = $('input[name=data]').val();
        if($data != ""){
            updateTable($data);
        }
        else{
            alert("Antes de realizar a busca, insira uma data!");
        }
    });
    $('#ranking_btn').click(function(){
        var $data = $('input[name=ranking]').val();
        if($data != ""){
            updateRanking($data);
        }
    });
    function updateRanking($data){
            $data = $data.split('-');
            console.log($data);
            $.ajax({
                data : {'ano':$data[0], 'mes':$data[1], 'setor_id':setorID},
                type : 'get',
                url : '/rankingAjax/',
                success : function(dados){
                     var tabela='<table id="ranking_tabela" class="table table-striped table-bordered table-hover">'
                    +'<tr><th><center>#</center></th><th>Colaborador</th><th>Número de Horas</th></tr>'

                    tabela+=
                    '<tr><th>1</th><th>'+dados[0].primeiro_nome+'</th>'+
                    '<th>'+dados[0].primeiro_horas+'</th></tr>' +
                     '<tr><th>2</th><th>'+dados[0].segundo_nome+'</th>'+
                    '<th>'+dados[0].segundo_horas+'</th></tr>'+
                    '<tr><th>3</th><th>'+dados[0].terceiro_nome+'</th>'+
                    '<th>'+dados[0].terceiro_horas+'</th></tr>' +
                     '<tr><th>4</th><th>'+dados[0].quarto_nome+'</th>'+
                    '<th>'+dados[0].quarto_horas+'</th></tr>'+
                     '<tr><th>5</th><th>'+dados[0].quinto_nome+'</th>'+
                    '<th>'+dados[0].quinto_horas+'</th></tr>';

                    $('#ranking_tabela').html(tabela);
                }
            });
    }
    function updateTable($data){
            $data = $data.split('-');
            var meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
            $.ajax({
                data : {'ano':$data[0], 'mes':$data[1], 'setor_id':setorID},
                type : 'get',
                url : '/tabelaAjax/',
                success : function(dados){
                    var tabela='<table id="tabelaPrincipal" class="table table-striped table-bordered table-hover">'+
                      '<thead><tr><th>Nome</th><th>CH Mês</th><th>CH Semanal</th></tr>'+
                      '</thead><tbody>';
                    for(var i=0; i < dados.length; i++){
                        tabela += '<tr>'+
                          '<td><a href="/detalhes_usuario/'+setorID+'/'+dados[i].chave+'">'+dados[i].nome+'</a></td>'+
                          '<td>'+dados[i].horas_mes+'</td>'+
                          '<td>'+
                            '<label class="label label-success">'+dados[i].semana1+'</label>'+
                            '<label class="label label-warning">'+dados[i].semana2+'</label>'+
                            '<label class="label label-danger">'+dados[i].semana3+'</label>'+
                            '<label class="label label-primary">'+dados[i].semana4+'</label>'+
                           '</td>'+
                        '</tr>'
                    }
                    tabela+='</tbody></table>';
                    $('#tabelaPrincipal').dataTable().fnClearTable();
                    $('#tabelaPrincipal').html(tabela);
                    initTable(meses[$data[1]-1]+' de '+$data[0]);

                }
            });
};
});
function initTable(entrada){
    $('#tabelaPrincipal').dataTable({
      "order": [[ 3, "desc" ]],
      "bDestroy": true,
      "sDom": 'T<"clear">lfrtip',
        "tableTools": {
            "sSwfPath": "/copy_csv_xls_pdf.swf",
            "aButtons": [ {
                    "sExtends": "print",
                    "sMessage":"<div class='col-med-4'><div class='well'>"+
                        '<center><h2>'+entrada+'</h2></center>'+"<div><div>"
                }  ]
        }
    });
}