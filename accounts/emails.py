from djoser.email import ActivationEmail


class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context["url"] = "http://localhost:3000/activate?uid={uid}&token={token}"
        return context
