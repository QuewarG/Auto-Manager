// script.js
function createUser(name, email, rol) {
    Swal.fire({
      title: "Crear Usuario",
      confirmButtonText: 'Crear',
      confirmButtonColor: '#28a745',
      showCloseButton: true,
      focusConfirm: true,   

      html: `
      <form method="post">
      <div>
        <label for="swal-input1">Nombre:</label>
        <input id="swal-input1" class="swal2-input" value="${name}">
      </div>
      <div > 
        <label for="swal-input2">UserName:</label style = "margin-left:100px;">
        <input autofocus id="swal-input2" class="swal2-input" value="" style = "margin-left:20px;">
      </div>
      <div> 
        <label for="swal-input3">Nro Doc:</label>
        <input id="swal-input3" class="swal2-input" value="">
      </div>
      <div>
        <label for="swal-input4">Email:</label>
        <input id="swal-input4" class="swal2-input" value="" style="margin-left: 65px;">
      </div>
      <div> 
        <label for="swal-input5">Telefono:</label>
        <input id="swal-input5" class="swal2-input" value="">
      </div>
      <div style="margin-right:110px; margin-top:25px;">
        <label for="swal-input6">Rol:</label>
        <select id="swal-input6" class="swal2-input" style="margin-left:150px;">
          <option value="admin" ${rol === 'admin' ? 'selected' : ''}>Admin</option>
          <option value="user" ${rol === 'user' ? 'selected' : ''}>User</option>
        </select>
      </div>
      </form>
      `,
      preConfirm: () => {
        return [
          document.getElementById("swal-input1").value,
        ];
      },
    }).then((result) => {
      if (result.value) {
        Swal.fire({
          icon: 'success',
          confirmButtonColor: '#28a745',
          text: 'Usuario creado exitosamente',
        })
        //Swal.fire(JSON.stringify(result.value));
        // Aquí puedes realizar la lógica de actualización de usuario si es necesario
      }
    });
  }
  