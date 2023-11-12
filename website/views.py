from itertools import chain

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Value, CharField

from accounts.models import User
from website.forms import TicketForm, ReviewForm
from website.models import Ticket, Review, UserFollows


# Create your views here
def home(request):

    return render(request, 'index.html')


def flux(request):

    if request.user.is_authenticated:
        current_user = request.user
        user_followed = UserFollows.objects.filter(followed_user_id=current_user)
        user_followed = [user.user_id for user in user_followed]

        reviews = Review.objects.all()
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        reviews = [post for post in reviews if post.user_id in user_followed]

        tickets = Ticket.objects.all()
        tickets = tickets.annotate(content_type=Value('TICKET'))
        tickets = [post for post in tickets if post.user_id in user_followed]

        posts = sorted(chain(tickets, reviews), key=lambda posts: posts.last_update, reverse=True)

        return render(request, 'flux.html', {'posts': posts})

    else:
        messages.success(request, 'Vous devez être connecter pour acceder à cette page...')
        return redirect('connexion')


def posts(request):

    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET'))
        reviews = Review.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        posts = sorted(chain(tickets, reviews), key=lambda posts: posts.last_update, reverse=True)

        return render(request, 'posts.html', {'posts': posts})


def follow_page(request):

    if request.user.is_authenticated:
        current_user = request.user.id
        user_followed = UserFollows.objects.filter(followed_user_id=current_user)
        follower = UserFollows.objects.filter(user_id=current_user)

        return render(request, 'follow_page.html', {'user_followed': user_followed,
                                                'follower': follower})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def search_user(request):

    if request.user.is_authenticated:
        current_user = request.user
        user_followed = UserFollows.objects.filter(followed_user_id=current_user)

        if request.method == 'POST':
            search = request.POST['search']
            searched_user = User.objects.filter(username__icontains=search)
            user_followed = [user.user for user in user_followed]
            searched_user = searched_user.exclude(username=current_user).exclude(username__in=user_followed)

            return render(request, 'searched_user.html', {'search': search,
                                                      'searched_user': searched_user})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def follow(request, pk):

    if request.user.is_authenticated:
        user_to_follow = get_object_or_404(User, id=pk)
        followed_user = request.user
        new_follow = UserFollows.objects.create(user_id=user_to_follow.id, followed_user=followed_user)
        new_follow.save()
        messages.warning(request, f'Vous êtes maintenant abonné à {user_to_follow}')

        return redirect('page_abonnement')

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def unfollow(request, pk):

    if request.user.is_authenticated:
        username = get_object_or_404(User, id=pk)
        user_to_unfollow = get_object_or_404(UserFollows, user_id=pk)
        user_to_unfollow.delete()
        messages.success(request, f"Vous n'êtes plus abonné à {username}")

        return redirect('page_abonnement')

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def create_ticket(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)

            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                messages.success(request, 'Ticket créé avec succès')
            return redirect('posts')

        form = TicketForm()

        return render(request, 'ticket/create_ticket.html', {'form': form})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def update_ticket(request, pk):

    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, id=pk)

        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)

            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                messages.success(request, 'Votre ticket a été modifié avec succès')
            return redirect('posts')

        form = TicketForm(instance=ticket)

        return render(request, 'ticket/ticket_edit.html', {'ticket': ticket, 'form': form})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def ticket_view(request, pk):

    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, id=pk)

        return render(request, 'ticket/delete_ticket_confirmation.html', {'post': ticket})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def delete_ticket(request, pk):

    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, id=pk)
        ticket.delete()
        messages.success(request, 'Votre ticket a été supprimé avec succès')

        return redirect('posts')

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def create_review_and_ticket(request):

    if request.user.is_authenticated:

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
            return redirect('posts')

        ticket_form = TicketForm()
        review_form = ReviewForm()

        return render(request, 'review/create_review_and_ticket.html',
                      {'ticket_form': ticket_form, 'review_form': review_form})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def create_review_from_ticket(request, pk):

    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, id=pk)

        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():
                review = form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()
                messages.success(request, 'Votre critique a été créé avec succès')
                return redirect('posts')

        form = ReviewForm()

        return render(request, 'review/create_review.html', {'post': ticket, 'form': form})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def update_review(request, pk):

    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=pk)
        ticket = get_object_or_404(Ticket, id=review.ticket.id)

        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)

            if form.is_valid():
                review = form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()
                messages.success(request, 'Votre critique a été modifié avec succès')
                return redirect('posts')
        form = ReviewForm(instance=review)

        return render(request, 'review/review_edit.html', {'form': form, 'post': ticket})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def review_view(request, pk):

    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=pk)

        return render(request, 'review/delete_review_confirmation.html', {'post': review})

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')


def delete_review(request, pk):

    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=pk)

        if review:
            review.delete()
            messages.success(request, 'Votre critique a été supprimé avec succès')
        else:
            messages.success(request, "Cette critique n'existe pas")

        return redirect('posts')

    else:
        messages.success(request, 'Vous devez être connecter pour accéder à cette page...')
        return redirect('connexion')
