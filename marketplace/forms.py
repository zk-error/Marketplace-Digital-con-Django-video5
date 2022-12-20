from django import forms
from .models import Product,comentarios

class productoformulario(forms.ModelForm):
    #asi le podemos mandar atributos a nuestro formulario para que se vea mas bonito en este caso el input y al final le decimos que sea requerido
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    slug = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    precio = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    content_url= forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    class Meta:
        model = Product
        fields =(
                'name',
                'descripcion',
                'imagen',
                'slug',
                'content_url',
                'cantent_file',
                'precio',
                'active',
        )
    

        def clean_precio(self,*args, **kwargs):
            precio = self.cleaned_data.get("precio")
            precio = int(precio)
            if precio > 99:
                return precio
            else:
                raise forms.ValidationError("el precio debe ser mayor a 1 dollar ")

class  formcomentarios(forms.ModelForm):
    contenido = forms.CharField(widget=forms.TextInput(attrs={'class':'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),required=True)
    class   Meta:
        model = comentarios
        fields = ('contenido',)       