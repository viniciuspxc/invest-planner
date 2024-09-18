"""
Funções adicionais do programa
"""
import json
from abc import ABC, abstractmethod
from django.db.models.signals import post_save
from datetime import date
from .models import Investment, Notification
from django.dispatch import receiver
import requests
from django.core.cache import cache
from .models import Investment, Income, Expense
from django.utils.timezone import now
from decouple import config
from groq import Groq
from gpt4all import GPT4All


def get_central_bank_rate():
    """Recebe os dados da API do banco central

    Returns:
        dict[str, list[dict[str, Unknown]]]: context
    """
    url_cdi = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json"
    url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"

    def fetch_rate(url, cache_key_rate, cache_key_date):
        """Executa as chamadas http
        """
        rate, date = None, None
        try:
            response = requests.get(url, timeout=20)
        except requests.exceptions.Timeout:
            print("Timed out")

        if response.status_code == 200:
            data = response.json()
            if data:
                rate = data[-1]['valor']
                date = data[-1]['data']
                cache.set(cache_key_rate, rate, timeout=86400)
                cache.set(cache_key_date, date, timeout=86400)
        return rate, date

    cdi_rate, cdi_date = cache.get('cdi_rate'), cache.get('cdi_date')
    if cdi_rate is None or cdi_date is None:
        cdi_rate, cdi_date = fetch_rate(url_cdi, 'cdi_rate', 'cdi_date')

    selic_rate, selic_date = cache.get('selic_rate'), cache.get('selic_date')
    if selic_rate is None or selic_date is None:
        selic_rate, selic_date = fetch_rate(
            url_selic, 'selic_rate', 'selic_date')

    context = {
        'taxes': [
            {'name': 'cdi', 'rate': cdi_rate, 'date': cdi_date},
            {'name': 'selic', 'rate': selic_rate, 'date': selic_date}
        ]
    }
    return context


def get_user_data(user):
    customer_data = {
        # "name": user.username,
        # "email": user.email,
        "investments": [],
        "income": [],
        "expenses": []
    }

    investments = Investment.objects.filter(user=user)
    for investment in investments:
        customer_data["investments"].append({
            "title": investment.title,
            "starting_amount": float(investment.starting_amount),
            "number_of_years": str(investment.number_of_years),
            "return_rate": float(investment.return_rate),
            "additional_contribution": float(investment.additional_contribution),
            "rate_type": str(investment.rate_type),
            "rate_value": float(investment.rate_value),
            "rate_percentage": float(investment.rate_percentage),
            "active": bool(investment.active),
            "starting_date": str(investment.starting_date),
            "tags": [tag.name for tag in investment.tags.all()],

        })

    incomes = Income.objects.filter(user=user)
    for income in incomes:
        customer_data["income"].append({
            "title": income.title,
            "monthly_income": float(income.monthly_income),
            "tags": [tag.name for tag in income.tags.all()]
        })

    expenses = Expense.objects.filter(user=user)
    for expense in expenses:
        customer_data["expenses"].append({
            "title": expense.title,
            "monthly_expense": float(expense.monthly_expense),
            "tags": [tag.name for tag in expense.tags.all()]
        })

    return customer_data


@receiver(post_save, sender=Investment)
def check_investment_end_date(sender, instance, **kwargs):
    end_date = instance.calculate_end_date()

    if end_date <= now().date():
        Notification.objects.create(
            user=instance.user,
            message=f"Your investment '{
                instance.title}' has reached its end date.",
        )


@receiver(post_save, sender=Investment)
def notify_investment_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        message = f"Investment '{instance.title}' was created with amount {
            instance.starting_amount}."
    else:
        message = f"Investment '{instance.title}' was updated with new amount {
            instance.starting_amount}."

    Notification.objects.create(user=instance.user, message=message)


GROQ_API_KEY = config('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)  # type: ignore


class ChatModelStrategy(ABC):
    @abstractmethod
    def get_response(self, message, user_data):
        pass


class GROQChatModelStrategy(ChatModelStrategy):
    def __init__(self):
        self.client = Groq(api_key=config('GROQ_API_KEY'))  # type: ignore

    def get_response(self, message, user_data):

        try:
            completion = self.client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "User data is in the json: {user_data}; Your name is GROQ Model;" +
                        "Don't use formulas or codes; Calculate the values if asked; Use less than 100 words; Make sure calculations are correct"
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=0.2,
                max_tokens=200,
                top_p=0.65,
                stream=False,
                stop=None,
            )

            if hasattr(completion, 'choices') and len(completion.choices) > 0:
                response_message = completion.choices[0].message
                if hasattr(response_message, 'content'):
                    return response_message.content
                else:
                    return "Content not found in response."
            else:
                return "No choices available in response."

        except Exception as e:
            return f"An error occurred: {str(e)}"


class ChatAssistant:
    def __init__(self, strategy: ChatModelStrategy):
        self.strategy = strategy

    def chat(self, message, user_data):
        return self.strategy.get_response(message, user_data)


class GPT4AllChatModelStrategy(ChatModelStrategy):
    def __init__(self):
        self.model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device="kompute") # cpu or kompute

    def get_response(self, message, user_data):

        with self.model.chat_session():
            commands = (
                "User data is in the json: {user_data}; Your name is GPT4ALL Model;" +
                        "Don't use formulas or codes; Calculate the values if asked; Use less than 100 words; Make sure calculations are correct"
                "The prompt is:"
            )
            prompt = f"{commands} {message}"
            response = self.model.generate(prompt, max_tokens=200)
            return response.strip()
