/**
 * Created by pedro on 6/25/14.
 */
$(document).ready(function(){
    var alterado ='<div id="datetimepicker2" class="input-append input-group dtpicker">'+
        '<input id="id_horario_entrada" name="horario_entrada" type="text">'+
        '<span class="input-group-addon add-on"><i data-time-icon="fa fa-clock-o" data-date-icon="fa fa-calendar"'+
        ' class="fa fa-clock-o"></i></span></div>'
    $('input.id_horario_entrada').html(alterado);
});
