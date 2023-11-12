from django.forms import ModelForm, forms, widgets

from website.models import Ticket, Review, UserFollows


class TicketForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'thumbnail']
        labels = {'title': 'Titre',
                  'description': 'Description',
                  'thumbnail': 'Image',
                  }


class ReviewForm(ModelForm, forms.Form):

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre',
                  'rating': 'Note',
                  'body': 'Commentaire'}




