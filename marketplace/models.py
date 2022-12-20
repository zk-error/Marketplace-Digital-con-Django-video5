

from django.core.validators import FileExtensionValidator #este es para que solo permita algunos tipos de extencion
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import reverse
import os
#ya no heredamos de este porque estamos extendiendo el modelo usuario
#User = get_user_model()#estamos jalando el modelo de usuario que es encuentra en django predeterminado esto igual usa allauth
User = settings.AUTH_USER_MODEL # ahoro usamos este ponque estamos extendinedo del modelo usuaio esto es lo que se pone es settings
#funcion para crear carpeta donde guardaremos nuestra imagenes
def diretorio_de_imagenes(instance,filename): #galamos una instancia de lo que estamos subiendo del objeto y un filename osea el nombre del archivo
    #donde la vamos a guardar marketplace/productos crearemos esas carpetas dentro de media
    #el 0 es para el nambre de nuestra instancia y el uno es el filename
    guardar_en = 'marketplace/productos/{0}/{1}'.format(instance.name,filename)
    full_path = os.path.join(settings.MEDIA_ROOT,guardar_en) #esto es por si queremos remplazar la imagen 
    #la removemos y ya esta
    if os.path.exists(full_path):
        os.remove(full_path)
    return guardar_en

class Product(models.Model):      #esto kiere decir que si elminamos el usuario se borran todos sus productos que a creado el usuario eso hace cascade osea borra todo lo que hace el usuario
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(blank=True,null = True,upload_to = diretorio_de_imagenes )
    slug = models.SlugField(unique=True)
    #es usuario va a tener la posivilidad de subir elegir en vender dos tipos de productos obio podemos agregar mas 
    content_url = models.URLField(blank=True,null=True)
    cantent_file = models.FileField(blank=True,null=True)
    #de esta manera solo pudiemos permitir un tipo de extencion
    #cantent_file = models.FileField(blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    active = models.BooleanField(default=False)
    #100 es un dolar creo que el precio inicial
    precio = models.PositiveIntegerField(default=100) #

    def __str__(self):
        return self.name
    #con esta funcion hacemos que el precio se vea bonito
    def price_display(self):
        #vamos a retornar el precio con 2 decimales y lo dividimos entre 100 para que muestre 1.00 dolar en ves de 100
        return "{0:.2f}".format(self.precio/100)
    #podemos uar esta o directamente en urls.py 
    #funcion para los likes
    #def get_like_url(self):
        #return reverse("like",kwargs={
         #  'slug':self.slug 
        #}) 
    #no se porque con la clase view no funciona
    #propiedad pora listar todos los comentarios
    @property
    def comments(self):
        return self.comentarios_set.all()  

    #el return retorna el conteo de las clases de abajo esto se puede poro que hay una union con forenkey
    #aremos una funcion para contar los camentarios,vistas y likes
    @property
    def get_comment_count(self):
        return self.comentarios_set.all().count()

    @property
    def get_view_count(self):
        return self.postview_set.all().count()
    
    @property
    def get_like_count(self):
        return self.likes_set.all().count()


class producto_comprado(models.Model):
    email = models.EmailField()#va a hacer el email del usuario que compro
    producto = models.ForeignKey(Product,on_delete=models.CASCADE)
    fecha_de_comprado = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.email


class comentarios(models.Model):
    usuariocoments = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuariocoments')
    post = models.ForeignKey(Product,on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    contenido = models.TextField()
    
    

#numero de vistas de mi post
class postview(models.Model):
    usuariovistas = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuarioviews')
    post = models.ForeignKey(Product,on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.usuariovistas

class likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='usuariolikes')
    post = models.ForeignKey(Product,on_delete=models.CASCADE)
   