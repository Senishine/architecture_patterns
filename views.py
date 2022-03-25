from my_framework.rendering import render


class HomePage:
    def __call__(self, request):
        return '200 OK', render('index.html', title="SpeakEnglish")


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', title="About us")


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', title="Contacts")


