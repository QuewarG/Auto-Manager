# En tu aplicación (donde se encuentran tus modelos), crea un archivo signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, PersonaXCargo, Cargo

@receiver(post_save, sender=Usuario)
def crear_persona_por_cargo(sender, instance, created, **kwargs):
    if created:
        roles_a_cargos = {
            'Superadministrador': 'Gerente',  # Asignando el cargo de Gerente a los Superadministradores
            'Gerente': 'Gerente',
            'Vendedor': 'Vendedor',
            'Jefe de taller': 'Jefe de taller',
            'Cliente': 'Cliente',
            # Agrega otros roles y sus correspondientes cargos aquí
        }

        cargo_nombre = roles_a_cargos.get(instance.cod_rol.rol_nombre, None)

        if cargo_nombre is not None:
            cargo_encontrado = Cargo.objects.filter(cargo_nombre=cargo_nombre).first()

            if cargo_encontrado:
                persona_por_cargo = PersonaXCargo(
                    perxcargo_persona_cod_id=instance.id,
                    perxcargo_cargo_cod_id=cargo_encontrado.cargo_cod,
                    perxcargo_sucursal_cod_id=7,  # Asigna la sucursal correspondiente
                    perxcargo_vigente=True,
                    # Otros campos según tus necesidades
                )
                persona_por_cargo.save()