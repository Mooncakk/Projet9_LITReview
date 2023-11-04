from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Value, CharField

from website.forms import TicketForm, ReviewForm
from website.models import Ticket, Review


# Create your views here

def home(request):
    return render(request, 'index.html')


def flux(request):

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET'))
    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda posts: posts.last_update, reverse=True)
    return render(request, 'flux.html', {'posts': posts})


def posts(request):

    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    posts = sorted(chain(tickets, reviews), key=lambda posts: posts.last_update, reverse=True)
    return render(request, 'posts.html', {'posts': posts})


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


def create_review_and_ticket(request):

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            ticket.user = request.user
            review.user, review.ticket = request.user, ticket
            ticket.save()
            review.save()
            messages.success(request, 'Votre critique a été créé avec succès')
        return redirect('post')

    ticket_form = TicketForm()
    review_form = ReviewForm()

    return render(request, 'review/create_review_and_ticket.html', {'ticket_form': ticket_form, 'review_form': review_form})


def create_review_from_ticket(request, pk):

    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Votre critique a été créé avec succès')
            return redirect('post')

    form = ReviewForm()
    return render(request, 'review/create_review.html', {'ticket': ticket, 'form': form})

