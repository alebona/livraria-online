from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Autor(models.Model):
    nome = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nome


class Editora(models.Model):
    nome = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    editora = models.ForeignKey(Editora, on_delete=models.SET_NULL, null=True)
    data_publicacao = models.DateField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    paginas = models.IntegerField()
    sinopse = models.TextField() 
    isbn_13 = models.CharField(max_length=20, unique=False)  
    isbn_10 = models.CharField(max_length=20, unique=False)    
    rating = models.FloatField(default=0.0)
    capa = models.URLField(max_length=500, null=True, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=10.00)

    def __str__(self):
        return self.titulo
