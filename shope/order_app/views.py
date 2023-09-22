"""Order views"""

from typing import Any
from django.urls import reverse
import inject
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from core.utils.injector import configure_inject
from interface.order_interface import IOrder
from interface.order_item_interface import IOrderItem
from order_app.models import Order
from core.enums import PayType
from profile_app.forms import EditProfileForm, EditUserForm
from order_app.forms import CreateOrderForm

configure_inject()


class HistoryOrderView(LoginRequiredMixin, ListView):
    """Oreder list tempale class. Will be deleted"""
    template_name = 'order_app/historyorder.html'
    context_object_name = 'order_list'
    paginate_by = 3
    model = Order
    _order_list: IOrder = inject.attr(IOrder)

    def get_queryset(self):
        return self._order_list.get_list_by_user(self.request.user)  # type: ignore


class DetailOrderView(DetailView):
    """Детальная страница заказа"""
    template_name = 'order_app/oneorder.html'
    model = Order
    context_object_name = 'order'
    _order: IOrder = inject.attr(IOrder)
    _order_item = inject.attr(IOrderItem)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return self._order.get_by_pk(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self._order_item.get_by_order(self.get_object())  # type: ignore
        return context


class CreateOrderView(LoginRequiredMixin, CreateView):
    """Создание заказа"""
    template_name = 'order_app/order.html'
    context_object_name = 'order'
    form_class = CreateOrderForm
    model = Order
    _SUCCESS_MESSAGE = _('Your order has been created')

    def get_success_url(self) -> str:
        """get success url"""
        return reverse('order_app:history-order')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CreateOrderForm(self.request.POST, instance=self.request.user)  # type: ignore
            context['user_form'] = EditUserForm(self.request.POST,
                                                instance=self.request.user)
            context['profile_form'] = EditProfileForm(self.request.POST,
                                                      instance=self.request.user.profile)  # type: ignore
        else:
            context['user_form'] = EditUserForm(instance=self.request.user)
            context['profile_form'] = EditProfileForm(instance=self.request.user.profile)  # type: ignore

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        profile_form = context['profile_form']
        valid_list = [form.is_valid(), user_form.is_valid(), profile_form.is_valid()]
        if all(valid_list):
            order_form = form.save(commit=False)
            order_form.user = self.request.user
            order_form.save()
            user_form.save()
            profile_form.save()
        else:
            context.update({'user_form': user_form,
                            'profile_form': profile_form})

            return self.render_to_response(context)
        messages.success(self.request, self._SUCCESS_MESSAGE)
        return super().form_valid(form)
