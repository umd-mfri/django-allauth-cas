# -*- coding: utf-8 -*-
from django.urls import include, re_path
from django.utils.module_loading import import_string


def default_urlpatterns(provider):
    package = provider.get_package()

    try:
        login_view = import_string(package + '.views.login')
    except ImportError:
        raise ImportError(
            "The login view for the '{id}' provider is lacking from the "
            "'views' module of its app.\n"
            "You may want to add:\n"
            "from allauth_cas.views import CASLoginView\n\n"
            "login = CASLoginView.adapter_view(<LocalCASAdapter>)"
            .format(id=provider.id)
        )

    try:
        callback_view = import_string(package + '.views.callback')
    except ImportError:
        raise ImportError(
            "The callback view for the '{id}' provider is lacking from the "
            "'views' module of its app.\n"
            "You may want to add:\n"
            "from allauth_cas.views import CASCallbackView\n\n"
            "callback = CASCallbackView.adapter_view(<LocalCASAdapter>)"
            .format(id=provider.id)
        )

    try:
        logout_view = import_string(package + '.views.logout')
    except ImportError:
        logout_view = None

    urlpatterns = [
        re_path('^login/$', login_view,
            name=provider.id + '_login'),
        re_path('^login/callback/$', callback_view,
            name=provider.id + '_callback'),
    ]

    if logout_view is not None:
        urlpatterns += [
            re_path('^logout/$', logout_view,
                name=provider.id + '_logout'),
        ]

    return [re_path('^' + provider.get_slug() + '/', include(urlpatterns))]
