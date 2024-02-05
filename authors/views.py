from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect, render
from authors.forms import RegisterForm, LoginForm
from pprint import pprint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html',
        {
            'form': form,
            'form_action': reverse('authors:register_create')
        }
    )


# View responsável somente por TRATAR os DADOS do FORMULÁRIO
def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST  # QueryDict com os dados de cada campo do formulário
    request.session['register_form_data'] = POST # Armazenando dados do formulário em uma chave da sessão.
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) # Salva um password criptografado no BD
        user.save()

        messages.success(request, 'Yor user is created! Please log in.')

        del(request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login.html', 
        {
            'form': form,
            'form_action': reverse('authors:login_create')
        }
    )


def login_create(request):
    
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    # Autenticando usuário
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Login successfully!')
            login(request, authenticated_user) 
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Error to validate form data.')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next') # Precisa estar logado para que a view funcione.
def logout_view(request):
    # Tentativa de logout sem estar logado, ou por meio de GET, gera mensagem de erro e Http404
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        raise Http404()
    
    # Redireciona o usuário que tente fazer logout com credenciais diferentes das do usuário atualmente autenticado
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))
    
    # Se estiver tudo válido, mostra mensagem de logout feito com sucesso
    messages.success(request, 'Logged out successfully')

    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next') # Precisa estar logado para que a view funcione.
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')