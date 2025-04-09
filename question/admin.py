from django.contrib import admin

from question import models as m

admin.site.register(m.Question)
admin.site.register(m.Answer)
admin.site.register(m.Like)
admin.site.register(m.AnswerLike)
