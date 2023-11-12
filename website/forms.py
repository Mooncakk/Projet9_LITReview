from django.forms import ModelForm, RadioSelect

from website.models import Ticket, Review


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


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre',
                  'rating': 'Note',
                  'body': 'Commentaire'}


