// script.js
function createRol(name, description) {
    Swal.fire({
      title: "Crear Rol",
      confirmButtonText: 'Crear',
      confirmButtonColor: '#28a745',
      showCloseButton: true,
      focusConfirm: true,
      
      html: `
      <div>
        <label for="swal-input1">Nombre:</label>
        <input id="swal-input1" class="swal2-input" value="">
      </div>
      <div > 
          <label for="swal-input2">Descripción:</label style = "margin-left:100px;">
          <input id="swal-input2" class="swal2-input" value="" style = "margin-left:20px;">
      </div>
      `,

      focusConfirm: false,
      preConfirm: () => {
        return [
          document.getElementById("swal-input1").value,
          document.getElementById("swal-input2").value,
        ];
      },
    }).then((result) => {
      if (result.value) {
        Swal.fire({
            icon: 'success',
            confirmButtonColor: '#28a745',
            text: 'Rol Creado',
          })
        //Swal.fire(JSON.stringify(result.value));
        // Aquí puedes realizar la lógica de actualización de usuario si es necesario
      }
    });
  }
  
// script.js
function editRol(name, description) {
    Swal.fire({
      title: "Editar Rol",
      confirmButtonText: 'Actualizar',
      confirmButtonColor: '#28a745',
      showCloseButton: true,
      focusConfirm: true,
      
      html: `
      <div>
        <label for="swal-input1">Nombre:</label>
        <input id="swal-input1" class="swal2-input" value="${name}">
      </div>
      <div > 
          <label for="swal-input2">Descripción:</label style = "margin-left:100px;">
          <input id="swal-input2" class="swal2-input" value="${description}" style = "margin-left:20px;">
      </div>
      `,

      focusConfirm: false,
      preConfirm: () => {
        return [
          document.getElementById("swal-input1").value,
          document.getElementById("swal-input2").value,
        ];
      },
    }).then((result) => {
      if (result.value) {
        Swal.fire({
            icon: 'success',
            confirmButtonColor: '#28a745',
            text: 'Rol Actualizado',
          })
        //Swal.fire(JSON.stringify(result.value));
        // Aquí puedes realizar la lógica de actualización de usuario si es necesario
      }
    });
  }
  
  function redirectcreateRol() {
    window.location.href = '/roles/create_rol/';
}