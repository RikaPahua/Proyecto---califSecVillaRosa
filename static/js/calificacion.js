function validar(form){
    var bimestre=form.bimestre.value;
    var mensaje=validarBimestre(bimestre);;
    var div=document.getElementById("notificaciones");
    var ban=false;
    if(mensaje!=""){
        div.innerHTML=mensaje;
        ban=false;
    }
    else{
        div.innerHTML="";
        ban=true;
    }
    return ban;
}

function validarBimestre(cadena){
    var salida="";
    if(cadena=="Seleccionar"){
        salida='Debes seleccionar un bimestre. <br>';
    }
    return salida;
}

function consultarCal(){
    var ajax=new XMLHttpRequest();
    var idCalificacion=document.getElementById("idCalificacion").value;
    var bimestre=document.getElementById("bimestre").value;
    var url="/detalleCal/bimestre/"+bimestre+","+idCalificacion;
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