from django.forms import CheckboxSelectMultiple
from django.template import Library

register = Library()


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxSelectMultiple().__class__.__name__


@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='priority_badge_class')
def priority_badge_class(priority):
    mapping = {
        0: 'badge-priority-none',
        1: 'badge-priority-bassa',
        2: 'badge-priority-media',
        3: 'badge-priority-alta',
    }
    return mapping.get(priority, 'badge-priority-none')


@register.filter(name='state_badge_class')
def state_badge_class(state):
    mapping = {
        1: 'badge-state-inserita',
        2: 'badge-state-presa-in-carico',
        3: 'badge-state-risolta',
        4: 'badge-state-riaperta',
        5: 'badge-state-da-verificare',
    }
    return mapping.get(state, 'badge-state-inserita')
