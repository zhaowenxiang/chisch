# coding: utf-8

import logging
import datetime

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)

from django.db import models
from django.db.models import Q
from django.utils import timezone

from chisch.common import exceptions
from chisch.common import dependency
from chisch.utils import stringutils
from chisch.common.constents import (
    TOKEN_EFFECTIVE_TIME as TET,
    TOKEN_INVALID_REASON_UNRECOGNIZED as TIRU,
    TOKEN_INVALID_REASON_EXPIRE as TIRE,
    TOKEN_INVALID_REASON_LOGIN_OTHER_PLACE as TIRLOP,
)


logger = logging.getLogger('django')


@dependency.requires('user_manager')
@dependency.provider('auth_manager')
class AuthManager(models.Manager):

    def _build_token_model(self, user, agent_idfa):
        access_token = stringutils.generate_token()
        take_effect_at = timezone.now()
        invalid_at = take_effect_at + datetime.timedelta(days=TET)

        token = self.model(user_id=user.id,
                           access_token=access_token,
                           take_effect_at=take_effect_at,
                           invalid_at=invalid_at,
                           agent_idfa=agent_idfa)
        return token

    def _create_token(self, user, agent_idfa):
        token = self._build_token_model(user, agent_idfa)

        try:
            token.save(using=self._db)
        except Exception:
            #TODO LOG
            raise
        return token

    def _destroy_token(self, access_token):
        if access_token is None:
            return
        token = self.get(access_token=access_token)
        token.delete(using=self.db)

    def _flush_token(self, user_id, agent_idfa, all=False):
        if all:
            self.filter(user_id=user_id).delete()
            return
        agent_idfa_arr = agent_idfa.split('-')
        agent_type = agent_idfa_arr[0]
        agent_os = agent_idfa_arr[1]
        agent_id = agent_idfa_arr[2]
        tokens = self.filter(Q(user_id=user_id)
                             &
                             Q(agent_idfa__istartswith=agent_type))
        for token in tokens:
            if (token.agent_os != agent_os) or \
                (token.agent_os == agent_os and
                 token.agent_id != agent_id):
                token.invalid_reason = TIRLOP
                token.save(using=self.db)
            else:
                token.delete(using=self.db)

    def recognise_access_token(self, access_token):
        try:
            token = self.get(access_token=access_token)
        except self.model.DoesNotExist:
            raise exceptions.InvalidAccessTokenErr(reason=TIRU)
        if token.invalid_reason is not None:
            raise exceptions.InvalidAccessTokenErr(reason=token.invalid_reason)
        if timezone.now() >= token.invalid_at:
            raise exceptions.InvalidAccessTokenErr(reason=TIRE)
        user = self.user_manager.get(id=token.user_id)
        return user

    def login(self, request, user, **kwargs):

        user_logged_in.send(sender=user.__class__, request=request, user=user)

        agent_idfa = kwargs.get('agent_idfa', None)
        flush_all_token = kwargs.get('flush_all_token', False)
        self._flush_token(user.id, agent_idfa, all=flush_all_token)
        token = self._create_token(user, agent_idfa)
        setattr(user, 'access_token', token.access_token)

    def logout(self, request):
        user = getattr(request, 'user', None)
        user_logged_out.send(sender=user.__class__, request=request, user=user)
        self._destroy_token(request.access_token)
