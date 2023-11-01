from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from website.forms import TicketForm, ReviewForm
from website.models import Ticket


# Create your views here

def home(request):
    return render(request, 'index.html')


def flux(request):

    tickets = Ticket.objects.all()
    return render(request, 'flux.html', {'tickets': tickets})


def posts(request):

    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'posts.html', {'tickets': tickets})


def create_ticket(request):

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            messages.success(request, 'Ticket créé avec succès')
        return redirect('post')

    form = TicketForm()

    return render(request, 'ticket/create_ticket.html', {'form': form})


def update_ticket(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre ticket a été modifié avec succès')
        return redirect('post')

    form = TicketForm(instance=ticket)
    return render(request, 'ticket/ticket_edit.html', {'ticket': ticket, 'form': form})


def delete_ticket(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)
    ticket.delete()
    messages.success(request, 'Votre ticket a été supprimé avec succès')
    return redirect('post')


def ticket_view(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)
    return render(request, 'ticket/delete_ticket_confirmation.html', {'ticket': ticket})


def create_review(request):

    review = ReviewForm()

