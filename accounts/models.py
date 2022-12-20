import email
from tabnanny import verbose
from django.db import models
from django.db.models.signals import post_save
#con este podemos extender la caractisticas del modelo usuario
from django.contrib.auth.models import AbstractUser
from marketplace.models import Product,producto_comprado

class user(AbstractUser):
    stripe_customer_id = models.CharField(max_length=50)

#libreria para asignarle los productos a los usuarios
class userlibreria(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,related_name='library')
    productos = models.ManyToManyField(Product,blank=True)

    class Meta:
       verbose_name_plural = 'user librerias' 

    def __str__(self):
        return self.user.email

#este es para que cada que se cree un usuario se le asigne una libreria esto es muy importante
#sender este es el que esta enviando la seÑal
#instance este es el usuario que esta siendo creado
#created es para que ocurre cuando es creado
def post_save_user_receiver(sender,instance,created,**kwargs):
    if created:#si el usuario es creado
        #le asignamos una libreria
        libreria = userlibreria.objects.create(user=instance)
        #si el usuario a comprado un producto  tenemos que asicnar ese producto al email 
        productos_lita = producto_comprado.objects.filter(email=instance.email)#filtromos el email del usuario y queremos el email del usuario que esta siendo registrado instance.email
        #hacemos un for de los productos que a comprado si es que a comprado
        for i in productos_lita:
            libreria.producto.add(i.producto) #asignamos los productos a la libreria

#asi se guardo la funcion
post_save.connect(post_save_user_receiver,sender=user)


