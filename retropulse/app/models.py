from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    # Opciones para el campo 'tipo' según la regla de negocio:
    # 1 = Coleccionables, 2 = Tecnología
    TIPO_CHOICES = [
        (1, 'Coleccionables'),
        (2, 'Tecnología Retro'),
    ]

    # cod_producto: entero (Clave primaria autoincremental única)
    cod_producto = models.AutoField(
        primary_key=True, 
        verbose_name="Código de Producto"
    )
    
    # tipo: entero con opciones definidas
    tipo = models.IntegerField(
        choices=TIPO_CHOICES,
        default=1,
        verbose_name="Tipo de Producto"
    )
    
    # nombre: alfanumérico
    nombre = models.CharField(
        max_length=150, 
        verbose_name="Nombre"
    )
    
    # descripción: alfanumérico
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    
    # cantidad_productos: entero (Stock disponible con validador de mínimo 0)
    cantidad_productos = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name="Cantidad / Stock"
    )
    
    # precio_unitario: real (Mapeado a Decimal para alta precisión monetaria)
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name="Precio Unitario"
    )

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        default='productos/default.jpg',
        verbose_name="Imagen del Producto"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['cod_producto']

    def __str__(self):
        tipo_str = "Coleccionable" if self.tipo == 1 else "Tecnología Retro"
        return f"[{self.cod_producto}] {self.nombre} - {tipo_str}"
