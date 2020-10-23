(function(){
    //Iniciar y crear ventana
	function ModalSignin( element ) {
		this.element = element;
		this.blocks = this.element.getElementsByClassName('js-signin-modal-block');
		this.switchers = this.element.getElementsByClassName('js-signin-modal-switcher')[0].getElementsByTagName('a'); 
		this.triggers = document.getElementsByClassName('js-signin-modal-trigger');
		this.hidePassword = this.element.getElementsByClassName('js-hide-password');
		this.init();
	};

	ModalSignin.prototype.init = function() {
		var self = this;
		//Mostrar y ocultar funcion
		for(var i =0; i < this.hidePassword.length; i++) {
			(function(i){
				self.hidePassword[i].addEventListener('click', function(event){
					self.togglePassword(self.hidePassword[i]);
				});
			})(i);
		} 
    };
    
	//cambiar el texto segun ocultar o mostrar
	ModalSignin.prototype.togglePassword = function(target) {
		var password = target.previousElementSibling;
		( 'password' == password.getAttribute('type') ) ? password.setAttribute('type', 'text') : password.setAttribute('type', 'password');
		target.textContent = ( 'Mostrar' == target.textContent ) ? 'Ocultar' : 'Mostrar';
		putCursorAtEnd(password);
	}

	var signinModal = document.getElementsByClassName("js-signin-modal")[0];
	if( signinModal ) {
		new ModalSignin(signinModal);
	}	


})();

function checkRut(rut) {
	// Despejar Puntos
	var valor = rut.value.replace('.','');
	// Despejar Guión
	valor = valor.replace('-','');
	
	// Aislar Cuerpo y Dígito Verificador
	cuerpo = valor.slice(0,-1);
	dv = valor.slice(-1).toUpperCase();
	
	// Formatear RUN
	rut.value = cuerpo + '-'+ dv
	
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
	if(dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }
	
	// Si todo sale bien, eliminar errores (decretar que es válido)
	rut.setCustomValidity('');
}
