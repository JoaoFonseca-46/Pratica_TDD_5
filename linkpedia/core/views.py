from .models import LinkModel
from .forms import LinkForm
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def login(request):

    if request.user.id is not None:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")

        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': LoginForm()})


def logout(request):

    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')

    return redirect("home")


@login_required
def home(request):

    context = {}

    return render(request, 'index.html', context)


@login_required
def listar_links(request):

    links = LinkModel.objects.all()

    context = {
        'links': links
    }

    return render(request, 'listar_links.html', context)


@login_required
def cadastrar_link(request):

    if request.method == 'POST':

        form = LinkForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_links')

    else:
        form = LinkForm()

    context = {
        'form': form
    }

    return render(request, 'cadastrar_link.html', context)


@login_required
def editar_link(request, id):

    link = get_object_or_404(LinkModel, id=id)

    if request.method == 'POST':

        form = LinkForm(request.POST, instance=link)

        if form.is_valid():
            form.save()
            return redirect('listar_links')

    else:
        form = LinkForm(instance=link)

    context = {
        'form': form,
        'link': link
    }

    return render(request, 'editar_link.html', context)


@login_required
def excluir_link(request, id):

    link = get_object_or_404(LinkModel, id=id)

    if request.method == 'POST':
        link.delete()
        return redirect('listar_links')

    context = {
        'link': link
    }

    return render(request, 'excluir_link.html', context)