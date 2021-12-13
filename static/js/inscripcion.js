function validar(form){
    var mensaje=validarInscripcion();
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
function validarInscripcion(){
    var fecha = new Date();
    var mes =fecha.getMonth() + 1;
    var salida="";
    if(mes!=8){
                salida+="Las inscripciones son en el mes de agosto";
            }
            else{
                salida="";
            }
    return salida;
}