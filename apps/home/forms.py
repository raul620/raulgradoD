
from django import forms
from django.core.validators import *
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseFormSet, formset_factory, modelform_factory, modelformset_factory

#from django_select2 import forms as s2forms
from django.forms import *
from django.forms import ModelForm
from .models import *

from django import forms

class ServiceRequestForm(ModelForm):
    
    title = CharField(
        
        widget=TextInput(
            attrs={
                'placeholder': 'Mis archivos estan corruptos, como los recupero?',
                'class': 'form-control',
                  'required': 'False'
                
            }
        ))
    
    
    Area = ModelChoiceField(required = False,queryset=Area.objects.all(),widget=Select(attrs={
        'class':'form-control',
        
    }))
   
    ComputoRegistrado= ModelChoiceField(required = False,queryset=ComputoRegistrado.objects.all(),widget=Select(attrs={
        'class':'form-control',
         
    }))
    
    
    ip_dir = CharField(
        required = False,
        widget=TextInput(
            attrs={
                'placeholder': 'Direccion IP',
                'class': 'form-control ',
                
            }
        ))
    
    mac_dir = CharField(
        required = False,
        widget=TextInput(
            attrs={
                'placeholder': 'Direccion MAC',
                'class': 'form-control ',
                
            }
        ))
    description = CharField(
        
        widget=Textarea(
            attrs={
           'placeholder': 'Description',
                'class': 'form-control',
                  'style':'color:white',
                'required': 'False'
            }
        ))
    screenshot =ImageField(
         required = False,
  
        label='',
         widget = forms.FileInput(
            attrs = { # add style fr"om here .
             'required': 'False'
         
                 
                    }
            )
    )
    
    class Meta:

        model = ServiceRequest
        
        fields = (
            'title',
            'ip_dir',
            'mac_dir',
            'description',
            'screenshot',
            'tags',
            'Area',
            'ComputoRegistrado'
         
          
            )
        
                
        def __init__():
            fields['screenshot'].required = False
        ''',
        widgets = {
            'title': TextInput(attrs={'class':'form-control'}),
            'ip_dir': TextInput(attrs={'class':'form-control'}),
            'mac_dir': TextInput(attrs={'class':'form-control'}),
            'description': TextInput(attrs={'class':'form-control'})
        }'''
        


class ServiceResponseForm(ModelForm):
    

    description = CharField(
        
        widget=Textarea(
            attrs={
           'placeholder': 'Description',
                'class': 'form-control',
                'style':'color:black',
                  'required':'false'
            }
        ))
    screenshot =ImageField(
       
    )
    
    class Meta:
        model = ServiceResponse
        fields = (
      
            'description',
            'screenshot',
        
            )




class EquipoForm(forms.ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'nombre_equipo': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
                'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
                                'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
                'screenshot': forms.ImageField()

        }


class SoftwareForm(forms.ModelForm):

    class Meta:
        model = Software
        fields = '__all__'
        widgets = {
            'nombre_software': forms.TextInput(
                attrs={
                    'class': 'form-control',
                      'required':'false'
                    }
                ),
                        'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                      'required':'false'
                    }
                ),
             'screenshot': forms.ImageField()

        }




SoftwareFormSet = inlineformset_factory(
    ServiceRequest, Software, form=SoftwareForm,

    extra=1, can_delete=True,
    can_delete_extra=True
)
EquipoFormSet = inlineformset_factory(
    ServiceRequest, Equipo, form=EquipoForm,
    
    extra=1, can_delete=True,
    can_delete_extra=True
)




class AreaForm(forms.ModelForm):
    nombre = CharField(
        
        widget=TextInput(
            attrs={
    
                'class': 'form-control',
                  'required':'false'
             
            }
        ))
    class Meta:
        model = Area
        fields = '__all__'

class ComputoRegistradoForm(forms.ModelForm):

    modelo = CharField(
        
        widget=TextInput(
            attrs={
           'placeholder': 'Modelo de tu equipo',
                'class': 'form-control',
                'style':'color:black',
                  'required':'false'
                
            }
        ))
    caracteristicas = CharField(
        
        widget=Textarea(
            attrs={
           'placeholder': 'Los componentes principales de el equipo',
                'class': 'form-control',
                'style':'color:black',
                  'required':'false'
            }
        ))
          
    ip_dir=CharField(required=False, widget=TextInput(
         
            attrs={
                'placeholder': 'Direccion IP',
                'class': 'form-control ',
                  'required':'false'
            }
        )
    )
    mac_dir = CharField(
        required=False,
        
        widget = TextInput(
            
            attrs={
                'placeholder': 'Direccion MAC',
                'class': 'form-control ',
                'required':'false'
            }
        ))
    


    class Meta:
        model = ComputoRegistrado
        fields = '__all__'

 

