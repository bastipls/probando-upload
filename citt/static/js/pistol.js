( function( ) {
    const txtName = document.getElementById( "txtName" );
    const datalist = document.getElementById("datalist-event");
    const titleEvennt = document.getElementById("event-now");

    titleEvennt.innerHTML = datalist.value;
    txtName.focus();
    if (document.getElementById('alert')){
        setTimeout(function() {document.getElementById('alert').style.display = "none";},3000);
    }
}) ( );


function checkRut(rut) {
 
    // Despejar Puntos
    var valor = rut.value.replace('.','');
    // Despejar Guión
    //valor = valor.replace("-",'');
    valor = valor.replace("'",'');
    
    // Aislar Cuerpo y Dígito Verificador
    cuerpo = valor.slice(0,-1);
    dv = valor.slice(-1).toUpperCase();
    var filtro = "456789";//Caracteres valido
    //Esto lo hago para verificar si el rut es 9 millones osea 7 digitos si asi
    //Quito todas las validaciones debido a que tengo conflicto con los carent y la pistola
    if (filtro.indexOf(txtName.value.charAt(0)) != -1) {
        rut.setCustomValidity('');
      
    }else{
       
    // Formatear RUN
    //rut.value = cuerpo +"'"+ dv
    
    // Si no cumple con el mínimo ej. (n.nnn.nnn)
    if(cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false;}
    
    // Calcular Dígito Verificador
    suma = 0;
    multiplo = 2;
    
    // Para cada dígito del Cuerpo
    for(i=1;i<=cuerpo.length;i++) {
    
        // Obtener su Producto con el Múltiplo Correspondiente
        index = multiplo * valor.charAt(cuerpo.length - i);
        
        // Sumar al Contador General
        suma = suma + index;
        
        // Consolidar Múltiplo dentro del rango [2,7]
        if(multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
  
    }
    
    // Calcular Dígito Verificador en base al Módulo 11
    dvEsperado = 11 - (suma % 11);
    
    // Casos Especiales (0 y K)
    dv = (dv == 'K')?10:dv;
    dv = (dv == 0)?11:dv;
    
    // Validar que el Cuerpo coincide con su Dígito Verificador
    if(dvEsperado != dv) 
    {
     rut.setCustomValidity("RUT Inválido");
     return false; 
    }
      // Si todo sale bien, eliminar errores (decretar que es válido)
      rut.setCustomValidity('');
    }

    if(txtName.value.indexOf("'")!=-1 ){
        rut.setCustomValidity('');
    }else{
        rut.setCustomValidity("Falta comilla '")
        return false;
    }
  
    
}


function soloRut(string){//Solo ruts formato con guión
    var out = '';
    var filtro = "1234567890'kK";//Caracteres validos
	
    //Recorrer el texto y verificar si el caracter se encuentra en la lista de validos 
    for (var i=0; i<string.length; i++)
       if (filtro.indexOf(string.charAt(i)) != -1) 
             //Se añaden a la salida los caracteres validos
	     out += string.charAt(i);
	 
    //Retornar valor filtrado
    return out;
} 



