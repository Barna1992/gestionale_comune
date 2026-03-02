import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _get_issue_url(issue, request):
    return request.build_absolute_uri(issue.get_absolute_url())


def _get_involved_emails(issue, exclude_user=None):
    """Get emails of all involved users (assignees + CC), excluding one user."""
    emails = set()
    for user in issue.assignee.all():
        if user != exclude_user and user.email:
            emails.add(user.email)
    for user in issue.cc.all():
        if user != exclude_user and user.email:
            emails.add(user.email)
    if issue.owner and issue.owner != exclude_user and issue.owner.email:
        emails.add(issue.owner.email)
    return list(emails)


def notify_issue_assigned(issue, request):
    """Notify assignees and CC when a new issue is created."""
    recipients = _get_involved_emails(issue, exclude_user=request.user)
    if not recipients:
        return

    context = {
        'issue': issue,
        'issue_url': _get_issue_url(issue, request),
        'created_by': request.user.get_full_name() or request.user.username,
    }

    subject = f'[Gestionale Comune] Nuova segnalazione: #{issue.pk} - {issue.title}'
    body = render_to_string('issue/email/issue_assigned.txt', context)

    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception('Errore invio email notifica nuova segnalazione #%s', issue.pk)


def notify_comment_added(comment, request):
    """Notify all involved users when a comment is added."""
    issue = comment.post
    recipients = _get_involved_emails(issue, exclude_user=request.user)
    if not recipients:
        return

    context = {
        'issue': issue,
        'comment': comment,
        'issue_url': _get_issue_url(issue, request),
        'commenter': request.user.get_full_name() or request.user.username,
    }

    subject = f'[Gestionale Comune] Nuovo commento su #{issue.pk} - {issue.title}'
    body = render_to_string('issue/email/comment_added.txt', context)

    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception('Errore invio email notifica commento su #%s', issue.pk)


def notify_state_changed(issue, old_state, new_state, changed_by, request):
    """Notify all involved users when issue state changes."""
    recipients = _get_involved_emails(issue, exclude_user=changed_by)
    if not recipients:
        return

    state_labels = dict(issue._meta.get_field('state').choices)

    context = {
        'issue': issue,
        'issue_url': _get_issue_url(issue, request),
        'changed_by': changed_by.get_full_name() or changed_by.username,
        'old_state': str(state_labels.get(old_state, old_state)),
        'new_state': str(state_labels.get(new_state, new_state)),
    }

    subject = f'[Gestionale Comune] Stato cambiato per #{issue.pk} - {issue.title}'
    body = render_to_string('issue/email/state_changed.txt', context)

    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception('Errore invio email notifica cambio stato #%s', issue.pk)
