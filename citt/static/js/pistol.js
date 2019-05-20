( function( ) {
    const txtName = document.getElementById( "txtName" );
    const txtResults = document.getElementById( "results" );
    const nameForm = document.getElementById( "nameForm" );
    const datalist = document.getElementById("datalist-event");
    const titleEvennt = document.getElementById("event-now");

    titleEvennt.innerHTML = datalist.value;
    txtName.focus();
    if (document.getElementById('alert')){
        setTimeout(function() {document.getElementById('alert').style.display = "none";},3000);
    }
 
    txtName.addEventListener("input",  ( e ) => {   
    });
        




    
}) ( );



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



