function consultarCal(){
    var ajax=new XMLHttpRequest();
    var idProfesor=document.getElementById("idProfesor").value;
    var dia=document.getElementById("dia").value;
    var horarioInicio=document.getElementById("horarioInicio").value;
    var url="/horario/dia/"+dia+","+horarioInicio+","+idProfesor;
    var div=document.getElementById("notificaciones");
    ajax.open("get",url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }
            else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();
}