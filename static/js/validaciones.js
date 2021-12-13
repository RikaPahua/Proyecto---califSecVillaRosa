function validarC(form){
    var nombre=form.nombre.value;
    var mensaje=validarNombre(nombre);
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
function validarNombre(cadena){
    var patron=/[0-9]{4}-[0-9]{4}/
    var ban=patron.test(cadena);
    var salida="";
    if(ban==false){
        salida='Debes informar un nombre de ciclo con el siguiente patron: ####-####. <br>';
    }
    return salida;
}



function consultarCiclos(){
    var ajax=new XMLHttpRequest();
    var nombre=document.getElementById("nombre").value;
    var url="/cicloEsc/nombre/"+nombre;
    var div=document.getElementById("notificacionesNom");
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

function consultarMateria(){
    var ajax=new XMLHttpRequest();
    var nombre=document.getElementById("nombre").value;
    var url="/materia/nombre/"+nombre;
    var div=document.getElementById("notificacionesNomM");
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