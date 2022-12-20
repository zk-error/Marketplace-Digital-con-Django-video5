

from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from marketplace.models import Product,likes,postview,comentarios
from marketplace.forms import productoformulario,formcomentarios
from django.conf import settings
from django.urls import reverse,reverse_lazy
from django.http.response import JsonResponse

#import stripe #este es para permitir pagos
#stripe.api_key = settings.AUTH_USER_MODEL

class HomeView(View):
    def get(self,request,*args, **kwargs):
        productos_disponibles=Product.objects.filter(active=True)
        form = productoformulario() #guardamos el  formulario en una varioble para pasarla por el context
        paginar_productos_data = None #este es importante cunado hacemos paginacion ya que si no hay productos mostrara un error y por eso hay que poner none
        #para paginar los productos que se veran en coda pagina
        if productos_disponibles:
            paginar = Paginator(productos_disponibles,5 ) #ponemos que vamos a paginal y el numero de post por pagina
            paginar_numeros = request.GET.get('page') #esto es algo que pide pagintor lo podemos guardar en cualquier variable 
            paginar_productos_data=paginar.get_page(paginar_numeros) #esto es lo que vamos a pasar en el contexto osea
            #uniremos los productos disponibles con la cantidad de post por pagina y lo pasaremos al contexto 

        context={
           'hola':paginar_productos_data,
           'hola2':form
        }
        return render(request,'pages/index.html',context)
    def post(self,request,*args, **kwargs):
        form=productoformulario()
        if request.method =='POST':
            form = productoformulario(request.POST,request.FILES) #el segundo es para que permita archivos multimedia
            if form.is_valid():
                form.user = request.user #este es para capturar el usuario actual
                name = form.cleaned_data.get('name')
                descripcion = form.cleaned_data.get('descripcion')
                imagen = form.cleaned_data.get('imagen')
                slug = form.cleaned_data.get('slug')
                content_url = form.cleaned_data.get('content_url')
                cantent_file = form.cleaned_data.get('cantent_file')
                precio = form.cleaned_data.get('precio')
                active = form.cleaned_data.get('active')
                p,created = Product.objects.get_or_create(user=form.user,name=name,descripcion=descripcion,imagen=imagen,slug=slug,content_url=content_url,cantent_file=cantent_file,precio=precio,active=active,)
                p.save()
                return redirect('home')

class userproductos(View):
    def get(self,request,*args, **kwargs):
        lista = Product.objects.filter(user =self.request.user)
        con={
          'lista':lista
        }
        return render(request,'pages/productos/user_productos.html',con)

class editar_producto(UpdateView):
    #model = Product
    form_class = productoformulario
    template_name = 'pages/productos/editar_productos.html' #podemos usar el mismo template que el de crear
    
    def get_queryset(self):
        return Product.objects.filter(user = self.request.user) 

    def get_success_url(self):
        return reverse('productos')

class detalledelprodcuto(View):

    def get(self,request,slug,*args, **kwargs):
        form = formcomentarios()
        #con esto contamos la vista de los usuarios auntenticados namas 
        post = get_object_or_404(Product,slug=slug)
        listacomentarios = comentarios.objects.filter(post=post) #asi filtramos los comentarios solo del post en el que nos metamos 
        if request.user.is_authenticated: # esta condicion es para que solo usuarios autenticados se cuenten las vistas
            postview.objects.get_or_create(usuariovistas=request.user,post=post)
        con={
            'producto':post,
            'form':form,
            'listacomentarios':listacomentarios
        }
        return render(request,'pages/productos/verproducto.html',con)
    def post(self,request,slug,*args, **kwargs):
        form=formcomentarios()
        if request.method =='POST':
            form = formcomentarios(request.POST) 
            if form.is_valid():
                post = get_object_or_404(Product,slug=slug)
                form.user = request.user
                comentario = form.cleaned_data.get('contenido')
                p,created = comentarios.objects.get_or_create(usuariocoments=form.user,post=post,contenido=comentario)
                p.save()
                return redirect('home')


#funcion para contar los likes
def like(request,slug):
    post = get_object_or_404(Product,slug=slug)
    
    like_qs = likes.objects.filter(user=request.user,post=post)
    if like_qs.exists():#si el usuario ya le dio like eliminalo
        like_qs[0].delete()
        return redirect('home')
    
            
    likes.objects.create(user=request.user,post=post)
    return redirect('home')





    """
class createcheckoutsession(View):
    def post(self,request,*args, **kwargs):
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )

        return JsonResponse({
            id:session.id
        })
"""#
