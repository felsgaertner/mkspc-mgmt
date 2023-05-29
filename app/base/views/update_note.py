from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from app.base.models import Person
from app.base.models.note import Note


class UpdateNoteView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        user = Person.objects.get(id=kwargs['user_id'])
        text = self.request.POST.get('text', '').strip()
        if text:
            Note.objects.update_or_create(user=user, defaults={'text': text})
        else:
            try:
                user.note.delete()
            except Person.note.RelatedObjectDoesNotExist:
                pass
        return redirect(user.get_absolute_url())
